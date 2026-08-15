# Controle da supervisão do sistema

from models.medicao import Medicao
from models.configuracao import Configuracao
from models.evento import Evento


class SupervisaoController:
    def __init__(self, configuracao):
        self.configuracao = configuracao
        self.medicao_atual = None
        self.eventos = []