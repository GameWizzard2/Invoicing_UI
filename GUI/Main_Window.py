import sys
import os
import logging

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLabel,
)
from ImageTools import resize_image_by_half



class FolderSelectorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Resizer")
        self.setGeometry(100, 100, 400, 200)

        # Instance variable to store source and destination folder path
        self.selectedInputFolder = None
        self.selectdOutputFolder = None

        # Set up widgets
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

    def setup_ui(self):
        # Create and add widgets
        self.selectFolderButton = QPushButton("Select Folder")
        self.selectFolderButton.clicked.connect(self.open_input_folder)
        self.mainLayout.addWidget(self.selectFolderButton)

        self.selectFolderButton = QPushButton("Select Output Folder for resized Images.")
        self.selectFolderButton.clicked.connect(self.open_output_folder)
        self.mainLayout.addWidget(self.selectFolderButton)

        self.inputFolderPathLabel = QLabel("No source destination folder selected.")
        self.mainLayout.addWidget(self.inputFolderPathLabel)

        self.ouputFolderPathLabel = QLabel("No selected destination selected.")
        self.mainLayout.addWidget(self.ouputFolderPathLabel)

        self.useFolderButton = QPushButton("Resize Images in selected folder")
        self.useFolderButton.clicked.connect(self.resize_images_in_folder)
        self.mainLayout.addWidget(self.useFolderButton)

    def run(self):
        # Organize startup tasks here
        self.setup_ui()

    def open_input_folder(self):
        inputFolderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if inputFolderPath:
            self.selectedInputFolder = inputFolderPath
            self.inputFolderPathLabel.setText(f"Selected Folder: {inputFolderPath}")
        else:
            self.inputFolderPathLabel.setText("No folder selected.")

    def open_output_folder(self):
        outputFolderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if outputFolderPath:
            self.selectedOutputFolder = outputFolderPath
            self.ouputFolderPathLabel.setText(f"Selected Folder: {outputFolderPath}")
        else:
            self.ouputFolderPathLabel.setText("No folder selected.")

    def resize_images_in_folder(self):
        if self.selectedInputFolder and self.selectedOutputFolder:
            for file in os.listdir(self.selectedInputFolder):
                logging.debug(f"The current file select is {file}")

                resize_image_by_half(self.selectedInputFolder, self.selectdOutputFolder)
        else:
            print("No folder selected yet!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderSelectorApp()
    window.run()  # Explicitly call the run method
    window.show()
    sys.exit(app.exec())
