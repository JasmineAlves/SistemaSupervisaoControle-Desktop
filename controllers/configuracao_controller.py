# Controle da configuração do sistema
import logging
from PySide6.QtWidgets import QDialog, QMessageBox
from ui.Ui_configuracoes import Ui_Dialog
from models.configuracao import Configuracao

logger = logging.getLogger(__name__)

class ConfiguracaoController(QDialog):
    def __init__(self, parent=None, model=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Impede a entrada de limites negativos
        self.ui.spin_tensao_max.setMinimum(0.0)
        self.ui.spin_corrente_max.setMinimum(0.0)

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

        # Avisa se o limite de potência foi alterado manualmente pela dash
        if self.model.foi_alterado_manualmente:
            self.ui.lbl_aviso_manual.setText(
                "Limite alterado manualmente na dashboard. Salvar irá recalcular por V × I configurados."
            )
        else:
            self.ui.lbl_aviso_manual.setText("")

    def atualizar_previa_potencia(self):
        # Recalcula a prévia exibida sempre que tensão ou corrente mudam
        potencia = self.ui.spin_tensao_max.value() * self.ui.spin_corrente_max.value()
        self.ui.lbl_potencia_calculada.setText(f"{potencia:.1f} W")

    def ao_salvar(self):
        corrente = self.ui.spin_corrente_max.value()
        tensao = self.ui.spin_tensao_max.value()

        # Valida limites
        if tensao < 0 or corrente < 0:
            QMessageBox.warning(
                self,
                "Erro de validação",
                "Os valores de tensão e corrente devem ser maiores ou iguais a zero."
            )
            return

        try:
            # Salva os limites pelo modelo
            sucesso = self.model.atualizar_limites(
                tensao=tensao,
                corrente=corrente
            )
            if sucesso:
                self.accept()
            else:
                QMessageBox.warning(
                    self,
                    "Erro de validação",
                    "Não foi possível salvar os limites informados."
                )
        except Exception:
            # Registra a falha e informa o usuário
            logger.exception("Erro ao salvar os limites de segurança")
            QMessageBox.critical(
                self,
                "Erro ao salvar",
                "Não foi possível salvar os limites. Verifique o log para mais detalhes."
            )

    def ao_cancelar(self):
        self.reject()