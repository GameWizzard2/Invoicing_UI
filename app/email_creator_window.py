import logging
import sys 

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QLabel,
)
from PySide6.QtGui import QAction

from base_window import BaseWindow

class EmailFormatter(BaseWindow):
    def __init__(self):
        super().__init__()
        # Instance variable to store source and destination folder path
        self.setWindowTitle("Email Formatter")

    def setup_ui(self):
        # Create and add widgets
        


        # Add project scope combo box.
        self.project_scope_combo_box()
        self.formLayout = QFormLayout()
        self.formLayout.addRow('Project Scope:', self.emailTypeSelectionComboBox)
        # Add form layout to the main layout
        self.mainLayout.addLayout(self.formLayout)

        # Create label to display self.formLayout.
        self.emailTypeSelectionLabel = QLabel('Select an Email Type')
        self.mainLayout.addWidget(self.emailTypeSelectionLabel)
        
    def project_scope_combo_box(self):
        self.emailTypeSelectionComboBox = QComboBox()
        self.emailTypeSelectionComboBox.addItems(['Inspection', 'Adjustment', 'Transload', 'Custom Input'])
        self.emailTypeSelectionComboBox.currentTextChanged.connect(self.handle_email_type_selection)
        return self.emailTypeSelectionComboBox
    
    def handle_email_type_selection(self, selected_value):
    # Define a dictionary for actions
    #FIXME set values for {orignalContainerNumber} and {NewContainerNumber}
        actions = {
            'Inspection': 'Inspection of {orginalContainerNumber}',
            'Adjustment': 'Adjustment of {orginalContainerNumber}',
            'Transload': 'Transload from {orignalContainerNumber} into {NewContainerNumber}.',
            'Custom Input': logging.info('User picked a custom input option for "Project Scope" selection')
        }

        # Update the label using the dictionary
        self.emailTypeSelectionLabel.setText(actions.get(selected_value, "Invalid selection. Please choose an email type."))
        

    def run(self):
        # Organize startup tasks here
        self.setup_ui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailFormatter()
    window.run()  # Explicitly call the run method
    window.show()
    sys.exit(app.exec())