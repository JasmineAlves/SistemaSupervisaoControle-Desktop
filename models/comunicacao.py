import serial
import serial.tools.list_ports


class ComunicacaoModel:
    def __init__(self):
        self.porta = ""
        self.baud_rate = "9600"
        self.timeout = 1.0
        self.conexao_serial = None
        self.is_connected = False

    def listar_portas(self) -> list:
        portas = serial.tools.list_ports.comports()
        return [p.device for p in portas]

    def conectar(self, porta: str, baud_rate: str, timeout: float) -> bool:
        if not porta or porta == "Nenhuma porta encontrada":
            return False

        self.porta = porta
        self.baud_rate = baud_rate
        self.timeout = float(timeout)
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