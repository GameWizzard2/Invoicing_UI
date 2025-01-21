from PySide6.QtWidgets import (
QPushButton,
QTextEdit, 
QWidget, 
QVBoxLayout
)

# Define the TextEditor class
class TextEditor(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QTextEdit widget
        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText("Type your text here...")
        self.textEdit.setMaximumHeight(400)

         # Create a Save button
        self.saveButton = QPushButton("Load Text For Format")
        self.saveButton.clicked.connect(self.save_plan_text_to_variable)

        # Variable to store the formatted text
        self.savedText = ""

        # Set up a layout and add the QTextEdit widget
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.saveButton)
        self.setLayout(layout)

        # Apply the layout to the TextEditor
        self.setLayout(layout)

    def save_rich_text_to_variable(self):
        self.savedTextRich = self.textEdit.toHtml()
        print(f"Rich text saved:\n{self.savedTextRich}")
        return self.savedTextRich
    
    def save_plan_text_to_variable(self):
        self.savedText = self.textEdit.toPlainText()
        print(f"Text saved:\n{self.savedText}")
        return self.savedText
    