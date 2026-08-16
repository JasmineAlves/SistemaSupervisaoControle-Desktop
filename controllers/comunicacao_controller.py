# Controle da comunicação com o hardware
import sys
import serial.tools.list_ports
from PySide6.QtWidgets import QWidget, QApplication
from ui.Ui_comunicacao import Ui_Form


class ComunicacaoController(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Guarda o estado atual da conexão serial
        self.is_connected = False

        # Configura as ações de clique dos botões
        self.configurar_sinais()

        # Busca e exibe as portas COM disponíveis
        self.carregar_portas_com()

        # Configura o estado inicial dos componentes da tela
        self.atualizar_interface()

    def configurar_sinais(self):
        # Conecta os botões da tela às suas respetivas funções

        self.ui.btn_conectar.clicked.connect(
            self.ao_conectar
        )

        self.ui.btn_desconectar.clicked.connect(
            self.ao_desconectar
        )

    def carregar_portas_com(self):
        # Mapeia e popula as portas COM reais no QComboBox

        self.ui.combo_porta.clear()

        portas = serial.tools.list_ports.comports()

        if portas:
            for porta in portas:
                self.ui.combo_porta.addItem(porta.device)
        else:
            self.ui.combo_porta.addItem("Nenhuma porta encontrada")

    def ao_conectar(self):
        # Trata o evento de conexão na etapa A1/1

        # Valida se existe uma porta válida selecionada
        if self.ui.combo_porta.currentText() == "Nenhuma porta encontrada":
            self.ui.lbl_status.setText(
                "Status : Erro - Nenhuma porta selecionada"
            )
            return

        # Captura os valores informados no painel
        porta = self.ui.combo_porta.currentText()
        baud_rate = self.ui.combo_baud.currentText()
        timeout = self.ui.spin_timeout.value()

        # Atualiza o estado visual para conectado
        self.is_connected = True

        self.ui.lbl_status.setText(
            f"Status : Conectado ({porta} @ {baud_rate} bps, timeout: {timeout}s)"
        )

        # Bloqueia os seletores durante a conexão
        self.atualizar_interface()

    def ao_desconectar(self):
        # Trata o evento de desconexão na etapa A1/1

        # Atualiza o estado visual para desconectado
        self.is_connected = False

        self.ui.lbl_status.setText(
            "Status : Desconectado"
        )

        # Atualiza novamente a lista para identificar novas portas
        self.carregar_portas_com()

        # Habilita os campos de edição
        self.atualizar_interface()

    def atualizar_interface(self):
        # Habilita ou desabilita os elementos conforme o estado da conexão

        conectado = self.is_connected

        # Entradas de configuração
        self.ui.combo_porta.setEnabled(not conectado)
        self.ui.combo_baud.setEnabled(not conectado)
        self.ui.spin_timeout.setEnabled(not conectado)

        # Controle de botões
        self.ui.btn_conectar.setEnabled(not conectado)
        self.ui.btn_desconectar.setEnabled(conectado)