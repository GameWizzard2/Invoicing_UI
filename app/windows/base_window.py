import sys
import os
import logging

from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QWidget,
    QFileDialog,
)

from PySide6.QtGui import QAction



class BaseWindow(QMainWindow):
    """
    A base class for shared UI functionality across all windows.
    
    Responsibilities:
    - Manage window styles and settings.
    - Provide common UI utilities like folder selection.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Base Window Settings")
        self.resize(800, 600)

        # Set up widgets
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        # Setup Message Box
        self.messageBox = QMessageBox()

    def open_folder(self, label: QLabel, dialogTitle: str) -> str:
        """
        Opens a folder dialog and updates the provided label with the selected path.

        Parameters:
        - label (QLabel): The label to update with the selected folder path.
        - dialog_title (str): The title of the folder selection dialog.
        
        Returns:
        - str: The selected folder path, or None if no folder was selected.
        """
        # Opens the selected input folder and displays output to a widget label.
        inputFolderPath = QFileDialog.getExistingDirectory(self, dialogTitle)
        if inputFolderPath:
            label.setText(f"Selected Folder: {inputFolderPath}")
            return inputFolderPath
        else:
            label.setText("No folder selected.")
            return None



    