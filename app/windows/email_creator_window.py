import logging
import sys 
import os
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QBoxLayout,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QFileDialog,
    QTextEdit,
    QLabel,
    QLineEdit,
    QLayout
)
from PySide6.QtGui import QAction

from app import EmailLogic

from app import has_file_path

from app import BaseWindow
from app.windows.text_editor_windowed import (
    TextEditor,
    EmailWindow,
)

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

        # Set string for email Generation
        self.email = "Email generator not yet activated by user."

        # UI components initialized in methods
        self.emailTypeSelectionComboBox = None
        self.emailTypeSelectionLabel = None
        self.getProjectScopeType = None

         # Dynamic input management
        self.customInputRow = None

        #Self explaintory
        self.currentDate = datetime.now()

        # Set strings to get photo for email generation
        self.photoPath = ""
        self.photoFiles = ""

    def setup_ui(self):
        # Create and add widgets
        # Init layout
        self.formLayout = QFormLayout()
        #self.formLayo = QFormLayout()

        # Add form fields
        self._add_form_fields()

        # Add project scope combo box.
        self.create_project_scope_combo_box()
        self.formLayout.addRow('Project Scope:', self.emailTypeSelectionComboBox)

        # Add form layout to the main layout
        self.mainLayout.addLayout(self.formLayout)

        # Create label to display self.formLayout.
        self._add_email_type_label()

        # Create a checkbox that enables folder seletion to select images to place in the email.
        folderSelectionPhotosCheckbox = QCheckBox("Add a list of photo names to email?", self)
        self.mainLayout.addWidget(folderSelectionPhotosCheckbox)
        folderSelectionPhotosCheckbox.checkStateChanged.connect(self.on_check_box_state_changed)

        # Placeholder Layout for the dynmaic row addded when checkbox clicked
        self.dynamicLayout1 = QBoxLayout(QBoxLayout.LeftToRight)
        self.mainLayout.addLayout(self.dynamicLayout1)
        
        # Create the QTextEdit
        self.TextEditor = TextEditor()
        self.mainLayout.addWidget(self.TextEditor)

        # Create Email format button
        self.GenerateEmail = QPushButton("Generate Email")
        self.GenerateEmail.clicked.connect(self.create_email)
        self.mainLayout.addWidget(self.GenerateEmail)

    def create_check_box_layout(self):
            self.photoCheckBoxFormLayout = QFormLayout()

            # Define Widgets
            self.getPhotoPathButton = QPushButton("Select Folder Containing Photos")
            self.setPhotoPathLabel = QLabel("No Folder Selected")
            self.photoCheckBoxFormLayout.addRow(self.getPhotoPathButton, self.setPhotoPathLabel)

            self.getPhotoPathButton.clicked.connect(self.set_photo_path)

            self.dynamicLayout1.addLayout(self.photoCheckBoxFormLayout)

    def set_photo_path(self):
        self.photoPath = self.open_folder(self.setPhotoPathLabel, 'Select Photo Folder')
        if hasattr(self,'photoPath') and self.photoPath and os.path.exists(self.photoPath) and os.path.isdir(self.photoPath):
            self.photoFiles = "\n".join([file for file in os.listdir(self.photoPath)])
            logging.info("No photos were provided to attach to email.")
        else:
            logging.info("No photos were provided to attach to email.")
            self.photoFiles = ""

            
    def on_check_box_state_changed(self, state):
        if state == Qt.Checked:
            self.create_check_box_layout()
        
        elif state == Qt.Unchecked:
            self.remove_layout_and_widgets(self.photoCheckBoxFormLayout)

    def create_email(self):
        """
        Creates an email by dynamically generating its body based on user input or predefined options.

        Description:
        ------------
        This method initializes an instance of the `EmailLogic` class and generates the email body based on whether 
        custom input is selected or predefined options are being used. If `is_custom_input_selected` is `True`, 
        the email body is constructed using the values from `userProjectScopeType` and `custom_row_actions`. 
        Otherwise, it uses the selected report type from `emailTypeSelectionComboBox`. The generated email is 
        then printed to the console.

        Parameters:
        -----------
        None

        Instance Attributes Used:
        --------------------------
        - `is_custom_input_selected` (bool): A flag indicating whether custom input is selected.
        - `userProjectScopeType` (QLineEdit): A line edit widget for entering custom project scope types.
        - `custom_row_actions` (function): A function that dynamically generates additional input data for custom input.
        - `emailTypeSelectionComboBox` (QComboBox): A combo box containing predefined report type options.
        - `currentDate` (datetime): The current date to include in the email.
        - `get_container_seal_actions` (method): Retrieves container seal-related actions.
        - `TextEditor.save_plain_text_to_variable` (method): Retrieves the plain text from the text editor.
        - `photoFiles` (str): A string containing the filenames of attached photos.

        Returns:
        --------
        None
        """
        self.email = EmailLogic()
        
        if self.is_custom_input_selected():
            self.email.generate_email_body(self.userProjectScopeType.text(), self.custom_row_actions(),
                                       self.currentDate, self.get_container_seal_actions(), self.TextEditor.save_plain_text_to_variable(), self.photoFiles)

        else:
            self.email.generate_email_body(self.emailTypeSelectionComboBox.currentText(), self.get_report_type_actions(),
                                       self.currentDate, self.get_container_seal_actions(), self.TextEditor.save_plain_text_to_variable(), self.photoFiles)
        
        # Open a new EmailWindow to display the email content
        self.email_window = EmailWindow(self.email.email)
        self.email_window.show()

    def generate_container_seal_info(self):
        """
        Generate email body text based on the selected email type and container/seal information.
        """
        # Retrieve container and seal details
        actions = self.get_container_seal_actions()

        # Define actions for each email type using a dictionary.
        getSealInfoText = self.define_seal_info_actions(actions)

        # Get the email body based on the selected email type
        return self.get_email_body(getSealInfoText)

    def get_container_seal_actions(self):
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

    def get_seal_info_for_email_body(self, actions: dict) -> str:
        """
        Retrieves the seal information for the email body based on the current project scope type.

        Args:
            actions (dict): A dictionary where keys represent possible project scope types
                            and values represent corresponding seal information.

        Returns:
            str: The seal information corresponding to the selected project scope type.
                If the project scope type is invalid or not found in the `actions` dictionary,
                a default message indicating an invalid or no selection is returned.
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
    
    def get_report_type_actions(self) -> dict:
        # Define a dictionary for actions displayed in the self.emailTypeSelectionComboBox
        actions = {
        'Inspection': f'Inspection of {self.originalContainerNumber.text()}',
        'Adjustment': f'Adjustment of {self.originalContainerNumber.text()}',
        'Transload': f'Transload from {self.originalContainerNumber.text()} into {self.NewContainerNumber.text()}.',
        'Custom Input': "Define you Project Title Scope, then provide a Description."  
        }

        return actions
        
    
    def update_email_type_combo_box_selection(self, selected_value):
        actions = self.get_report_type_actions()
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
        #TODO make logic that checks if "Custom Input combo box" is navigated away from and then call self._hide_custom_input_row() instead of everytime Custom Input is not selected.
        if self.is_custom_input_selected() and not hasattr(self, 'customInputRowLayout'):
                # Create horizontal layout for the row
                self.customInputRowLayout = QHBoxLayout()
                self._create_custom_input_row()
                self.customInputRow = self.formLayout.rowCount()  # Track the row index
                self.formLayout.addRow("Enter project scope details:", self.customInputRowLayout)

        elif self.is_custom_input_selected() and hasattr(self, 'customInputRowLayout'):
            self.customInputRowLayout.setEnabled(True)

        elif (self.is_custom_input_selected() is False) and hasattr(self, 'customInputRowLayout'):
                self._hide_custom_input_row()


        elif self.is_custom_input_selected() and not hasattr(self, 'customInputRowLayout'):
            logging.info("Custom input is not selected and self.customInputRowLayout does not exist, moving on.")


                

        
        elif self.customInputRowLayout.isEnabled() == False:
            # Remove the "Custom Input" row if it is not selected.
            if hasattr(self, "customInputRowLayout"):
                self._hide_custom_input_row()
                

    def _create_custom_input_row(self):
            # Creates Custom input row.
            # Create widgets
            self.userProjectScopeType = QLineEdit()
            self.userProjectScopeType.setPlaceholderText('Enter Project scope, Example: "Transload", "Inspection", or "other".')

            self.userProjectScopeDetails = QLineEdit()
            self.userProjectScopeDetails.setPlaceholderText("Enter Project Scope details, containers, etc")
            
            # Add widgets to the horizontal layout
            self.customInputRowLayout.addWidget(self.userProjectScopeType)
            self.customInputRowLayout.addWidget(self.userProjectScopeDetails)


    def custom_row_actions(self):
        """
        Collects user inputs and returns them as a dictionary.
        """
        return {
            self.userProjectScopeType.text() : self.userProjectScopeDetails.text(),
        }

    def _hide_custom_input_row(self):

        
        # Remove row from form layout
        self.customInputRowLayout.setEnabled(False)


    def is_custom_input_selected(self):
        # check if custom input is selected in combobox 
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