"""
Ponto de entrada do CortexForge.

Inicia a aplicação desktop PySide6 e exibe a janela principal.
"""

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> int:
    """Cria a aplicação Qt e executa o loop de eventos."""
    app = QApplication(sys.argv)
    app.setApplicationName("CortexForge")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
