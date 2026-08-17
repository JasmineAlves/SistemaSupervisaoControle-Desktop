from PySide6.QtWidgets import QDialog
from ui.Ui_comunicacao import Ui_Form
from models.comunicacao import ComunicacaoModel


class ComunicacaoController(QDialog):
    def __init__(self, parent=None, model=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.model = model if model else ComunicacaoModel()

        self.configurar_sinais()
        self.carregar_portas_com()
        self.atualizar_interface()

    def configurar_sinais(self):
        self.ui.btn_conectar.clicked.connect(self.ao_conectar)
        self.ui.btn_desconectar.clicked.connect(self.ao_desconectar)
        self.ui.btn_fechar.clicked.connect(self.close)

    def carregar_portas_com(self):
        self.ui.combo_porta.clear()
        
        portas = self.model.listar_portas()

        if portas:
            self.ui.combo_porta.addItems(portas)
        else:
            self.ui.combo_porta.addItem("Nenhuma porta encontrada")

    def ao_conectar(self):
        porta = self.ui.combo_porta.currentText()
        baud_rate = self.ui.combo_baud.currentText()
        timeout = self.ui.spin_timeout.value()

        sucesso = self.model.conectar(porta, baud_rate, timeout)

        if sucesso:
            self.atualizar_status(self.model.obter_status(), conectado=True)
            self.atualizar_interface()
        else:
            self.atualizar_status("Status : Erro - Nenhuma porta selecionada", conectado=False)

    def ao_desconectar(self):
        self.model.desconectar()

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