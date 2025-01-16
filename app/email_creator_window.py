import logging
import sys 
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
        self.getProjectScopeType = None

         # Dynamic input management
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
            projectScopeDescription = self.userProjectScopeDetails.text()
        else:
            typeOfReport = self.getProjectScopeType
            projectScopeDescription = self.projectScopeDescription

        #projectScopeDescription = typeOfReport

        # Generate the container seal info
        containerSealInfo = self.generate_container_seal_info()
        # Build the email body
        lines = [
            "All,",
            "",
            f"Please see attached a copy of our {typeOfReport} Report for:",
            "",
            f"Project Scope: {projectScopeDescription}",
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
        # Retrieve container and seal details
        actions = self.get_container_seal_details()

        # Define actions for each email type using a dictionary.
        getSealInfoText = self.define_seal_info_actions(actions)

        # Get the email body based on the selected email type
        return self.get_email_body(getSealInfoText)

    def get_container_seal_details(self):
        """
        Retrieve container and seal details from input fields.
        """
        return {
            'ogContainer': self.originalContainerNumber.text(),
            'ogSeal': self.orginalSealNumber.text(),
            'newContainer': self.NewContainerNumber.text(),
            'newSeal': self.newlSealNumber.text(),
        }

    def define_seal_info_actions(self, details):
        """
        Define the email body actions based on container and seal details.
        """
        return {
            'Inspection': f"Container: {details['ogContainer']}\n\nOld Seal: {details['ogSeal']}\nNew Seal: {details['newSeal']}\n",
            'Adjustment': f"Container: {details['ogContainer']}\n\nOld Seal: {details['ogSeal']}\nNew Seal: {details['newSeal']}\n",
            'Transload': f"Original Container: {details['ogContainer']}\nOld Seal: {details['ogSeal']}\n\nNew Container: {details['newContainer']}\nNew Seal: {details['newSeal']}\n",
            'Custom Input': ""  # Custom input is handled separately
        }

    def get_email_body(self, actions):
        """
        Retrieve the email body based on the selected email type.
        """
        if self.getProjectScopeType in actions:
            return actions[self.getProjectScopeType]
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
        self.emailTypeSelectionComboBox.currentTextChanged.connect(self.update_email_type_combo_box_selection)
        return self.emailTypeSelectionComboBox
    
    def _get_project_combo_box_actions(self) -> dict:
        # Define a dictionary for actions displayed in the self.emailTypeSelectionComboBox
        actions = {
        'Inspection': f'Inspection of {self.originalContainerNumber.text()}',
        'Adjustment': f'Adjustment of {self.originalContainerNumber.text()}',
        'Transload': f'Transload from {self.originalContainerNumber.text()} into {self.NewContainerNumber.text()}.',
        'Custom Input': "Define you Project Title Scope, then provide a Description."  
        }

        return actions
        
    
    def update_email_type_combo_box_selection(self, selected_value):
        actions = self._get_project_combo_box_actions()
        #FIXME set values for {orignalContainerNumber} and {NewContainerNumber}
        
        # Update the label using the dictionary stored in actions
        action_text = actions.get(selected_value, "Invalid selection. Please choose an email type.")
        self.emailTypeSelectionLabel.setText(actions.get(action_text))

        # Define Variables for Project scope Type, and description for Type
        self.projectScopeDescription = action_text
        self.getProjectScopeType = selected_value
        

        # Handle user 'Custom Input' selection in combobox.
        self.handle_combo_box_user_input()

    def handle_combo_box_user_input(self):
        #TODO make logic that checks if "Custom Input combo box" is navigated away from and then call self._delete_custom_input_row() instead of everytime Custom Input is not selected.
        if self.is_custom_input_selected() == True:
            # Create horizontal layout for the row
            self.customInputRowLayout = QHBoxLayout()
            self._create_custom_input_row()
            self.customInputRow = self.formLayout.rowCount()  # Track the row index
            self.formLayout.addRow("Enter project scope details:", self.customInputRowLayout)
        else:
            # Remove the "Custom Input" row if it exists
            if hasattr(self, "customInputRowLayout"):
                self._delete_custom_input_row()
                

    def _create_custom_input_row(self):
            # Creates Custom input row.
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

    def _delete_custom_input_row(self):
        # Deletes Custom input row.
        self.formLayout.removeRow(self.customInputRow)  
        self.customInputRowLayout.deleteLater()
        del self.customInputRowLayout
        del self.customInputRow  

    def is_custom_input_selected(self):
        if (self.getProjectScopeType == "Custom Input"):
            return True
        else:
            return False

   
        
    def run(self):
        # Organize startup tasks here
        self.setup_ui()
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailFormatter()
    window.run()  # Explicitly call the run method
    window.show()
    sys.exit(app.exec())