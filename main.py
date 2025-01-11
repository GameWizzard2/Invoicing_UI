import sys
import logging

from PySide6.QtWidgets import QApplication

from app import MainWindow
from Logger import LoggerSetup



if __name__ == '__main__':
    LoggerSetup().initialize()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.run()  # Explicitly call the run method
    window.show()
    sys.exit(app.exec())
