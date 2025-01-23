from datetime import datetime
import logging
import os


class EmailLogic():
    """
    A class containing utility methods for handling email logic.
    """
    
    def generate_email_body(self, selectedReport: str, reportTypeActions: dict, currentDate: datetime,
                            sealActions: dict, emailBody: str, files: str):
        """
        Generates an email body based on the provided report details and associated actions.

        Parameters:
        ----------
        selectedReport : str
            The type of report being generated (e.g., 'Inspection', 'Adjustment').
        actions : dict
            A dictionary mapping report types to project scope details.
            Example: {'Inspection': 'Inspection of EMHU', 'Adjustment': 'Adjustment of EMHU'}
        currentDate : datetime
            The current date to include in the email, formatted as MM/DD/YYYY.
        sealActions : dict
            A dictionary mapping report types to seal-specific actions or notes.
            Example: {'Inspection': 'New seal: #1, Old Seal: #2', 'Adjustment': 'New, Old Seal: old'}
        emailBody : str
            Additional notes or details to include in the email body.
        files : str
            A string listing any attached files.

        Returns:
        -------
        str
            A formatted email body as a single string, with line breaks separating sections.

        Example:
        --------
        Input:
            selectedReport = 'Inspection'
            actions = {'Inspection': 'Inspection of EMHU'}
            currentDate = datetime(2025, 1, 22)
            sealActions = {'Inspection': 'New seal: #1, Old Seal: #2'}
            emailBody = 'This is a summary of the inspection findings.'
            files = 'Attached files: Report.pdf'
        """
        
        lines = [
                "All,",
                "",
                f"Please see attached a copy of our {selectedReport} Report for:",
                "",
                f"Project Scope: {reportTypeActions.get(selectedReport)}",
                "",
                "<b>Notes & Photo Breakdown:</b>",
                "",
                f"Date: {currentDate.strftime('%m/%d/%Y')}",
                "",
                sealActions.get(selectedReport, ""),
                "",
                emailBody,
                "",
                f"{files}"
            ]
        
        self.email = "\n".join(lines)

    def print_email(self):
        print(self.email)

            

        """currentDate = datetime.now()

        # Retrieve the saved text from the TextEditor object
        emailBody = self.TextEditor.savedText.strip() if self.TextEditor.savedText else "No notes provided."

        # Determine the type of report
        if self.is_custom_input_selected():
            typeOfReport = self.userProjectScopeType.text()
            projectScopeDescription = self.userProjectScopeDetails.text()
        else:
            typeOfReport = self.getProjectScopeType
            projectScopeDescription = self.projectScopeDescription



        containerSealInfo = self.generate_container_seal_info()

        #return currentDate, emailBody, typeOfReport, projectScopeDescription, files, containerSealInfo

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
            "",
            f"{files}"
        ]

        # Combine the lines into a single string
        self.emailFormated = "\n".join(lines)
        print(self.emailFormated)
        return self.emailFormated"""