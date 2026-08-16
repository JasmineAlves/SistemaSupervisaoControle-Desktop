import sys
from PySide6.QtWidgets import QApplication
from controllers.dashboard_controller import DashController


def main():
    app = QApplication(sys.argv)

    janela_principal = DashController()
    janela_principal.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()