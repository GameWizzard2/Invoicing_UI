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
    QLineEdit,
)
from PySide6.QtGui import QAction

from base_window import BaseWindow

class EmailFormatter(BaseWindow):
    def __init__(self):
        super().__init__()
        # Instance variable to store source and destination folder path
        self.setWindowTitle("Email Formatter")

        # Set empty string for container and seal numbers
        self.originalContainerNumber = QLineEdit()
        self.orginalSealNumber = QLineEdit()
        self.NewContainerNumber = QLineEdit("Not input")
        self.newlSealNumber = QLineEdit()

        # UI components initialized in methods
        self.emailTypeSelectionComboBox = None
        self.emailTypeSelectionLabel = None
        self.selectedEmailType = None

         # Dynamic input management
        self.userInputProjectScope = None
        self.customInputRow = None

    def setup_ui(self):
        # Create and add widgets

        # Add project scope combo box.
        self.project_scope_combo_box()
        self.formLayout = QFormLayout()
        self.formLayout.addRow('Original Container', self.originalContainerNumber)
        self.formLayout.addRow('Original Seal', self.orginalSealNumber)
        self.formLayout.addRow('New Container', self.NewContainerNumber)
        self.formLayout.addRow('New Seal', self.newlSealNumber)
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
            'Inspection': f'Inspection of {self.originalContainerNumber.text()}',
            'Adjustment': f'Adjustment of {self.originalContainerNumber.text()}',
            'Transload': f'Transload from {self.originalContainerNumber.text()} into {self.NewContainerNumber.text()}.',
            'Custom Input': logging.info('User picked a custom input option for "Project Scope" selection')
        }
        # Update the label using the dictionary
        self.emailTypeSelectionLabel.setText(actions.get(selected_value, "Invalid selection. Please choose an email type."))

        # Handle user 'Custom Input' selection in combobox
        self.selectedEmailType = selected_value
        self.manage_project_scope_user_input_input()

    def manage_project_scope_user_input_input(self):
        if (self.selectedEmailType == "Custom Input"):
            # Create and add the custom input field
            self.userInputProjectScope = QLineEdit()
            self.customInputRow = self.formLayout.rowCount()  # Track the row index
            self.formLayout.addRow("Enter project scope details:", self.userInputProjectScope)
        else:
            # Remove the "Custom Input" row if it exists
            if hasattr(self, "userInputProjectScope"):
                self.formLayout.removeRow(self.customInputRow)  
                del self.userInputProjectScope  
                del self.customInputRow  
        
    def run(self):
        # Organize startup tasks here
        self.setup_ui()
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailFormatter()
    window.run()  # Explicitly call the run method
    window.show()
    sys.exit(app.exec())