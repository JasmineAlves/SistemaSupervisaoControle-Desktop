# Registros de eventos pelo sistema

from datetime import datetime

class Registro:
    def __init__(self, tipo, descricao, valor):
        self.tipo = tipo
        self.descricao = descricao
        self.valor = valor
        self.timestamp = datetime.now()
