from src.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

def run() -> None:
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())