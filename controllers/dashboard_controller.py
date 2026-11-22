# Controle da supervisão do sistema
from datetime import datetime, timedelta # data/hora e intervalo de tempo
import pyqtgraph as pg # desenhar gráficos
from PySide6.QtCore import QTimer, QDate # Executa função a cada certo período e base para datas
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox # Base da janela principal e texto dentro das células da tabela
from ui.Ui_dashboard import Ui_MainWindow # Interface criada pelo Qt Designer
from models.medicao import Medicao # Medições
from models.registro import Registro # Evento registrado no sistema
from controllers.comunicacao_controller import ComunicacaoController
from controllers.configuracao_controller import ConfiguracaoController
from models.configuracao import Configuracao
from models.registro_repository import RegistroRepository
import logging
import math

logger = logging.getLogger(__name__)

# Classe principal
class DashController(QMainWindow):
    def __init__(self):
        super().__init__()

        # Carregando a interface
        self.ui = Ui_MainWindow() # Objeto que representa a interface
        self.ui.setupUi(self) # Coloca a interface dentro da janela
        # Passa a ter acesso aos componentes

        # Inicializa o filtro com a data atual
        hoje = QDate.currentDate()
        self.ui.data_inicio.setDate(hoje)
        self.ui.data_fim.setDate(hoje)

        # Indica se o filtro de data está ativo
        self.filtro_data_ativo = False

        # Guarda os registros de eventos do sistema
        self.registros = []

        # Guarda o histórico das leituras brutas recebidas do Arduino
        self.historico_adc = []

        # Guarda se o limite de potência já foi ultrapassado
        self.limite_ultrapassado = False

        # Se a potência ultrapassar o limite configurado por esse fator, disjuntor dispara sozinho
        self.fator_sobrecorrente = 1.5
        self.medicao_disparo = None
        # Indica que a proteção automática já realizou uma tentativa de disparo
        self.protecao_sobrecorrente_disparada = False
        # False = não clalibrado, True = calibrado
        self.protecao_automatica_habilitada = True
        # Evita repetir logs enquanto a comunicação estiver indisponível
        self.protecao_comunicacao_indisponivel = False
        # Evita repetir logs enquanto o limite de potência está pendente
        self.protecao_limite_pendente = False

        # Conta amostras consecutivas acima do limite de disparo (evita corte por uma amostra ruim)
        self.amostras_sobrecorrente = 0
        # Quantidade de amostras consecutivas necessárias para o disparo automático
        self.amostras_para_disparo = 3
        # Janela de carência da proteção logo após conectar (transitório do ADC)
        self.ignorar_protecao_ate = None

        # Energiza (envia !1) uma única vez ao conectar, se o relé estiver aberto
        # Coloque False para apenas espelhar o estado informado pelo hardware
        self.energizar_ao_conectar = True
        # Indica que a energização inicial já foi tentada nesta conexão
        self.tentou_energizar_ao_conectar = False
        # Indica que a energização inicial aguarda confirmação do relé
        self.energizando_ao_conectar = False
        # Guarda o estado anterior da conexão serial para detectar mudanças
        self.conexao_anterior = False

        # Guarda a última medição recebida do hardware
        self.medicao_atual = None
        # Guarda o estado anterior do disjuntor, inicialmente desconhecido
        self.disjuntor_anterior = None
        self.dados_serial_atual = None
        self.acao_rele_pendente = None

        self.confirmacoes_rele_aberto = 0
        self.timer_confirmacao_rele = QTimer(self)
        self.timer_confirmacao_rele.setSingleShot(True)
        self.timer_confirmacao_rele.timeout.connect(
            self.ao_expirar_confirmacao_rele
        )

        self.modo_tempo_real = False

        # Configura o gráfico, chama a função que cria o gráfico
        self.configurar_grafico()

        # Configura a tabela de registros, define tamanho das colunas
        self.configurar_tabela()

        # Recupera eventos salvos no bd antes
        self.carregar_registros()

        # Att interface p/ exibir eventos recuperados
        self.atualizar_tabela()

        # Registra evento p/ indicar que sistema iniciou supervisao
        self.adicionar_registro(
            tipo="Status",
            descricao="Sistema de supervisão iniciado. Aguardando dados do Arduino.",
            valor="Sem medição"
        )

        # Medição inicial
        self.atualizar_dashboard()

        # Modelo compartilhado de configuração (carrega do arquivo na inicialização)
        self.model_config = Configuracao()
        self.ui.spin_limite_potencia.setValue(self.model_config.lim_potencia)

        # Limite efetivamente aplicado à proteção.
        # O valor digitado fica pendente até o usuário clicar em OK.
        self.limite_potencia_aplicado = self.model_config.lim_potencia
        self.limite_potencia_pendente = False

        # Guarda o estado do corte de emergência
        self.corte_emergencia_ativo = False
        # Controla o corte de emergência
        self.ui.btn_corte_emergencia.clicked.connect(self.alternar_corte_emergencia)

        self.ui.btn_tempo_real.clicked.connect(
            self.alternar_tempo_real
        )

        # Alterações no campo ficam pendentes até clicar em OK.
        self.ui.spin_limite_potencia.valueChanged.connect(self.marcar_limite_pendente)
        self.ui.btn_ok_limite.clicked.connect(self.confirmar_limite_potencia)

        # Guarda instância do controller de comunicação serial
        self.comunicacao_controller = ComunicacaoController(self)
        # Conecta o sinal de dados recebidos ao método responsável q recebe na dash
        self.comunicacao_controller.dados_serial_recebidos.connect(
            self.ao_receber_dados_serial
        )

        # Monitora a conexão serial para reiniciar o estado quando ela muda
        # (funciona mesmo com a janela de comunicação aberta)
        self.timer_monitor_conexao = QTimer(self)
        self.timer_monitor_conexao.timeout.connect(self.monitorar_conexao)
        self.timer_monitor_conexao.start(200)

        # Abre a janela de comunicação serial
        self.ui.btn_comunicacao.clicked.connect(self.abrir_comunicacao)

        # Abre a janela de configuração de limites (QDialog modal)
        self.ui.btn_configuracao.clicked.connect(self.abrir_configuracao)

        # Conecta os botões de filtro de data
        self.ui.btn_filtrar.clicked.connect(self.filtrar_historico_por_data)
        self.ui.btn_limpar_filtro.clicked.connect(self.limpar_filtro_data)


    # Detecta conexão/desconexão e reinicia o estado da supervisão
    def monitorar_conexao(self):
        conectado = bool(self.comunicacao_controller.model.is_connected)

        if conectado != self.conexao_anterior:
            self.conexao_anterior = conectado
            self.resetar_estado_conexao()

    # Descarta o estado da sessão anterior para o hardware ser sincronizado do zero
    def resetar_estado_conexao(self):
        self.timer_confirmacao_rele.stop()
        self.acao_rele_pendente = None

        self.dados_serial_atual = None
        self.medicao_atual = None
        # Força nova sincronização com o estado real do hardware
        self.disjuntor_anterior = None
        self.corte_emergencia_ativo = False
        self.limite_ultrapassado = False

        self.protecao_sobrecorrente_disparada = False
        self.medicao_disparo = None
        self.amostras_sobrecorrente = 0
        self.tentou_energizar_ao_conectar = False
        self.energizando_ao_conectar = False
        # Carência para ignorar transitórios logo após conectar
        self.ignorar_protecao_ate = datetime.now() + timedelta(seconds=2)

        self.ui.btn_corte_emergencia.setText("⚠  CORTE DE EMERGÊNCIA")
        self.ui.lbl_valor_potencia.setStyleSheet(
            "font-weight: bold;"
        )

        # Volta para "AGUARDANDO MEDIÇÃO"
        self.atualizar_dashboard()

    # Monta evento com medição atual antes de registrar corte
    def executar_corte(self, aberto, tipo, descricao, valor_medicao=None):
        registro = Registro(
            tipo=tipo,
            descricao=descricao,
            valor=(
                valor_medicao
                if valor_medicao is not None
                else self.formatar_medicao()
            )
        )
        try:
            # Att disjuntor e salva o evento
            id_registro = RegistroRepository.registrar_corte(
                aberto=aberto,
                registro=registro
            )
        except Exception as erro:
            # Registra log no smartgrid.log
            logger.exception(
                "Falha na operação de corte emergencial. "
                "A transação foi revertida quando aplicável: %s",
                erro
            )

            # Informa a falha sem modificar o estado
            QMessageBox.critical(
                self,
                "Falha no registro da operação",
                (
                    "O Arduino confirmou a alteração física do relé, "
                    "mas não foi possível registrar o evento no banco de dados.\n\n"
                    "Verifique a persistência e o histórico do sistema.\n\n"
                    f"Detalhes: {erro}"
                )
            )
            return False

        # Guarda o id gerado pelo bd no objeto do evento
        registro.id = id_registro

        # Registra log no smartgrid.log
        if aberto:
            logger.warning(
                "Corte de emergência registrado com sucesso. "
                "Disjuntor: ABERTO. Tipo: %s. Descrição: %s",
                tipo,
                descricao
            )
        else:
            logger.info(
                "Retomada do sistema registrada com sucesso. "
                "Disjuntor: FECHADO. Tipo: %s. Descrição: %s",
                tipo,
                descricao
            )

        # Att lista em memória
        self.registros.insert(0, registro)
        self.atualizar_tabela()
        return True

    def solicitar_acao_rele(self, acao, comando):
        # Evita enviar comandos enquanto outro aguarda confirmação
        if self.acao_rele_pendente is not None:
            logger.warning("Já existe uma operação do relé pendente.")
            return False

        # Registra a ação antes do envio para evitar perder uma confirmação rápida
        self.acao_rele_pendente = acao

        # Envia o comando diretamente ao Arduino
        try:
            enviado = self.comunicacao_controller.model.enviar_comando(
                comando
            )
        except Exception:
            logger.exception("Erro ao enviar comando para o relé")

            self.acao_rele_pendente = None

            QMessageBox.critical(
                self,
                "Erro de comunicação",
                "Não foi possível enviar o comando ao Arduino."
            )
            return False

        # Verifica se o comando foi enviado
        if not enviado:
            self.acao_rele_pendente = None

            QMessageBox.warning(
                self,
                "Falha no comando",
                "O comando não foi enviado ao Arduino."
            )
            return False

        # Aguarda até 3 segundos pela confirmação do relé
        self.timer_confirmacao_rele.start(3000)

        logger.info(
            "Comando %s enviado. Aguardando confirmação do Arduino.",
            comando
        )

        return True

    # Confirma corte/reativação do sistema por Arduino
    def alternar_corte_emergencia(self):
        # Evita enviar comandos enquanto outro aguarda confirmação
        if self.acao_rele_pendente is not None:
            QMessageBox.warning(
                self,
                "Operação pendente",
                "Aguarde a confirmação da operação atual pelo Arduino."
            )
            return

        # Define a ação de acordo com o estado atual
        if not self.corte_emergencia_ativo:
            resposta = QMessageBox.question(
                self,
                "Corte de emergência",
                "Deseja realizar o corte de emergência?"
            )

            if resposta != QMessageBox.StandardButton.Yes:
                return

            acao = {
                "aberto": True,
                "status_esperado": 0,
                "tipo": "Alerta",
                "descricao": "Corte de emergência acionado."
            }

            comando = "!0"

        else:
            resposta = QMessageBox.question(
                self,
                "Reativar sistema",
                "Deseja reativar o sistema?"
            )

            if resposta != QMessageBox.StandardButton.Yes:
                return

            acao = {
                "aberto": False,
                "status_esperado": 1,
                "tipo": "Status",
                "descricao": "Sistema reativado após corte de emergência."
            }

            comando = "!1"
        # Solicita ação de abertura/fechamento do rele
        self.solicitar_acao_rele(acao, comando)

    # Trata o caso em que o Arduino não confirma o comando enviado
    def ao_expirar_confirmacao_rele(self):
        # Guarda a operação que não recebeu confirmação
        acao = self.acao_rele_pendente

        # Limpa a operação pendente
        self.acao_rele_pendente = None

        if acao is None:
            return

        # Sem confirmação da energização inicial: passa a mostrar o estado real
        if self.energizando_ao_conectar:
            self.energizando_ao_conectar = False
            self.atualizar_dashboard()
        logger.warning(
            "Timeout aguardando confirmação do relé. "
            "Estado esperado: %s",
            acao["status_esperado"]
        )
        QMessageBox.warning(
            self,
            "Sem confirmação do Arduino",
            (
                "O comando foi enviado, mas não houve confirmação do estado do relé.\n\n"
                "O estado do sistema não será atualizado na interface."
            )
        )

    # Cria e configura gráfico
    def configurar_grafico(self):
        # Cria o gráfico principal
        self.grafico = pg.PlotWidget()
        self.grafico.setBackground("w")

        self.grafico.setTitle(
            "Sinais dos circuitos de medição",
            color="#24343B",
            size="12pt"
        )

        self.grafico.setLabel("left", "Valor ADC")
        self.grafico.setLabel("bottom", "Horário")
        self.grafico.setYRange(0, 1023)

        self.grafico.showGrid(x=True, y=True, alpha=0.15)
        self.grafico.setMinimumHeight(190)

        # Utiliza eixo com horário
        eixo_tempo = pg.DateAxisItem(orientation="bottom")
        self.grafico.setAxisItems({"bottom": eixo_tempo})

        # Legenda das curvas
        self.grafico.addLegend()

        # Curva do sinal A0
        self.curva_a0 = self.grafico.plot(
            pen=pg.mkPen(color="#2878B8", width=2),
            name="A0"
        )

        # Curva do sinal A1
        self.curva_a1 = self.grafico.plot(
            pen=pg.mkPen(color="#D97732", width=2),
            name="A1"
        )

        # Insere o gráfico no layout da dashboard
        layout = self.ui.widget_grafico.layout()

        if layout is None:
            from PySide6.QtWidgets import QVBoxLayout
            layout = QVBoxLayout(self.ui.widget_grafico)

        layout.addWidget(self.grafico)


    def atualizar_grafico(self):
        # Não atualiza o gráfico sem leituras
        if not self.historico_adc:
            return

        agora = datetime.now()

        if self.modo_tempo_real:
            # Exibe somente as leituras dos últimos 60 segundos
            limite = agora - timedelta(seconds=60)

            historico = [
                item
                for item in self.historico_adc
                if item["timestamp"] >= limite
            ]
        else:
            # Exibe as leituras das últimas 24 horas
            limite = agora - timedelta(hours=24)

            historico = [
                item
                for item in self.historico_adc
                if item["timestamp"] >= limite
            ]

        if not historico:
            self.curva_a0.setData([], [])
            self.curva_a1.setData([], [])
            return

        tempos = [
            item["timestamp"].timestamp()
            for item in historico
        ]

        valores_a0 = [
            item["a0"]
            for item in historico
        ]

        valores_a1 = [
            item["a1"]
            for item in historico
        ]

        # Atualiza as duas curvas
        self.curva_a0.setData(tempos, valores_a0)
        self.curva_a1.setData(tempos, valores_a1)

        # Ajusta o eixo horizontal ao intervalo exibido
        if self.modo_tempo_real:
            inicio = (agora - timedelta(seconds=60)).timestamp()
            fim = agora.timestamp()
        else:
            inicio = limite.timestamp()
            fim = agora.timestamp()

        self.grafico.setXRange(inicio, fim, padding=0)

    def alternar_tempo_real(self):
        self.modo_tempo_real = not self.modo_tempo_real

        if self.modo_tempo_real:
            self.ui.btn_tempo_real.setText("24 Horas")
        else:
            self.ui.btn_tempo_real.setText("Tempo Real")

        self.atualizar_grafico()
    
    def atualizar_dashboard(self):

        # Verifica se existe telemetria recebida
        # (também aguarda enquanto a energização inicial não é confirmada)
        if self.dados_serial_atual is None or self.energizando_ao_conectar:
            self.ui.lbl_valor_tensao.setText("--")
            self.ui.lbl_valor_corrente.setText("--")
            self.ui.lbl_valor_potencia.setText("--")

            self.ui.lbl_status_disjuntor.setText(
                "AGUARDANDO MEDIÇÃO"
            )
            self.ui.lbl_status_detalhe.setText(
                "Aguardando dados do Arduino."
            )
            self.ui.lbl_status_atualizacao.setText(
                "Última atualização: --"
            )
            return

        dados = self.dados_serial_atual
        medicao = self.medicao_atual

        status_rele = int(dados["status_rele"])

        # Sistema desenergizado: grandezas elétricas zeradas
        if status_rele == 0:
            self.ui.lbl_valor_tensao.setText("0.00 V")
            self.ui.lbl_valor_corrente.setText("0.00 A")
            self.ui.lbl_valor_potencia.setText("0.00 W")

            self.ui.lbl_status_disjuntor.setText(
                "ABERTO / PROTEÇÃO ATIVADA"
            )

            self.ui.lbl_status_detalhe.setText(
                "A instalação encontra-se desenergizada."
            )

            estado = "aberto"

        else:
            # Sistema energizado: exibe as grandezas reais
            if medicao is not None:
                self.ui.lbl_valor_tensao.setText(
                    f"{medicao.tensao:.2f} V"
                )
                self.ui.lbl_valor_corrente.setText(
                    f"{medicao.corrente:.2f} A"
                )
                self.ui.lbl_valor_potencia.setText(
                    f"{medicao.potencia:.2f} W"
                )
            else:
                self.ui.lbl_valor_tensao.setText("--")
                self.ui.lbl_valor_corrente.setText("--")
                self.ui.lbl_valor_potencia.setText("--")

            self.ui.lbl_status_disjuntor.setText(
                "FECHADO / NORMAL"
            )

            self.ui.lbl_status_detalhe.setText(
                f"Relé energizado | "
                f"A0: {dados['a0']} | "
                f"A1: {dados['a1']} | "
                f"Botão: {dados['status_botao']}"
            )

            estado = "fechado"

        # Atualiza estado visual
        self.ui.statusCard.setProperty("estado", estado)
        self.ui.lbl_status_disjuntor.setProperty("estado", estado)

        for widget in (
            self.ui.statusCard,
            self.ui.lbl_status_disjuntor
        ):
            widget.style().unpolish(widget)
            widget.style().polish(widget)

        # Horário da última comunicação recebida
        horario = datetime.now().strftime("%H:%M:%S")

        self.ui.lbl_status_atualizacao.setText(
            f"Última atualização: {horario}"
        )

    def marcar_limite_pendente(self):
        # O valor digitado ainda não foi confirmado.
        if self.ui.spin_limite_potencia.value() != self.limite_potencia_aplicado:
            self.limite_potencia_pendente = True

            # Diferencia visualmente o valor pendente.
            self.ui.spin_limite_potencia.setStyleSheet(
                "QDoubleSpinBox { color: #B07A00; }"
            )
        else:
            self.limite_potencia_pendente = False
            self.ui.spin_limite_potencia.setStyleSheet("")

    def verificar_limite(self):
        # Verifica o limite usando a medição atual
        
        if self.medicao_atual is None:
            return
        
        # Usa somente o limite confirmado.
        limite = self.limite_potencia_aplicado

        ultrapassou_limite = (
            self.medicao_atual.potencia > limite
        )

        if ultrapassou_limite:
            self.ui.lbl_valor_potencia.setStyleSheet(
                "color: #D64545; font-weight: bold;"
            )
        else:
            self.ui.lbl_valor_potencia.setStyleSheet(
                "font-weight: bold;"
            )

    def verificar_protecao_sobrecorrente(self):
        # Impede o acionamento com medições não calibradas
        if not self.protecao_automatica_habilitada:
            return

        # Evita repetir comandos após uma tentativa de proteção automática
        if self.protecao_sobrecorrente_disparada:
            return

        # Impede a avaliação sem uma medição válida
        if self.medicao_atual is None:
            return

        # Ignora a proteção durante a carência logo após conectar
        if (
            self.ignorar_protecao_ate is not None
            and datetime.now() < self.ignorar_protecao_ate
        ):
            self.amostras_sobrecorrente = 0
            return

        # Não avalia sobrecorrente durante alteração do limite
        if self.limite_potencia_pendente:
            if not self.protecao_limite_pendente:
                logger.warning(
                    "Proteção automática temporariamente suspensa: "
                    "alteração do limite de potência pendente."
                )

            self.protecao_limite_pendente = True
            return

        # Registra que a alteração do limite foi concluída
        if self.protecao_limite_pendente:
            logger.info(
                "Alteração do limite de potência concluída. "
                "Proteção automática retomada."
            )
            self.protecao_limite_pendente = False

        # Valida a potência antes de utilizá-la na proteção
        try:
            potencia = float(self.medicao_atual.potencia)
            limite = float(self.limite_potencia_aplicado)
        except (TypeError, ValueError):
            logger.warning(
                "Proteção automática ignorada: potência ou limite inválido."
            )
            return

        # Impede o uso de valores não numéricos ou fora do domínio esperado
        if not math.isfinite(potencia) or not math.isfinite(limite):
            logger.warning(
                "Proteção automática ignorada: valor numérico inválido."
            )
            return

        if potencia < 0 or limite < 0:
            logger.warning(
                "Proteção automática ignorada: potência ou limite negativo."
            )
            return

        # Limite zero faria qualquer potência positiva disparar a proteção
        if limite == 0:
            logger.warning(
                "Proteção automática ignorada: limite de potência é zero."
            )
            return

        # Evita novos acionamentos enquanto existe uma operação pendente
        if self.acao_rele_pendente is not None:
            return

        # Proteção automática só atua com o relé fisicamente fechado
        if not self.medicao_atual.disjuntor:
            self.amostras_sobrecorrente = 0
            return

        # Evita corte redundante se o sistema já estiver em emergência
        if self.corte_emergencia_ativo:
            return

        # Usa somente valores validados e o limite de potência confirmado
        sobrecorrente_severa = (
            potencia > limite * self.fator_sobrecorrente
        )

        if not sobrecorrente_severa:
            self.amostras_sobrecorrente = 0
            return

        # Exige amostras consecutivas acima do limite antes de disparar
        self.amostras_sobrecorrente += 1

        if self.amostras_sobrecorrente < self.amostras_para_disparo:
            return

        # Verifica se existe comunicação com o Arduino
        if not self.comunicacao_controller.model.is_connected:
            if not self.protecao_comunicacao_indisponivel:
                logger.error(
                    "Proteção automática detectou condição, mas a comunicação "
                    "com o Arduino está desconectada. Corte físico indisponível."
                )

            self.protecao_comunicacao_indisponivel = True
            return

        # Registra a recuperação da comunicação
        if self.protecao_comunicacao_indisponivel:
            logger.info(
                "Comunicação com o Arduino restabelecida. "
                "Proteção automática voltou a operar."
            )
            self.protecao_comunicacao_indisponivel = False

        # Guarda a medição que provocou o disparo
        self.medicao_disparo = self.medicao_atual

        logger.warning(
            "Sobrecorrente severa detectada: potência medida=%.1f W, "
            "limite configurado=%.1f W, fator=%.1f, "
            "limite de disparo=%.1f W",
            self.medicao_disparo.potencia,
            limite,
            self.fator_sobrecorrente,
            limite * self.fator_sobrecorrente
        )

        # Prepara a ação que será concluída somente após confirmação do Arduino
        acao = {
            "aberto": True,
            "status_esperado": 0,
            "tipo": "Alerta",
            "descricao": (
                "Corte automático por sobrecorrente severa."
            ),
            "automatico": True
        }

        # Bloqueia novas tentativas automáticas repetidas
        self.protecao_sobrecorrente_disparada = True

        # Solicita a abertura física do relé
        enviado = self.solicitar_acao_rele(acao, "!0")

        if not enviado:
            logger.error(
                "Proteção automática detectada, mas o comando de abertura "
                "do relé não foi enviado."
            )
            return

    def verificar_eventos(self):
        # Verifica se aconteceu alguma mudança relevante
        medicao = self.medicao_atual

        if medicao is None or medicao.potencia is None:
            return
        # Não avalia limite de potência com o relé aberto
        if not medicao.disjuntor:
            self.limite_ultrapassado = False
            self.ui.lbl_valor_potencia.setStyleSheet(
                "font-weight: bold;"
            )
            return

        # Usa somente o limite efetivamente aplicado.
        limite = self.limite_potencia_aplicado

        ultrapassou_limite = (
            medicao.potencia > limite
        )

        # Atualiza a indicação visual do limite
        if ultrapassou_limite:
            self.ui.lbl_valor_potencia.setStyleSheet(
                "color: #D64545; font-weight: bold;"
            )
        else:
            self.ui.lbl_valor_potencia.setStyleSheet(
                "font-weight: bold;"
            )

                # Registra somente quando entra na condição de alerta
        if (
            ultrapassou_limite  
            and not self.limite_ultrapassado
        ):
            logger.warning(
                "Limite de potência ultrapassado: %.1f W "
                "(Limite configurado: %.1f W).",
                medicao.potencia,
                limite
            )
                        
            self.adicionar_registro(
                tipo="Alerta",
                descricao="Limite de potência ultrapassado.",
                valor=self.formatar_medicao()
            )

        self.limite_ultrapassado = ultrapassou_limite

    def adicionar_registro(
        self,
        tipo,
        descricao,
        valor
    ):
        # Cria objeto Registro c/ infos recebidas
        registro = Registro(
            tipo=tipo,
            descricao=descricao,
            valor=valor
        )
        
        try:
            id_registro = RegistroRepository.inserir(registro)
        except Exception as erro:
            logger.exception(
                "Falha ao persistir evento no SQLite. "
                "Tipo=%s, descrição=%s, motivo=%s",
                tipo,
                descricao,
                erro
            )

            QMessageBox.critical(
                self,
                "Erro ao salvar evento",
                (
                    "Não foi possível salvar o evento no banco de dados.\n\n"
                    f"Detalhes: {erro}"
                )
            )
            return
        
        # Adiciona o id retornado pelo banco ao objeto do evento
        registro.id = id_registro
        # Insere evento no início da lista em memória, com eventos +recentes antes
        self.registros.insert(0, registro)
        # Att a tabela de histórico
        self.atualizar_tabela()

    def carregar_registros(self):
        registros_banco = RegistroRepository.listar_todos()
        # Limpa a lista em memória antes de carregar os registros
        self.registros = []

        for item in registros_banco:
            # Cria um objeto Registro com os dados recuperados
            registro = Registro(
                tipo=item["tipo_evento"],
                descricao=item["descricao"],
                valor=item["valor_medido"]
            )
            # Converte texto ISO p/ objeto datetime
            registro.timestamp = datetime.fromisoformat(
                item["data_hora"]
            )
            # Adiciona o evento à lista em memória
            self.registros.append(registro)

    def atualizar_tabela(self):
        # Atualiza a tabela respeitando o filtro, se estiver ativo

        if self.filtro_data_ativo:
            data_inicio = self.ui.data_inicio.date().toPython()
            data_fim = self.ui.data_fim.date().toPython()

            registros_exibidos = [
                registro
                for registro in self.registros
                if data_inicio <= registro.timestamp.date() <= data_fim
            ]
        else:
            registros_exibidos = self.registros

        # Atualiza a tabela de uma vez, evitando efeito visual de "piscar"
        self.ui.tabela_registros.setUpdatesEnabled(False)
        self.ui.tabela_registros.setRowCount(0)

        for registro in registros_exibidos:
            linha = 0

            self.ui.tabela_registros.insertRow(
                linha
            )

            # Data e hora
            self.ui.tabela_registros.setItem(
                linha,
                0,
                QTableWidgetItem(
                    registro.timestamp.strftime(
                        "%d/%m/%Y %H:%M:%S"
                    )
                )
            )

            # Tipo
            self.ui.tabela_registros.setItem(
                linha,
                1,
                QTableWidgetItem(
                    registro.tipo
                )
            )

            # Valor medido
            self.ui.tabela_registros.setItem(
                linha,
                2,
                QTableWidgetItem(
                    registro.valor
                )
            )

            # Descrição
            self.ui.tabela_registros.setItem(
                linha,
                3,
                QTableWidgetItem(
                    registro.descricao
                )
            )

        self.ui.tabela_registros.setUpdatesEnabled(True)
        self.ui.tabela_registros.viewport().update()

    def configurar_tabela(self):
        # Configura o tamanho das colunas da tabela

        # Define tamanhos iniciais das colunas da tabela de auditoria
        self.ui.tabela_registros.setColumnWidth(0, 200)
        self.ui.tabela_registros.setColumnWidth(1, 120)
        self.ui.tabela_registros.setColumnWidth(2, 200)

        # Faz a descrição ocupar o espaço restante e evitar espaço vazio que estava aparecendo
        self.ui.tabela_registros.horizontalHeader().setStretchLastSection(True)

        # Para evitar um espaço vazio que estava aparecendo à direita
        self.ui.tabela_registros.horizontalHeader().setStretchLastSection(True)

    def filtrar_historico_por_data(self):
        # Filtra a tabela por intervalo de datas selecionado
        
        data_inicio = self.ui.data_inicio.date().toPython()
        data_fim = self.ui.data_fim.date().toPython()
        
        # Impede intervalo inválido
        if data_inicio > data_fim:
            QMessageBox.warning(
                self,
                "Filtro inválido",
                "A data inicial não pode ser maior que a data final."
            )
            return

        self.filtro_data_ativo = True

        # Atualiza a tabela usando o filtro
        self.atualizar_tabela()

    def limpar_filtro_data(self):
        # Remove o filtro
        self.filtro_data_ativo = False

        # Volta as datas para o dia atual
        hoje = QDate.currentDate()
        self.ui.data_inicio.setDate(hoje)
        self.ui.data_fim.setDate(hoje)

        # Mostra novamente todos os registros
        self.atualizar_tabela()

    def formatar_medicao(self):
        # Conf se existe telemetria disponível
        if self.dados_serial_atual is None:
            return "Sem telemetria disponível"

        dados = self.dados_serial_atual

        return (
            f"A0: {dados['a0']} | "
            f"A1: {dados['a1']} | "
            f"Relé: {dados['status_rele']} | "
            f"Botão: {dados['status_botao']}"
        )

    def formatar_medicao_customizada(self, medicao):
        # Formata uma medição específica (não necessariamente a atual)
        return (
            f"{medicao.tensao:.1f} V / "
            f"{medicao.corrente:.1f} A / "
            f"{medicao.potencia:.1f} W"
        )

    def abrir_comunicacao(self):
        # Exibe a janela de comunicação serial e, ao fechar,
        # reflete o estado da conexão no badge do cabeçalho
        self.comunicacao_controller.exec()

        conectado = self.comunicacao_controller.model.is_connected

        if conectado:
            self.ui.lbl_status_comunicacao.setText(
                "●  " + self.comunicacao_controller.model.obter_status()
            )
        else:
            self.ui.lbl_status_comunicacao.setText(
                "●  Comunicação: Desconectado"
            )

        self.ui.lbl_status_comunicacao.setProperty(
            "state", "on" if conectado else "off"
        )
        self.ui.lbl_status_comunicacao.style().unpolish(self.ui.lbl_status_comunicacao)
        self.ui.lbl_status_comunicacao.style().polish(self.ui.lbl_status_comunicacao)

    def abrir_configuracao(self):
        # Exibe a janela modal de configuração de limites (tensão / corrente)
        # Passa o modelo compartilhado para manter os valores do último acesso
        dialogo = ConfiguracaoController(self, model=self.model_config)

        if dialogo.exec() == dialogo.DialogCode.Accepted:
            # Resgata o limite de potência calculado (P = V x I) e aplica no dashboard
            novo_limite = self.model_config.lim_potencia

            self.ui.spin_limite_potencia.setValue(novo_limite)

            # O OK da configuração aplica efetivamente o novo limite.
            self.limite_potencia_aplicado = novo_limite
            self.limite_potencia_pendente = False

            # Rearma a proteção após alteração confirmada do limite,
            # somente se o relé estiver fisicamente fechado.
            if (
                self.medicao_atual is not None
                and self.medicao_atual.disjuntor
                and self.acao_rele_pendente is None
            ):
                self.protecao_sobrecorrente_disparada = False
                self.medicao_disparo = None
                self.amostras_sobrecorrente = 0

            self.ui.spin_limite_potencia.setStyleSheet("")

            self.adicionar_registro(
                tipo="Comando",
                descricao=(
                    f"Limites atualizados: {self.model_config.lim_tensao:.1f} V / "
                    f"{self.model_config.lim_corrente:.1f} A"
                ),
                valor=f"{novo_limite:.1f} W"
            )

    def confirmar_limite_potencia(self):
        # Confirma o limite digitado no spin da dashboard.
        novo_limite = self.ui.spin_limite_potencia.value()

        # Salva e valida antes de aplicar o limite
        try:
            sucesso = self.model_config.atualizar_limite_potencia_manual(
                novo_limite
            )
            if not sucesso:
                logger.warning(
                    "Tentativa de configurar limite de potência inválido: %s",
                    novo_limite
                )
                
                QMessageBox.warning(
                    self,
                    "Limite inválido",
                    "Informe um limite de potência válido e não negativo."
                )
                return
        except Exception:
            logger.exception("Erro ao salvar o limite de potência")
            QMessageBox.critical(
                self,
                "Erro ao salvar",
                "Não foi possível salvar o limite de potência."
            )
            return
        
        # Aplica o limite somente depois de salvar com sucesso
        novo_limite = 0.0 if novo_limite == 0 else novo_limite
        # Valor passa a valer para a proteção e para os alertas
        self.limite_potencia_aplicado = novo_limite
        self.limite_potencia_pendente = False

        # Rearma a proteção após alteração confirmada do limite,
        # somente se o relé estiver fisicamente fechado
        if (
            self.medicao_atual is not None
            and self.medicao_atual.disjuntor
            and self.acao_rele_pendente is None
        ):
            self.protecao_sobrecorrente_disparada = False
            self.medicao_disparo = None
            self.amostras_sobrecorrente = 0

        self.ui.spin_limite_potencia.setValue(novo_limite)
        # Volta a cor normal depois da confirmação.
        self.ui.spin_limite_potencia.setStyleSheet("")

        # Att o estado de ultrapassagem somente com medição disponível
        if self.medicao_atual is not None:
            self.limite_ultrapassado = (
                self.medicao_atual.potencia
                > self.limite_potencia_aplicado
            )
        else:
            self.limite_ultrapassado = False
        self.verificar_limite()

        self.adicionar_registro(
            tipo="Comando",
            descricao="Limite de potência alterado manualmente na dashboard.",
            valor=f"{novo_limite:.1f} W"
        )

    # closeEvent = método definido pelo Qt, NÃO pode mudar nomeação
    def closeEvent(self, event):
        # Encerra a comunicação serial antes de destruir a janela
        if (
            self.comunicacao_controller.model.is_connected
            or (
                self.comunicacao_controller.leitura_serial
                and self.comunicacao_controller.leitura_serial.isRunning()
            )
        ):
            self.comunicacao_controller.ao_desconectar()
        # Permite que a janela seja fechada após o encerramento da comunicação
        event.accept()

    # Recebe dados interpretados enviados pelo controller de comunicação
    def ao_receber_dados_serial(self, dados: dict):
        # Registra os dados recebidos no log
        logger.debug("Dados recebidos na dashboard: %s", dados)

        # Conf se todos os campos esperados foram recebidos
        campos_necessarios = {
            "a0",
            "a1",
            "status_botao",
            "status_rele"
        }

        if not campos_necessarios.issubset(dados.keys()):
            logger.warning("Dados serial recebidos incompletos: %s", dados)
            return

        # Converte o estado do relé para inteiro
        try:
            status_rele = int(dados["status_rele"])
        except (ValueError, TypeError):
            logger.warning("Estado do relé inválido recebido: %s", dados)
            return

        if status_rele not in (0, 1):
            logger.warning("Estado do relé fora do padrão: %s", status_rele)
            return

        # Converte o estado recebido para o estado lógico do sistema
        rele_ligado = status_rele == 1

        # Guarda os dados recebidos do Arduino para usar na dash
        self.dados_serial_atual = dados

        # Converte os dados brutos em uma medição elétrica
        try:
            self.medicao_atual = Medicao.a_partir_dos_dados_brutos(
                adc_tensao=dados["a0"],
                adc_corrente=dados["a1"],
                disjuntor=rele_ligado
            )
        except (ValueError, TypeError, KeyError) as erro:
            self.medicao_atual = None
            logger.warning("Falha ao processar medição elétrica: %s", erro)

        # Registra dados para o gráfico e o histórico, inclusive com o relé aberto
        # A comunicação serial continua ativa mesmo com o sistema cortado
        try:
            self.registrar_telemetria_bruta(dados, rele_ligado)
        except (ValueError, TypeError, KeyError) as erro:
            logger.warning(
                "Falha ao registrar telemetria bruta: %s",
                erro
            )

        # Verifica se existe uma operação aguardando confirmação
        if self.acao_rele_pendente is not None:
            acao = self.acao_rele_pendente

            # Aguarda a telemetria apresentar o estado solicitado
            if status_rele != acao["status_esperado"]:
                return

            # Cancela o timeout, pois o Arduino confirmou
            self.timer_confirmacao_rele.stop()
            self.acao_rele_pendente = None

            logger.info("Comando do relé confirmado pela telemetria.")
            self.energizando_ao_conectar = False

            # Preserva a medição original do disparo automático
            valor_disparo = None

            if acao.get("automatico") and self.medicao_disparo is not None:
                valor_disparo = self.formatar_medicao_customizada(
                    self.medicao_disparo
                )

            # Registra o corte confirmado pelo hardware
            sucesso = self.executar_corte(
                aberto=acao["aberto"],
                tipo=acao["tipo"],
                descricao=acao["descricao"],
                valor_medicao=valor_disparo
            )

            # Atualiza a interface conforme o estado real informado pelo Arduino
            self.corte_emergencia_ativo = not rele_ligado
            self.disjuntor_anterior = rele_ligado

            # Rearma a proteção automática após confirmação de reativação
            if rele_ligado and not self.limite_potencia_pendente:
                self.protecao_sobrecorrente_disparada = False
                self.medicao_disparo = None
                self.amostras_sobrecorrente = 0

            if self.corte_emergencia_ativo:
                self.ui.btn_corte_emergencia.setText("▶  REATIVAR SISTEMA")
            else:
                self.ui.btn_corte_emergencia.setText("⚠  CORTE DE EMERGÊNCIA")

            self.atualizar_dashboard()

            # Popup obrigatório após confirmação física do corte automático
            if acao.get("automatico") and not rele_ligado:
                QMessageBox.warning(
                    self,
                    "Proteção Ativada",
                    (
                        "O disjuntor abriu automaticamente devido à "
                        "sobrecorrente severa.\n\n"
                        f"Medição no momento do disparo: {valor_disparo}"
                    )
                )

            # Informa caso o estado físico tenha sido confirmado,
            # mas o registro no banco tenha falhado
            if not sucesso:
                logger.error(
                    "O relé confirmou a alteração, mas o registro do evento falhou."
                )

            return

        # Verifica eventos relacionados à medição real
        if self.medicao_atual is not None:
            self.verificar_eventos()

        # Sincroniza o estado inicial com o hardware
        if self.disjuntor_anterior is None:
            self.disjuntor_anterior = rele_ligado
            self.corte_emergencia_ativo = not rele_ligado

            # Carência da proteção a partir do primeiro pacote recebido
            self.ignorar_protecao_ate = datetime.now() + timedelta(seconds=2)
            self.amostras_sobrecorrente = 0

            # Relé aberto ao conectar: tenta energizar uma única vez
            # Mostra "AGUARDANDO MEDIÇÃO" até o hardware confirmar
            if (
                not rele_ligado
                and self.energizar_ao_conectar
                and not self.tentou_energizar_ao_conectar
            ):
                self.tentou_energizar_ao_conectar = True
                self.energizando_ao_conectar = True

                logger.info(
                    "Relé aberto ao conectar. Enviando comando de energização inicial."
                )

                acao = {
                    "aberto": False,
                    "status_esperado": 1,
                    "tipo": "Status",
                    "descricao": "Sistema energizado ao iniciar a comunicação."
                }

                if not self.solicitar_acao_rele(acao, "!1"):
                    self.energizando_ao_conectar = False

            if self.corte_emergencia_ativo:
                self.ui.btn_corte_emergencia.setText("▶  REATIVAR SISTEMA")
            else:
                self.ui.btn_corte_emergencia.setText("⚠  CORTE DE EMERGÊNCIA")

            self.atualizar_dashboard()

            return

        # Detecta alterações de estado realizadas diretamente no hardware
        if rele_ligado != self.disjuntor_anterior:
            aberto = not rele_ligado

            # Identifica abertura espontânea do relé
            abertura_espontanea = (
                aberto
                and self.acao_rele_pendente is None
            )

            if abertura_espontanea:
                logger.warning(
                    "Abertura espontânea do relé detectada pelo hardware."
                )

                # Captura a medição no instante da abertura espontânea
                valor_disparo = (
                    self.formatar_medicao_customizada(self.medicao_atual)
                    if self.medicao_atual is not None
                    else "Sem medição disponível"
                )

                QMessageBox.warning(
                    self,
                    "Proteção ativada",
                    (
                        "O disjuntor foi aberto pelo hardware sem uma "
                        "solicitação do software.\n\n"
                        f"Medição no momento da abertura: {valor_disparo}\n\n"
                        "Verifique a carga e as condições do sistema."
                    )
                )

            # Registra a alteração identificada pela telemetria
            sucesso = self.executar_corte(
                aberto=aberto,
                tipo="Alerta" if aberto else "Status",
                descricao=(
                    "Relé desligado pelo hardware."
                    if aberto
                    else "Relé ligado pelo hardware."
                ),
                valor_medicao=valor_disparo if aberto else None
            )

            # Atualiza o estado conforme a telemetria, independentemente do registro
            self.disjuntor_anterior = rele_ligado
            self.corte_emergencia_ativo = aberto

            # Rearma a proteção quando o hardware fecha o relé
            if rele_ligado and not self.limite_potencia_pendente:
                self.protecao_sobrecorrente_disparada = False
                self.medicao_disparo = None
                self.amostras_sobrecorrente = 0

            if aberto:
                self.ui.btn_corte_emergencia.setText("▶  REATIVAR SISTEMA")
            else:
                self.ui.btn_corte_emergencia.setText("⚠  CORTE DE EMERGÊNCIA")

            self.atualizar_dashboard()

            if not sucesso:
                logger.error(
                    "Estado do relé atualizado, mas o evento não foi persistido."
                )

        # Verifica a proteção automática após processar a telemetria
        if self.medicao_atual is not None:
            self.verificar_protecao_sobrecorrente()

    # Registra os dados brutos recebidos do Arduino
    def registrar_telemetria_bruta(self, dados, rele_ligado=True):
        # Guarda o instante da leitura
        instante = datetime.now()

        # Converte e valida os sinais recebidos
        a0 = int(dados["a0"])
        a1 = int(dados["a1"])
        status_botao = int(dados["status_botao"])
        status_rele = int(dados["status_rele"])

        if not (0 <= a0 <= 1023 and 0 <= a1 <= 1023):
            raise ValueError("Valor ADC fora da faixa de 0 a 1023")

        if status_botao not in (0, 1):
            raise ValueError("Estado do botão inválido")

        if status_rele not in (0, 1):
            raise ValueError("Estado do relé inválido")

        # Organiza os dados recebidos
        # Com o relé aberto os sinais são registrados como 0 (curva mostra o corte)
        leitura = {
            "timestamp": instante,
            "a0": a0 if rele_ligado else 0,
            "a1": a1 if rele_ligado else 0,
            "status_botao": status_botao,
            "status_rele": status_rele
        }

        # Adiciona a leitura ao histórico
        self.historico_adc.append(leitura)

        # Mantém o histórico em memória limitado
        # Evita crescimento ilimitado durante a execução
        if len(self.historico_adc) > 1000:
            self.historico_adc.pop(0)

        # Atualiza o gráfico e os indicadores
        self.atualizar_grafico()
        self.atualizar_dashboard()