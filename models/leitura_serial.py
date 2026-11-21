# Signal = emite informações (dados recebidos, mensagem bruta e erros); 
# Serve pra comunicação entre objetos em conjunto com SLot que vai ser usado no controller
import logging
from PySide6.QtCore import QThread, Signal
from models.protocolo_serial import ProtocoloSerial

# Cria o logger do módulo
logger = logging.getLogger(__name__)

# Pega a recepção continua de dados da comunicação serial em thread separada p/ n bloquar interface
# valida mensagens com protocolo serial e encaminha válidos pro controller
class LeituraSerial(QThread):
    # Signals/sinais para comunicar os dados recebidos/erros
    dados_recebidos = Signal(dict)
    mensagem_bruta = Signal(str)
    erro_leitura = Signal(str)

    def __init__(self, conexao_serial, parent=None):
        super().__init__(parent)
        self.conexao_serial = conexao_serial

    def run(self):
        # Mantém a leitura enquanto thread n recebe uma solicitação de interrupção
        while not self.isInterruptionRequested():
            try:
                # Conf se conexão serial existe e ta aberta
                if not self.conexao_serial or not self.conexao_serial.is_open:
                    break
                # Lê linha da porta serial
                linha = self.conexao_serial.readline()
                # Aguarda pra caso n tenha recebido dados
                if not linha:
                    continue

                # Converte bytes recebidos para str e remove espaços+quebras de linha
                mensagem = linha.decode("utf-8", errors="replace").strip()
                # Emite a mensagem original recebida
                self.mensagem_bruta.emit(mensagem)

                print(f"SERIAL: {repr(mensagem)}", flush=True)
                # Conf se mensagem recebida é um pacote de telemetria
                if mensagem.startswith("$DAT,"):
                    try:
                        # Interpreta/vsalida mensagem recebida pelo protocolo
                        dados = ProtocoloSerial.interpretar(mensagem)
                        # Emite dados validados para o controller
                        self.dados_recebidos.emit(dados)
                    except ValueError as erro:  
                        # Registra mensagens inválidas sem interromper a leitura
                        logger.warning("Mensagem serial inválida: %s", erro)

            except Exception as erro:
                # Registra erros inesperados durante leitura
                logger.exception("Erro durante a leitura serial")
                # Comunica o erro ao controller
                self.erro_leitura.emit(str(erro))
                break