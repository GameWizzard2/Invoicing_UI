import sys
import os
import logging

from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QLabel,
)
from PySide6.QtGui import QAction

from app.base_window import BaseWindow
from app.resizer_modal import ResizerApp

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invoice Assistant")



    def menu_bar_creation(self):
        # Create menu bar
        menuBar = self.menuBar()
        # Create a help menu
        helpMenu = menuBar.addMenu("Help")
        # Add actions to the Help menu
        about_action = QAction("How-To", self)

    def setup_ui(self):
        # Create and add widgets
        self.resizerModalButton = QPushButton("1. Resize Images")
        self.resizerModalButton.clicked.connect(self.open_resizer_modal)
        self.mainLayout.addWidget(self.resizerModalButton)

        self.resizerModalButton = QPushButton("2. Email Creation")
        self.resizerModalButton.clicked.connect(self.open_email_creation)
        self.mainLayout.addWidget(self.resizerModalButton)

    def run(self):
        # Organize startup tasks here
        self.setup_ui()
        self.menu_bar_creation()

    def open_resizer_modal(self):
        self.modal = ResizerApp()
        self.modal.run()
        self.modal.show()

    def open_email_creation(self):
        self.messageBox.setText("Feature under construction.")
        self.messageBox.exec()

        