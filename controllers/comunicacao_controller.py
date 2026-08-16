from PySide6.QtWidgets import QWidget
from ui.Ui_comunicacao import Ui_Form
from models.comunicacao import ComunicacaoModel


class ComunicacaoController(QWidget):
    def __init__(self, parent=None, model=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Instancia ou recebe o model completo
        self.model = model if model else ComunicacaoModel()

        self.configurar_sinais()
        self.carregar_portas_com()
        self.atualizar_interface()

    def configurar_sinais(self):
        self.ui.btn_conectar.clicked.connect(self.ao_conectar)
        self.ui.btn_desconectar.clicked.connect(self.ao_desconectar)

    def carregar_portas_com(self):
        self.ui.combo_porta.clear()
        
        # O Model realiza a varredura do hardware
        portas = self.model.listar_portas()

        if portas:
            self.ui.combo_porta.addItems(portas)
        else:
            self.ui.combo_porta.addItem("Nenhuma porta encontrada")

    def ao_conectar(self):
        porta = self.ui.combo_porta.currentText()
        baud_rate = self.ui.combo_baud.currentText()
        timeout = self.ui.spin_timeout.value()

        # O Model processa a conexão
        sucesso = self.model.conectar(porta, baud_rate, timeout)

        if sucesso:
            self.ui.lbl_status.setText(self.model.obter_status())
            self.atualizar_interface()
        else:
            self.ui.lbl_status.setText("Status : Erro - Nenhuma porta selecionada")

    def ao_desconectar(self):
        # O Model executa o encerramento
        self.model.desconectar()
        
        self.ui.lbl_status.setText(self.model.obter_status())
        self.carregar_portas_com()
        self.atualizar_interface()

    def atualizar_interface(self):
        # O Controller apenas consulta o estado no Model
        conectado = self.model.is_connected

        self.ui.combo_porta.setEnabled(not conectado)
        self.ui.combo_baud.setEnabled(not conectado)
        self.ui.spin_timeout.setEnabled(not conectado)

        self.ui.btn_conectar.setEnabled(not conectado)
        self.ui.btn_desconectar.setEnabled(conectado)