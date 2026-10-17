import logging
from pathlib import Path

# Define os caminhos a partir da raiz do projeto
DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_LOGS = DIR_PROJETO / "logs"
ARQUIVO_LOG = DIR_LOGS / "smartgrid.log"

# Configura o registro de eventos operacionais do sistema
def configurar_logging():
    # Cria a pasta de logs caso ela ainda não exista
    DIR_LOGS.mkdir(parents=True, exist_ok=True)
    # Define o formato das mensagens de log
    formato = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    # Configura o arquivo e a saída no terminal
    logging.basicConfig(
        level=logging.INFO,
        format=formato,
        handlers=[
            logging.FileHandler(ARQUIVO_LOG, encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True
    )

    # Registra que a configuração do log foi inicializada
    logging.getLogger(__name__).info(
        "Sistema de logging inicializado"
    )