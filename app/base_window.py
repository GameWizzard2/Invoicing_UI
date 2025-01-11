import sys
import os
import logging

from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QMessageBox,
    QWidget,
)

from PySide6.QtGui import QAction
from app.utils import resize_image_by_half



class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Base Window Settings")
        self.setGeometry(100, 100, 400, 200)

        # Set up widgets
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        # Setup Message Box
        self.messageBox = QMessageBox()