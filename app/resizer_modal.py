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
from app.utils import resize_image_by_half



class ResizerApp(BaseWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Resizer")
        # Instance variable to store source and destination folder path
        self.selectedInputFolder = None
        self.selectdOutputFolder = None

    def setup_ui(self):
        # Create and add widgets
        self.selectInputFolderButton = QPushButton("Select Source Folder")
        self.selectInputFolderButton.clicked.connect(self.open_input_folder)
        self.mainLayout.addWidget(self.selectInputFolderButton)

        self.selectOutputFolderButton = QPushButton("Select Output Folder.")
        self.selectOutputFolderButton.clicked.connect(self.open_output_folder)
        self.mainLayout.addWidget(self.selectOutputFolderButton)

        self.inputFolderPathLabel = QLabel("No source destination folder selected.")
        self.mainLayout.addWidget(self.inputFolderPathLabel)

        self.ouputFolderPathLabel = QLabel("No selected destination selected.")
        self.mainLayout.addWidget(self.ouputFolderPathLabel)

        self.useFolderButton = QPushButton("Resize Images in selected folder")
        self.useFolderButton.clicked.connect(self.resize_images_in_folder)
        self.mainLayout.addWidget(self.useFolderButton)

    def menu_bar_creation(self):
        # Create menu bar
        menuBar = self.menuBar()
        # Create a help menu
        helpMenu = menuBar.addMenu("Help")
        # Add actions to the Help menu
        about_action = QAction("How-To", self)
        about_action.triggered.connect(self._show_about_dialog)
        helpMenu.addAction(about_action)

    def run(self):
        # Organize startup tasks here
        self.setup_ui()
        self.menu_bar_creation()

    def _show_about_dialog(self):
        docuResizerApp = """
        This window resizes all images in the selected folder.

        To resize all images the following steps should be taken:

        1. Select the folder containing the images you would like to resize.
        2. Select the destination folder you would like the images to be saved to.
        3. Click Resize Images button to begin.
        4. Navigate to the destination folder to retrieve the resized images.
    
        """
        QMessageBox.about(self, "How-To", docuResizerApp)

    def open_input_folder(self):
        # Opens the selected input folder.
        inputFolderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if inputFolderPath:
            self.selectedInputFolder = inputFolderPath
            self.inputFolderPathLabel.setText(f"Selected Folder: {inputFolderPath}")
        else:
            self.inputFolderPathLabel.setText("No folder selected.")

    def open_output_folder(self):
        # Opens the selected output folder.
        outputFolderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if outputFolderPath:
            self.selectedOutputFolder = outputFolderPath
            self.ouputFolderPathLabel.setText(f"Selected Folder: {outputFolderPath}")
        else:
            self.ouputFolderPathLabel.setText("No folder selected.")

    def resize_images_in_folder(self):
        # Process each file in the input folder and resize if image.
        totalFilesInFolder = len(os.listdir(self.selectedInputFolder))
        if self.selectedInputFolder and self.selectedOutputFolder:

            countImagesResized = 0 # Count the number of images that got resized.
            skippedFiles = ''
            for file in os.listdir(self.selectedInputFolder):
                # Construct full input and output file paths
                inputFilePath = os.path.join(self.selectedInputFolder, file)
                outputFilePath = os.path.join(self.selectedOutputFolder, file)
                logging.debug(
                    f"The current file selected is {file} and has been joined to create "
                    f"inputFilePath: {inputFilePath} and outputFilePath: {outputFilePath}"
                    )

                # Filter for valid image files
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                    resize_image_by_half(inputFilePath, outputFilePath)
                    countImagesResized += 1
                else:
                    logging.info(f"Skipping non-image file: {file}")
                    skippedFiles += (f"{file}\n")

            # Let user know if all images were resized.
            if countImagesResized == totalFilesInFolder:
                self.messageBox.setText(f"All {countImagesResized} images were resized!")
            else:
                self.messageBox.setText(f"{countImagesResized} out of {totalFilesInFolder} files were compatible image files and have been resized!\n\n"
                                        f"The following files were incompitable or unable to be resized:\n{skippedFiles}")
        else:
            self.messageBox.setText("No 'Destination' or 'Source' folder selected yet! \nPlease verfiy both folders have been set.")
        self.messageBox.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResizerApp()
    window.run()  # Explicitly call the run method
    window.show()
    sys.exit(app.exec())