import sys
import logging

from PySide6.QtWidgets import QApplication

from GUI import FolderSelectorApp
from Logger import LoggerSetup



if __name__ == '__main__':
    LoggerSetup().initialize()
    app = QApplication(sys.argv)
    window = FolderSelectorApp()
    window.run()  # Explicitly call the run method
    window.show()
    sys.exit(app.exec())
