import serial
import serial.tools.list_ports
from models.configuracao import Configuracao


class ComunicacaoModel:
    def __init__(self):
        self.configuracao = Configuracao()

        # Recupera os parâmetros salvos no JSON
        parametros = self.configuracao.obter_configuracao_comunicacao()
        self.porta = parametros["porta_serial"]
        self.baud_rate = parametros["baud_rate"]
        self.timeout = parametros["timeout_serial"]
        self.conexao_serial = None
        self.is_connected = False

    def listar_portas(self) -> list:
        portas = serial.tools.list_ports.comports()
        return [p.device for p in portas]

    def conectar(self, porta: str, baud_rate: str, timeout: float) -> bool:
        if not porta or porta == "Nenhuma porta encontrada":
            return False
        if not str(baud_rate).isdigit():
            return False

        try:
            timeout = float(timeout)
        except (TypeError, ValueError):
            return False
        
        if timeout <= 0:
            return False

        # Persiste a configuração antes de atualizar o estado
        sucesso = self.configuracao.atualizar_configuracao_comunicacao(
            porta=porta,
            baud_rate=str(baud_rate),
            timeout=timeout
        )
        if not sucesso:
            return False

        self.porta = porta
        self.baud_rate = str(baud_rate)
        self.timeout = timeout
        self.is_connected = True
        return True

    def desconectar(self) -> bool:
        if self.conexao_serial and getattr(self.conexao_serial, 'is_open', False):
            self.conexao_serial.close()

        self.is_connected = False
        return True

    def obter_status(self) -> str:
        if self.is_connected:
            return f"Status : Conectado ({self.porta} @ {self.baud_rate} bps, timeout: {self.timeout}s)"
        return "Status : Desconectado"