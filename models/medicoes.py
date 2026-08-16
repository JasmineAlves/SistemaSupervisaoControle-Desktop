# Dados recebidos do hardware 
# (tensão, corrente, potência, estado do disjuntor e momento da medição)

from datetime import datetime

class Medicao:
    def __init__(self, v, i, disjuntor):
        self.tensao = v
        self.corrente = i
        self.potencia = v * i
        self.disjuntor = disjuntor
        self.timestamp = datetime.now()

