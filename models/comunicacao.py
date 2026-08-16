class ComunicacaoModel:
    def __init__(self):
        self.porta = ""
        self.baud_rate = "9600"
        self.timeout = 1
        self.conexao_serial = None
        self.is_connected = False