# Controle da configuração do sistema
from PySide6.QtWidgets import QDialog, QMessageBox
from ui.Ui_configuracoes import Ui_Dialog
from models.configuracao import Configuracao

class ConfiguracaoController(QDialog):
    def __init__(self, parent=None, model=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Instancia a classe de Configuração correta
        self.model = model if model else Configuracao()

        self.configurar_sinais()
        self.carregar_dados()

    def configurar_sinais(self):
        self.ui.btn_salvar.clicked.connect(self.ao_salvar)
        self.ui.btn_cancelar.clicked.connect(self.ao_cancelar)

        # Atualiza a prévia de potência (P = V x I) em tempo real
        self.ui.spin_tensao_max.valueChanged.connect(self.atualizar_previa_potencia)
        self.ui.spin_corrente_max.valueChanged.connect(self.atualizar_previa_potencia)

    def carregar_dados(self):
        dados = self.model.obter_parametros()
        self.ui.spin_corrente_max.setValue(dados["corrente_max"])
        self.ui.spin_tensao_max.setValue(dados["tensao_max"])
        self.atualizar_previa_potencia()

    def atualizar_previa_potencia(self):
        # Recalcula a prévia exibida sempre que tensão ou corrente mudam
        potencia = self.ui.spin_tensao_max.value() * self.ui.spin_corrente_max.value()
        self.ui.lbl_potencia_calculada.setText(f"{potencia:.1f} W")

    def ao_salvar(self):
        corrente = self.ui.spin_corrente_max.value()
        tensao = self.ui.spin_tensao_max.value()

        # Envia os dados atualizados para o Model tratar e validar
        sucesso = self.model.atualizar_limites(tensao=tensao, corrente=corrente)

        if sucesso:
            self.accept()
        else:
            QMessageBox.warning(
                self, 
                "Erro de Validação", 
                "Os valores de tensão e corrente devem ser maiores ou iguais a zero."
            )

    def ao_cancelar(self):
        self.reject()