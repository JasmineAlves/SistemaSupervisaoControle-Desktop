# Limites/parâmetros do sistema e importa logging
import json
import os
import logging
from pathlib import Path
import math

# Cria o logger do módulo
logger = logging.getLogger(__name__)

class Configuracao:

    # Mantém o arquivo de configuração na pasta data do projeto
    _ARQUIVO = str(
        Path(__file__).resolve().parent.parent / "data" / "config.json"
    )

    def __init__(self, lim_v=0.0, lim_i=0.0, lim_p=0.0):
        self.lim_tensao = lim_v
        self.lim_corrente = lim_i
        self.lim_potencia = lim_p
        self.porta_serial = ""
        self.baud_rate = "9600"
        self.timeout_serial = 1.0
        self._carregar()

    def atualizar_limites(self, tensao: float, corrente: float) -> bool:
        # Valida e atualiza os limites de operação
        if not math.isfinite(tensao) or not math.isfinite(corrente):
            return False
        if tensao < 0 or corrente < 0:
            return False

        # Normaliza zero
        tensao = 0.0 if tensao == 0 else tensao
        corrente = 0.0 if corrente == 0 else corrente

        self.lim_tensao = tensao
        self.lim_corrente = corrente
        self.lim_potencia = tensao * corrente
        self.foi_alterado_manualmente = False
        self._salvar()
        return True

    def atualizar_limite_potencia_manual(self, potencia: float) -> bool:
        # Atualiza o limite de potência diretamente pela dash (entrada manual)
        if not math.isfinite(potencia) or potencia < 0:
            return False

        # Normaliza zero
        potencia = 0.0 if potencia == 0 else potencia
        
        self.lim_potencia = potencia
        self.foi_alterado_manualmente = True
        self._salvar()
        return True

    def atualizar_configuracao_comunicacao(self, porta: str, baud_rate: str, timeout: float) -> bool:
        # Valida os parâmetros de comunicação
        if not isinstance(porta, str):
            return False
        if not isinstance(baud_rate, str) or not baud_rate.isdigit():
            return False

        try:
            timeout = float(timeout)
        except (TypeError, ValueError):
            return False

        if timeout <= 0:
            return False
        self.porta_serial = porta
        self.baud_rate = baud_rate
        self.timeout_serial = timeout
        self._salvar()
        return True

    def obter_configuracao_comunicacao(self) -> dict:
        # Retorna os parâmetros de comunicação
        return {
            "porta_serial": self.porta_serial,
            "baud_rate": self.baud_rate,
            "timeout_serial": self.timeout_serial
        }

    def obter_parametros(self) -> dict:
        #  Retorna os parâmetros atuais organizados em dicionário
        return {
            "tensao_max": self.lim_tensao,
            "corrente_max": self.lim_corrente,
            "potencia_max": self.lim_potencia
        }

    def resetar_padrao(self):
        # Redefine os parâmetros para os valores de segurança padrão
        self.lim_tensao = 0.0
        self.lim_corrente = 0.0
        self.lim_potencia = 0.0
        self.foi_alterado_manualmente = False
        self._salvar()

    def _salvar(self):
        try:
            os.makedirs(os.path.dirname(self._ARQUIVO), exist_ok=True)
            dados = {
                "lim_tensao": self.lim_tensao,
                "lim_corrente": self.lim_corrente,
                "lim_potencia": self.lim_potencia,
                "foi_alterado_manualmente": self.foi_alterado_manualmente,
                "porta_serial": self.porta_serial,
                "baud_rate": self.baud_rate,
                "timeout_serial": self.timeout_serial
            }
            with open(self._ARQUIVO, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, indent=2, ensure_ascii=False)
            logger.info("Configurações salvas com sucesso em data/config.json.")
        except (OSError, TypeError, ValueError):
            # Registra a falha ao salvar a configuração
            logger.exception("Erro ao salvar data/config.json")
            raise

    def _carregar(self):
        if not os.path.exists(self._ARQUIVO):
            self._salvar()
            return

        try:
            with open(self._ARQUIVO, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, dict):
                raise ValueError("O conteúdo do JSON deve ser um objeto.")
            self.lim_tensao = float(
                dados.get("lim_tensao", self.lim_tensao)
            )
            self.lim_corrente = float(
                dados.get("lim_corrente", self.lim_corrente)
            )
            self.lim_potencia = float(
                dados.get("lim_potencia", self.lim_potencia)
            )
            self.foi_alterado_manualmente = bool(
                dados.get("foi_alterado_manualmente", False)
            )
            self.porta_serial = str(
                dados.get("porta_serial", self.porta_serial)
            )
            self.baud_rate = str(
                dados.get("baud_rate", self.baud_rate)
            )
            self.timeout_serial = float(
                dados.get("timeout_serial", self.timeout_serial)
            )
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            # Registra a falha e recria o arquivo com valores padrão
            logger.exception("Erro ao carregar data/config.json")
            self._salvar()
            return

        # Completa arquivos antigos que ainda não tinham os campos seriais
        self._salvar()