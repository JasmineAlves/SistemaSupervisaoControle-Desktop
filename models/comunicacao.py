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
        self.baud_rate_atual = 9600
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
            baud_rate = int(baud_rate)
            timeout = float(timeout)
        except (TypeError, ValueError):
            return False
        
        if timeout <= 0 or baud_rate <= 0:
            return False

        nova_conexao = None

        try:
            # Abre a conexão fisica com porta serial
            nova_conexao = serial.Serial(
                port = porta,
                baudrate = 9600,
                timeout = timeout
            )

            # Persiste a config após abrir a porta
            sucesso = self.configuracao.atualizar_configuracao_comunicacao(
                porta = porta,
                baud_rate = str(baud_rate),
                timeout = timeout
            )
            if not sucesso:
                nova_conexao.close()
                return False

            # Fecha conexão anterior caso exista
            if self.conexao_serial and self.conexao_serial.is_open:
                self.conexao_serial.close()

            self.conexao_serial = nova_conexao
            self.porta = porta
            self.baud_rate = str(baud_rate)
            self.baud_rate_atual = 9600
            self.timeout = timeout
            self.is_connected = True
            return True

        except(serial.SerialException, OSError, ValueError):
            if nova_conexao and nova_conexao.is_open:
                nova_conexao.close()
            self.conexao_serial = None
            self.is_connected = False
            return False

    def enviar_comando(self, comando: str) -> bool:
        # Conf se conexão serial existe e ta aberta
        if not self.conexao_serial or not self.conexao_serial.is_open:
            return False

        try:
            # Garante que comando termine com quebra de linha
            comando = comando.rstrip("\r\n") + "\n"
            # Converte pra bytes e envia por serial
            self.conexao_serial.write(comando.encode("utf-8"))
            #Aguarda escrita dos dados pendentes
            self.conexao_serial.flush()
            return True
        except (serial.SerialException, OSError):
            return False

    def alterar_baud_rate(self, baud_rate: int) -> bool:
        if not self.conexao_serial or not self.conexao_serial.is_open:
            return False

        try:
            # altera a velocidade da conexão serial
            self.conexao_serial.baudrate = baud_rate
            self.baud_rate_atual = baud_rate
            return True
        except (serial.SerialException, OSError, ValueError):
            return False

    def desconectar(self) -> bool:
        try:
            if self.conexao_serial and self.conexao_serial.is_open:
                self.conexao_serial.close()
            self.conexao_serial = None
            self.is_connected = False
            return True
        except serial.SerialException:
            self.is_connected = False
            return False

    def obter_status(self) -> str:
        if self.is_connected and self.conexao_serial and self.conexao_serial.is_open:
            return (
                f"Status : Conectado "
                f"({self.porta} @ {self.baud_rate_atual} bps, "
                f"timeout: {self.timeout}s)"
        )
        return "Status : Desconectado"