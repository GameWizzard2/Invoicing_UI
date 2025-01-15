import logging
import sys 
import textwrap
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QFileDialog,
    QTextEdit,
    QLabel,
    QLineEdit,
)
from PySide6.QtGui import QAction

from base_window import BaseWindow
from text_editor_windowed import TextEditor

class EmailFormatter(BaseWindow):
    def __init__(self):
        super().__init__()
        # Instance variable to store source and destination folder path
        self.setWindowTitle("Email Formatter")

        # Set empty string for container and seal numbers
        self.originalContainerNumber = QLineEdit()
        self.orginalSealNumber = QLineEdit()
        self.NewContainerNumber = QLineEdit()
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
        # Init layout
        self.formLayout = QFormLayout()

        # Add form fields
        self._add_form_fields()

        # Add project scope combo box.
        self.create_project_scope_combo_box()
        self.formLayout.addRow('Project Scope:', self.emailTypeSelectionComboBox)

        # Add form layout to the main layout
        self.mainLayout.addLayout(self.formLayout)

        # Create label to display self.formLayout.
        self._add_email_type_label()

        # Create the QTextEdit
        self.TextEditor = TextEditor()
        self.mainLayout.addWidget(self.TextEditor)


        # Create Email format button
        self.GenerateEmail = QPushButton("Generate Email")
        self.GenerateEmail.clicked.connect(self.create_formated_email)
        self.mainLayout.addWidget(self.GenerateEmail)

    def create_formated_email(self):
        #TODO self.emailTypeSelectionComboBox.currentText() if set to custom input, input must reflect user title input
        # Get the current date
        currentDate = datetime.now()

        # Retrieve the saved text from the TextEditor object
        emailBody = self.TextEditor.savedText.strip() if self.TextEditor.savedText else "No notes provided."

        # Determine the type of report
        if self.is_custom_input_selected():
            typeOfReport = self.userProjectScopeType.text()
        else:
            typeOfReport = self.emailTypeSelectionComboBox.currentText()

        # Generate the container seal info
        containerSealInfo = self.generate_container_seal_info()

        # Build the email body
        lines = [
            "All,",
            "",
            f"Please see attached a copy of our {typeOfReport} Report for:",
            "",
            "Project Scope: THIS NEEDS TO BE FIXED",
            "",
            "<b>Notes & Photo Breakdown:</b>",
            "",
            f"Date: {currentDate.strftime('%m/%d/%Y')}",
            "",
            containerSealInfo.strip(),
            "",
            emailBody,
            ""
        ]

        # Combine the lines into a single string
        self.emailFormated = "\n".join(lines)
        print(self.emailFormated)
        return self.emailFormated

    def generate_container_seal_info(self):
        """
        Generate email body text based on the selected email type and container/seal information.
        """
        # Retrieve text from input fields
        ogContainer = self.originalContainerNumber.text()
        ogSeal = self.orginalSealNumber.text()
        newContainer = self.NewContainerNumber.text()
        newSeal = self.newlSealNumber.text()

        # Define actions for each email type
        actions = {
            'Inspection': f'Container: {ogContainer}\n\nOld Seal: {ogSeal}\nNew Seal: {newSeal}\n',
            'Adjustment': f'Container: {ogContainer}\n\nOld Seal: {ogSeal}\nNew Seal: {newSeal}\n',
            'Transload': f'Original Container: {ogContainer}\nOld Seal: {ogSeal}\n\nNew Container: {newContainer}\nNew Seal: {newSeal}\n',
            'Custom Input': ""  # Custom input is handled separately
        }

        # Check if the selected email type exists in actions
        if self.selectedEmailType in actions:
            email_body = actions[self.selectedEmailType]
            # Handle custom input if needed
            if self.selectedEmailType == 'Custom Input' and hasattr(self, 'userInputProjectScope'):
                email_body = self.userInputProjectScope.text()
            return email_body
        else:
            logging.debug("Invalid or no email type selected.")
            return "Invalid selection or no email type selected."


    def _add_form_fields(self):
        self.formLayout.addRow('Original Container', self.originalContainerNumber)
        self.formLayout.addRow('Original Seal', self.orginalSealNumber)
        self.formLayout.addRow('New Container', self.NewContainerNumber)
        self.formLayout.addRow('New Seal', self.newlSealNumber)
        

    def _add_email_type_label(self):
        self.emailTypeSelectionLabel = QLabel('Select an Email Type')
        self.mainLayout.addWidget(self.emailTypeSelectionLabel)


    def create_project_scope_combo_box(self):
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

        # Handle user 'Custom Input' selection in combobox.
        self.selectedEmailType = selected_value
        self.manage_project_scope_user_input()

    def is_custom_input_selected(self):
        if (self.selectedEmailType == "Custom Input"):
           return True
        else:
            return False

    def manage_project_scope_user_input(self):
        if self.is_custom_input_selected() == True:
            # Create horizontal layout for the row
            self.customInputRowLayout = QHBoxLayout()

            # Create widgets
            userInputLabel1 = QLabel("Enter project scope details:")
            self.userProjectScopeType = QLineEdit()
            self.userProjectScopeType.setPlaceholderText('Enter Project scope, Example: "Transload", "Inspection", or "other".')

            self.userProjectScopeDetails = QLineEdit()
            self.userProjectScopeDetails.setPlaceholderText("Enter Project Scope details, containers, etc")
            
            # Add widgets to the horizontal layout
            self.customInputRowLayout.addWidget(userInputLabel1)
            self.customInputRowLayout.addWidget(self.userProjectScopeType)
            self.customInputRowLayout.addWidget(self.userProjectScopeDetails)

            self.customInputRow = self.formLayout.rowCount()  # Track the row index
            self.formLayout.addRow("Enter project scope details:", self.customInputRowLayout)
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