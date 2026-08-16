import sys
from PySide6.QtWidgets import QApplication
from controllers.dashboard_controller import DashController

def main():
    # Cria a aplicação Qt
    app = QApplication(sys.argv)

    # Cria a janela princiapl
    janela_principal = DashController()
    # Mostra a janela princiapl
    janela_principal.show()

    # Inicia o event loop que fica esperando: clique botão, alteração de valor,
    # receber dados, atualizar tela e fechar janela
    sys.exit(app.exec())

if __name__ == "__main__":
    main()