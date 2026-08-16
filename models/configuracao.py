# Limites/parâmetros do sistema

class  Configuracao:
    def __init__(self, lim_v, lim_i, lim_p):
        self.lim_tensao = lim_v
        self.lim_corrente = lim_i
        self.lim_potencia = lim_p