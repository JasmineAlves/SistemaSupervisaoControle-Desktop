# Limites/parâmetros do sistema

class Configuracao:
    def __init__(self, lim_v=0.0, lim_i=0.0, lim_p=0.0):
        self.lim_tensao = lim_v
        self.lim_corrente = lim_i
        self.lim_potencia = lim_p

    def atualizar_limites(self, tensao: float, corrente: float) -> bool:
        """Valida e atualiza os limites de operação."""
        if tensao < 0 or corrente < 0:
            return False  # Não aceita valores negativos

        self.lim_tensao = tensao
        self.lim_corrente = corrente
        
        # Calcula automaticamente o limite de potência (P = V * I)
        self.lim_potencia = self.lim_tensao * self.lim_corrente
        return True

    def obter_parametros(self) -> dict:
        """Retorna os parâmetros atuais organizados em dicionário."""
        return {
            "tensao_max": self.lim_tensao,
            "corrente_max": self.lim_corrente,
            "potencia_max": self.lim_potencia
        }

    def resetar_padrao(self):
        """Redefine os parâmetros para os valores de segurança padrão."""
        self.lim_tensao = 0.0
        self.lim_corrente = 0.0
        self.lim_potencia = 0.0