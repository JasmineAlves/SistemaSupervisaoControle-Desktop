import sys
import sqlite3
from PySide6.QtWidgets import QApplication, QMessageBox
from controllers.dashboard_controller import DashController
from database.connection import Database
from config.logging_config import configurar_logging
import logging

def main():
    # Cria a aplicação Qt
    app = QApplication(sys.argv)

    # Inicializa o registro de eventos e cria logger
    configurar_logging()
    logger = logging.getLogger(__name__)
    logger.info("Iniciando aplicação")

    try:
        # Inicializa o bd
        Database.init_db()
    except sqlite3.Error as erro:
        # Registra o erro de inicialização do banco
        logger.exception("Falha ao inicializar o banco de dados")

        # Executa em caso de erro ao inicializar o bd
        QMessageBox.critical(
            None,
            "Erro no banco de dados",
            f"Não foi possível inicializar o banco de dados da aplicação!\n\n{erro}"
        )
        # Indica que inicialização falhou/não abre janela principal
        return 1

    # Cria a janela princiapl
    janela_principal = DashController()
    # Mostra a janela princiapl
    janela_principal.show()

    # Inicia o event loop que fica esperando: clique botão, alteração de valor,
    # receber dados, atualizar tela e fechar janela
    sys.exit(app.exec())

if __name__ == "__main__":
    sys.exit(main())