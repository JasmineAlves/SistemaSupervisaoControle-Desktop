# Limites/parâmetros do sistema
import json
import os

class Configuracao:

    _ARQUIVO = "config/parametros.json"

    def __init__(self, lim_v=0.0, lim_i=0.0, lim_p=0.0):
        self.lim_tensao = lim_v
        self.lim_corrente = lim_i
        self.lim_potencia = lim_p
        self.foi_alterado_manualmente = False
        self._carregar()

    def atualizar_limites(self, tensao: float, corrente: float) -> bool:
        """Valida e atualiza os limites de operação."""
        if tensao < 0 or corrente < 0:
            return False

        self.lim_tensao = tensao
        self.lim_corrente = corrente
        self.lim_potencia = self.lim_tensao * self.lim_corrente
        self.foi_alterado_manualmente = False
        self._salvar()
        return True

    def atualizar_limite_potencia_manual(self, potencia: float) -> bool:
        """Atualiza o limite de potência diretamente pela dash (entrada manual)."""
        if potencia < 0:
            return False
        self.lim_potencia = potencia
        self.foi_alterado_manualmente = True
        self._salvar()
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
        self.foi_alterado_manualmente = False
        self._salvar()

    def _salvar(self):
        try:
            os.makedirs("config", exist_ok=True)
            with open(self._ARQUIVO, "w", encoding="utf-8") as f:
                json.dump({
                    "lim_tensao": self.lim_tensao,
                    "lim_corrente": self.lim_corrente,
                    "lim_potencia": self.lim_potencia,
                    "foi_alterado_manualmente": self.foi_alterado_manualmente
                }, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")

    def _carregar(self):
        try:
            if os.path.exists(self._ARQUIVO):
                with open(self._ARQUIVO, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                self.lim_tensao = dados.get("lim_tensao", self.lim_tensao)
                self.lim_corrente = dados.get("lim_corrente", self.lim_corrente)
                self.lim_potencia = dados.get("lim_potencia", self.lim_potencia)
                self.foi_alterado_manualmente = dados.get("foi_alterado_manualmente", False)
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
