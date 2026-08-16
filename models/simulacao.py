# Simulação das medições do sistema
import random  # Simular valores do hardware
from models.medicao import Medicao

class Simulador:

    def __init__(self):
        # Define o disjuntor inicialmente como fechado
        self.disjuntor = True

    def gerar_medicao(self):
        # Gera uma nova medição simulada

        if self.disjuntor:
            # Simula tensão e corrente com o disjuntor fechado
            tensao = random.uniform(218.0, 222.0)
            corrente = random.uniform(7.0, 10.0)

        else:
            # Simula a instalação desenergizada
            tensao = 0.0
            corrente = 0.0

        # Cria e retorna uma nova medição
        return Medicao(
            v=tensao,
            i=corrente,
            disjuntor=self.disjuntor
        )

    def alterar_disjuntor(self, estado):
        # Atualiza o estado simulado do disjuntor
        self.disjuntor = estado