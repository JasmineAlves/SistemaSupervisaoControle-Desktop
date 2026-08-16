# Controle da supervisão do sistema

from datetime import datetime, timedelta # data/hora e intervalo de tempo
import pyqtgraph as pg # desenhar gráficos
from PySide6.QtCore import QTimer # Executa função a cada certo período
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox # Base da janela principal e texto dentro das células da tabela
from ui.Ui_dashboard import Ui_MainWindow # Interface criada pelo Qt Designer
from models.medicao import Medicao # Medições
from models.registro import Registro # Evento registrado no sistema
from models.simulacao import Simulador

# Classe principal
class DashController(QMainWindow):
    def __init__(self):
        super().__init__()

        # Carregando a interface
        self.ui = Ui_MainWindow() # Objeto que representa a interface
        self.ui.setupUi(self) # Coloca a interface dentro da janela
        # Passa a ter acesso aos componentes

        # Faz a simulação de uma medição inicial
        self.medicao_atual = Medicao(
            v=220.0,
            i=8.0,
            disjuntor=True # Fechado 
        )

        self.simulador = Simulador()

        # Guarda as medições utilizadas no gráfico
        self.historico_potencia = []

        # Guarda os registros de eventos do sistema
        self.registros = []

        # Guarda o estado anterior do disjuntor
        self.disjuntor_anterior = self.medicao_atual.disjuntor

        # Guarda se o limite de potência já foi ultrapassado
        # Se a potência estava anteriormente acima do limite, evita registrar alerta a cada segundo
        self.limite_ultrapassado = False

        # Configura o gráfico, chama a função que cria o gráfico
        self.configurar_grafico()

        # Carrega dados iniciais para o gráfico, cria dados simulados
        self.carregar_historico_inicial()

        # Configura a tabela de registros, define tamanho das colunas
        self.configurar_tabela()

        # Registra a inicialização do sistema, adiciona primeiro registro
        self.adicionar_registro(
            tipo="Status",
            descricao="Sistema de supervisão iniciado.",
            valor=self.formatar_medicao()
        )

        # Temporizador que atualiza periodicamente, timer dispara a função atualizar_medicao() é executada
        self.timer = QTimer()

        self.timer.timeout.connect(
            self.atualizar_medicao
        )

        # Medição inicial
        self.atualizar_dashboard()

        # Att a telemetria a cada 1s
        self.timer.start(1000)

        # Guarda o estado do corte de emergência
        self.corte_emergencia_ativo = False
        # Controla o corte de emergência
        self.ui.btn_corte_emergencia.clicked.connect(
            self.alternar_corte_emergencia
        )

        # Guarda o limite anterior para registrar alterações
        self.limite_anterior = self.ui.spin_limite_potencia.value()

        # Verifica o limite quando ele é alterado
        self.ui.spin_limite_potencia.valueChanged.connect(
            self.verificar_limite
        )

    def alternar_corte_emergencia(self):
        # Confirma o corte ou a reativação do sistema

        if not self.corte_emergencia_ativo:

            resposta = QMessageBox.question(
                self,
                "Corte de emergência",
                "Deseja realizar o corte de emergência?"
            )

            if resposta == QMessageBox.StandardButton.Yes:

                # Atualiza o estado do disjuntor no simulador
                self.simulador.alterar_disjuntor(False)

                # Atualiza o estado do corte
                self.corte_emergencia_ativo = True

                # Registra o corte
                self.adicionar_registro(
                    tipo="Alerta",
                    descricao="Corte de emergência acionado.",
                    valor=self.formatar_medicao()
                )

                # Atualiza a interface
                self.atualizar_dashboard()

                # Altera o texto do botão
                self.ui.btn_corte_emergencia.setText(
                    "▶  REATIVAR SISTEMA"
                )

        else:

            resposta = QMessageBox.question(
                self,
                "Reativar sistema",
                "Deseja reativar o sistema?"
            )

            if resposta == QMessageBox.StandardButton.Yes:

                # Religa o estado do disjuntor no simulador
                self.simulador.alterar_disjuntor(True)

                # Atualiza o estado do corte
                self.corte_emergencia_ativo = False

                # Registra a reativação
                self.adicionar_registro(
                    tipo="Status",
                    descricao="Sistema reativado após corte de emergência.",
                    valor=self.formatar_medicao()
                )

                # Atualiza a interface
                self.atualizar_dashboard()

                # Altera o texto do botão
                self.ui.btn_corte_emergencia.setText(
                    "⚠  CORTE DE EMERGÊNCIA"
                )    

    # Cria e configura gráfico
    def configurar_grafico(self):
        # Cria o gráfico de demanda de potência

        self.grafico = pg.PlotWidget()

        self.grafico.setBackground("w")

        self.grafico.setTitle(
            "Demanda de potência",
            color="#24343B",
            size="12pt"
        )

        self.grafico.setLabel(
            "left",
            "Potência",
            units="W"
        )

        self.grafico.setLabel(
            "bottom",
            "Tempo"
        )

        self.grafico.showGrid(
            x=True,
            y=True,
            alpha=0.15
        )

        self.grafico.setMinimumHeight(190)

        # Coloca o gráfico na área reservada da dashboard
        layout = self.ui.widget_grafico.layout()

        if layout is None:
            from PySide6.QtWidgets import QVBoxLayout

            layout = QVBoxLayout(
                self.ui.widget_grafico
            )

        layout.addWidget(self.grafico)

        # Cria a curva de potência
        self.curva_potencia = self.grafico.plot(
            pen=pg.mkPen(
                color="#245A63",
                width=2
            )
        )

    def carregar_historico_inicial(self):
        # Cria dados simulados das últimas 24 horas

        agora = datetime.now()

        quantidade_pontos = 48 # 24horas / 48pontos = 0,5 hora cada ponto

        for indice in range(quantidade_pontos):
            # Horário de cada ponto distribuido
            momento = agora - timedelta(
                hours=24 - (indice * 0.5)
            )

            # Gera uma nova medição simulada com base no estado atual do disjuntor
            medicao = self.simulador.gerar_medicao()

            # Obtém a potência calculada da medição simulada
            potencia = medicao.potencia

            # Adiciona um dicionário na lista
            self.historico_potencia.append(
                {
                    "timestamp": momento,
                    "potencia": potencia
                }
            )

        # Att o gráfico com os dados iniciais
        self.atualizar_grafico()

    def atualizar_grafico(self):
        # Att a curva de demanda de potência
        # Pega o histórico e transforma em dados para o gráfico
        valores = [
            item["potencia"]
            for item in self.historico_potencia
        ]

        tempos = list(
            range(len(valores))
        )
        # Desenha o gráfico usando esses pontos
        self.curva_potencia.setData(
            tempos,
            valores
        )

    # Chegada de uma nova simulação
    def atualizar_medicao(self):
        # Simula uma nova medição recebida, como se fosse um hardware

        # Gera uma nova medição simulada
        self.medicao_atual = self.simulador.gerar_medicao()

        # Adiciona a nova potência ao histórico
        self.historico_potencia.append(
            {
                "timestamp": self.medicao_atual.timestamp,
                "potencia": self.medicao_atual.potencia
            }
        )

        # Limita a quantidade de pontos armazenados
        if len(self.historico_potencia) > 1000:
            self.historico_potencia.pop(0)

        # Verifica se aconteceu algum evento
        self.verificar_eventos()

        # Atualiza os dados da interface
        self.atualizar_dashboard()

        # Atualiza o gráfico
        self.atualizar_grafico()

    def atualizar_dashboard(self):
        # Exibe na interface oq veio da medição
        
        # Coloca os valores na interface, tensão, corrente, potência e estado disjuntor
        medicao = self.medicao_atual

        # Att tensão
        self.ui.lbl_valor_tensao.setText(
            f"{medicao.tensao:.1f}"
        )

        # Att corrente
        self.ui.lbl_valor_corrente.setText(
            f"{medicao.corrente:.1f}"
        )

        # Att potência
        self.ui.lbl_valor_potencia.setText(
            f"{medicao.potencia:.1f}"
        )

        # Atualiza estado do disjuntor
        if medicao.disjuntor: # Se True
            self.ui.lbl_status_disjuntor.setText( 
                "FECHADO / NORMAL"
            )

            self.ui.lbl_status_detalhe.setText(
                "Instalação energizada e proteção disponível."
            )

        else: # Se False
            self.ui.lbl_status_disjuntor.setText(
                "ABERTO / PROTEÇÃO ATIVADA"
            )

            self.ui.lbl_status_detalhe.setText(
                "A instalação encontra-se desenergizada."
            )

        # Atualiza o horário da última medição
        horario = medicao.timestamp.strftime(
            "%H:%M:%S"
        )

        self.ui.lbl_status_atualizacao.setText(
            f"Última atualização: {horario}"
        )

    def verificar_limite(self):
        # Verifica o limite usando a medição atual

        limite = self.ui.spin_limite_potencia.value()

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


    def verificar_eventos(self):
        # Verifica se aconteceu alguma mudança relevante

        medicao = self.medicao_atual

        # Verifica mudança no estado do disjuntor
        if medicao.disjuntor != self.disjuntor_anterior:

            if medicao.disjuntor:
                self.adicionar_registro(
                    tipo="Status",
                    descricao="Disjuntor retornou ao estado normal.",
                    valor=self.formatar_medicao()
                )

            else:
                self.adicionar_registro(
                    tipo="Alerta",
                    descricao="Disjuntor aberto / proteção ativada.",
                    valor=self.formatar_medicao()
                )

            self.disjuntor_anterior = medicao.disjuntor

        # Pega o limite configurado na interface
        limite = self.ui.spin_limite_potencia.value()

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
        # Cria um novo registro de evento

        registro = Registro(
            tipo=tipo,
            descricao=descricao,
            valor=valor
        )

        self.registros.append(registro)

        # Att a tabela de histórico
        self.atualizar_tabela()

    def atualizar_tabela(self):
        # Att a tabela com os registros do sistema

        self.ui.tabela_registros.setRowCount(0)

        for registro in self.registros:

            # Para registros ocorrerem em ordem decrescente
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

    def formatar_medicao(self):
        # Formata a medição para mostrar nos registros

        return (
            f"{self.medicao_atual.tensao:.1f} V / "
            f"{self.medicao_atual.corrente:.1f} A / "
            f"{self.medicao_atual.potencia:.1f} W"
        )