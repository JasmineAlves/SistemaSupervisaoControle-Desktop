import logging
from ui.Ui_comunicacao import Ui_Form
from models.comunicacao import ComunicacaoModel
from PySide6.QtWidgets import QDialog, QMessageBox
from models.leitura_serial import LeituraSerial
from PySide6.QtCore import QTimer, Signal

logger = logging.getLogger(__name__)

class ComunicacaoController(QDialog):
    # Cria signal p/ enviar dados interpretados pra outros controllers
    dados_serial_recebidos = Signal(dict)
    # Emitido quando a leitura serial falha inesperadamente (ex.: cabo/USB
    # desconectado), pra outros controllers registrarem o evento
    erro_comunicacao = Signal(str)

    def __init__(self, parent=None, model=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.model = model if model else ComunicacaoModel()
        # Inicializa thread de leitura serial
        self.leitura_serial = None
        # Controla se inicialização da comunicação foi confirmada
        self.inicializacao_confirmada = False
        self.placa_pronta = False
        # Controla o tempo de espera pela confirmação do Arduino
        self.timer_ack = QTimer(self)
        self.timer_ack.setSingleShot(True)
        self.timer_ack.timeout.connect(self.ao_timeout_inicializacao)

        self.timer_placa_pronta = QTimer(self)
        self.timer_placa_pronta.setSingleShot(True)
        self.timer_placa_pronta.timeout.connect(self.ao_timeout_placa_pronta)

        self.configurar_sinais()
        self.carregar_portas_com()
        self.carregar_configuracao_salva()
        self.atualizar_interface()

    def configurar_sinais(self):
        self.ui.btn_conectar.clicked.connect(self.ao_conectar)
        self.ui.btn_desconectar.clicked.connect(self.ao_desconectar)
        self.ui.btn_fechar.clicked.connect(self.close)

    # showEvent = método definido pelo Qt, NÃO pode mudar nomeação
    def showEvent(self, event):
        super().showEvent(event)

        # Reconsulta as portas disponíveis sempre que a tela é aberta - sem
        # isso, a lista só era atualizada na primeira abertura e após uma
        # desconexão, então uma porta reconectada com a tela já fechada
        # (ex.: usuário fechou o aviso de erro antes de reabrir) não aparecia
        porta_atual = self.ui.combo_porta.currentText()
        self.carregar_portas_com()

        indice = self.ui.combo_porta.findText(porta_atual)
        if indice >= 0:
            self.ui.combo_porta.setCurrentIndex(indice)

    def carregar_portas_com(self):
        self.ui.combo_porta.clear()

        # portas = [] > usada pra testar ausência de portas
        portas = self.model.listar_portas()

        if portas:
            self.ui.combo_porta.addItems(portas)
        else:
            self.ui.combo_porta.addItem("Nenhuma porta encontrada")

    def ao_conectar(self):
        porta = self.ui.combo_porta.currentText()
        baud_rate = self.ui.combo_baud.currentText()
        timeout = self.ui.spin_timeout.value()

        # Impede conexão sem porta valida
        if not porta or porta == "Nenhuma porta encontrada":
            QMessageBox.warning(
                self,
                "Porta inválida",
                "Selecione uma porta de comunicação válida."
            )
            return

        try:
            sucesso = self.model.conectar(porta, baud_rate, timeout)
            if sucesso:
                logger.info(
                    "Comunicação iniciada: porta=%s, baud rate=%s, timeout=%.1f s.",
                    porta,
                    baud_rate,
                    timeout
                )

                self.inicializacao_confirmada = False
                self.atualizar_status(
                    self.model.obter_status(),
                    conectado=True
                )
                self.atualizar_interface()
                # Reinicia estados de inicialização
                self.inicializacao_confirmada = False
                self.placa_pronta = False

                # Inicia thread responsável pela recepção serial
                self.iniciar_leitura_serial()

                # Aguarda arduino informar que terminou o setup
                self.timer_placa_pronta.start(5000)
            else:
                logger.warning(
                    "Falha ao estabelecer comunicação: porta=%s, baud rate=%s.",
                    porta,
                    baud_rate
                )
                QMessageBox.warning(
                    self,
                    "Falha na conexão",
                    "Não foi possível estabelecer a comunicação."
                )
                self.atualizar_status(
                    "Status: desconectado",
                    conectado=False
                )
        except Exception:
            logger.exception("Erro ao conectar à porta de comunicação")
            QMessageBox.critical(
                self,
                "Erro de comunicação",
                "Ocorreu um erro ao tentar conectar. Consulte o log."
            )

    def ao_desconectar(self):
        # Cancela temporizadores de inicialização
        self.timer_ack.stop()
        self.timer_placa_pronta.stop()
        # Reinicia estados da inicialização
        self.inicializacao_confirmada = False
        self.placa_pronta = False

        # Interrompe thread de leitura antes de fechar a comunicação
        if self.leitura_serial and self.leitura_serial.isRunning():
            self.leitura_serial.requestInterruption()
            self.leitura_serial.wait()

        # Libera a thread parada (uma nova é criada a cada reconexão em
        # iniciar_leitura_serial) - encerramento cooperativo completo
        if self.leitura_serial:
            self.leitura_serial.deleteLater()
            self.leitura_serial = None

        # Faz desconexão da comunicação serial
        self.model.desconectar()
        logger.info("Comunicação desconectada.")

        self.atualizar_status(self.model.obter_status(), conectado=False)
        self.carregar_portas_com()
        self.atualizar_interface()

    def atualizar_status(self, texto, conectado):
        # Atualiza o texto e o estado visual (badge) do card de status
        self.ui.lbl_status.setText(texto)

        estado = "conectado" if conectado else "desconectado"

        self.ui.statusCard.setProperty("estado", estado)
        self.ui.lbl_status.setProperty("estado", estado)

        for widget in (self.ui.statusCard, self.ui.lbl_status):
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def atualizar_interface(self):
        conectado = self.model.is_connected

        self.ui.combo_porta.setEnabled(not conectado)
        self.ui.combo_baud.setEnabled(not conectado)
        self.ui.spin_timeout.setEnabled(not conectado)

        self.ui.btn_conectar.setEnabled(not conectado)
        self.ui.btn_desconectar.setEnabled(conectado)

        if conectado:
            self.atualizar_status(self.model.obter_status(), conectado=True)
        else:
            self.atualizar_status(self.model.obter_status(), conectado=False)

    def carregar_configuracao_salva(self):
        # Recupera parâmetros persistidos
        parametros = self.model.configuracao.obter_configuracao_comunicacao()

        porta_salva = parametros["porta_serial"]
        baud_rate_salvo = parametros["baud_rate"]
        timeout_salvo = parametros["timeout_serial"]

        # Restaura porta selecionada
        if porta_salva:
            indice_porta = self.ui.combo_porta.findText(porta_salva)
            if indice_porta < 0:
                self.ui.combo_porta.addItem(porta_salva)
                indice_porta = self.ui.combo_porta.findText(porta_salva)

            self.ui.combo_porta.setCurrentIndex(indice_porta)

        # Restaura baudrate
        indice_baud = self.ui.combo_baud.findText(baud_rate_salvo)

        if indice_baud >= 0:
            self.ui.combo_baud.setCurrentIndex(indice_baud)
        # Restaura timeout salvo
        self.ui.spin_timeout.setValue(timeout_salvo)

    def iniciar_leitura_serial(self):
        # Conf se já existe thread de leitura executando
        if self.leitura_serial and self.leitura_serial.isRunning():
            return

        # Cria thread responsável pela leitura serial
        self.leitura_serial = LeituraSerial(self.model.conexao_serial, self)
        # Conecta signals da thread nos métodos do controller
        self.leitura_serial.dados_recebidos.connect(self.ao_receber_dados)
        self.leitura_serial.mensagem_bruta.connect(self.ao_receber_mensagem_bruta)
        self.leitura_serial.erro_leitura.connect(self.ao_ocorrer_erro_leitura)

        # Inicia a recepção de dados
        self.leitura_serial.start()

    def ao_receber_dados(self, dados: dict):
        # Recebe dados validados pelo protocolo certinho
        # OBS: não usar print() aqui - roda a cada pacote (até 200Hz) e já
        # existe o logger.debug abaixo pra diagnóstico sem o custo do print
        logger.debug("Dados serial recebidos: %s", dados)

        # Emite signal que contem os dados recebidos (isso faz com q outros controllers sejam notificados)
        self.dados_serial_recebidos.emit(dados)

    def ao_receber_mensagem_bruta(self, mensagem: str):
        # Registra mensagem original recebida
        logger.debug("Mensagem serial recebida: %s", mensagem)

        # Aguarda a placa informar que terminou a inicialização
        if not self.placa_pronta:
            if mensagem == "PLACA EM ESPERA (9600 baud)":
                self.placa_pronta = True
                self.timer_placa_pronta.stop()

                logger.info("Arduino pronto para receber comandos.")

                baud_rate = self.ui.combo_baud.currentText()
                comando = f"!S{baud_rate}"

                if self.model.enviar_comando(comando):
                    logger.info(
                        "Comando de inicialização enviado: %s",
                        comando
                    )
                    self.timer_ack.start(3000)
                else:
                    logger.error("Falha ao enviar comando de inicialização.")
                    QMessageBox.warning(
                        self,
                        "Falha na inicialização",
                        "Não foi possível enviar o comando ao Arduino."
                    )
                    self.ao_desconectar()

            return

        # Confirma inicialização após recebimento do ACK
        if not self.inicializacao_confirmada:
            baud_rate = self.ui.combo_baud.currentText()
            ack_inicializacao = f">>> ACK: INICIANDO EM {baud_rate} BPS <<<"

            if mensagem == ack_inicializacao:
                self.inicializacao_confirmada = True
                self.timer_ack.stop()

                # Altera velocidade da serial após confirmação
                sucesso = self.model.alterar_baud_rate(int(baud_rate))

                if sucesso:
                    logger.info(
                        "Inicialização confirmada. Comunicação operando em %s baud.",
                        baud_rate
                    )
                    self.atualizar_status(
                        self.model.obter_status(),
                        conectado=True
                    )
                else:
                    logger.error("Falha ao alterar baud rate após confirmação.")
                    QMessageBox.warning(
                        self,
                        "Falha na comunicação",
                        "O Arduino confirmou a inicialização, mas não foi possível alterar o baud rate."
                    )
                    self.ao_desconectar()

    def ao_timeout_inicializacao(self):
        if self.inicializacao_confirmada:
            return

        logger.error("Timeout aguardando confirmação de inicialização do Arduino.")
        QMessageBox.warning(
            self,
            "Timeout de comunicação",
            "O Arduino não confirmou a inicialização dentro do tempo esperado."
        )
        self.ao_desconectar()

    def ao_timeout_placa_pronta(self):
        if self.placa_pronta:
            return

        logger.error("Timeout aguardando inicialização do Arduino.")

        QMessageBox.warning(
            self,
            "Timeout de comunicação",
            "O Arduino não informou que estava pronto para receber comandos."
        )

        self.ao_desconectar()

    def ao_ocorrer_erro_leitura(self, erro: str):
        # Registra erro q pode acontecer na leitura
        logger.error("Erro na leitura serial: %s", erro)

        # Alerta o operador (ex.: desconexão repentina do cabo/porta) e
        # limpa o estado da conexão, já que a thread de leitura parou
        QMessageBox.warning(
            self,
            "Erro na comunicação serial",
            (
                "A leitura da porta serial foi interrompida por um erro "
                "inesperado (ex.: cabo ou porta desconectados).\n\n"
                f"Detalhes: {erro}"
            )
        )

        # Notifica outros controllers (ex.: dashboard) pra registrar o
        # evento no histórico, além do log
        self.erro_comunicacao.emit(erro)

        self.ao_desconectar()

    # closeEvent = método definido pelo Qt, NÃO pode mudar nomeação
    def closeEvent(self, event):
        # Fecha o modal de comunicação, mas comunicação vai continuar normal
        event.accept()