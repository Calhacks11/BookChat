import sys
import time


from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPushButton, QFileDialog, QVBoxLayout, QLineEdit
import os
from epub_parser.epub_to_text import epub_to_chapters, get_chapter
from llm.llm_queries import query_characters

class ChapterWindow(QWidget):
    def __init__(self, bookname):
        super().__init__()
        self.bookname = bookname
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()
        content = get_chapter(self.bookname, 1)
        label = QLabel(content, self)
        status = QLabel('---', self)
        layout.addWidget(label)
        layout.addWidget(status)
        self.setLayout(layout)
        self.setWindowTitle('Chapter Window')
        self.setGeometry(300, 300, 400, 200)
        status.setText('Understanding the characters...')
        prompt_response = query_characters(content)
        status.setText(str(prompt_response))

        # print(prompt_response)


class FileUploadApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set the layout
        layout = QVBoxLayout()

        # Create a button to open the file dialog
        self.upload_button = QPushButton('Upload File', self)
        self.upload_button.clicked.connect(self.openFileDialog)

        # Create a label to display the selected file path
        self.label = QLabel('No file selected', self)

        # Create a button to save the file to the specified path
        self.save_button = QPushButton('Save File', self)
        self.save_button.clicked.connect(self.saveFile)
        self.save_button.setEnabled(False)  # Disable save button until a file is selected

        # Add widgets to layout
        layout.addWidget(self.upload_button)
        layout.addWidget(self.label)
        layout.addWidget(self.save_button)

        # Set the main layout
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('File Upload')
        self.setGeometry(300, 300, 400, 200)

        self.file_bytes = None  # Variable to store the file bytes

    def openFileDialog(self):
        # Open the file dialog
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*)')

        # If a file is selected
        if file_name:
            self.label.setText(f'Selected file: {file_name}')
            self.selected_file_path = file_name

            # Read the file in binary mode and get the bytes
            with open(file_name, 'rb') as file:
                self.file_bytes = file.read()

            self.save_button.setEnabled(True)  # Enable save button after file is selected
        else:
            self.label.setText('No file selected')
            self.save_button.setEnabled(False)  # Disable save button if no file is selected

    def saveFile(self):
        # Get the new file path from the input field
        file_name = os.path.splitext(os.path.basename(self.selected_file_path))[0]
        new_file_path = f'data/{file_name}.epub'

        if new_file_path and self.file_bytes:
            try:
                # Write the file bytes to the new path
                with open(new_file_path, 'wb') as new_file:
                    new_file.write(self.file_bytes)
                self.label.setText(f'File saved to: {new_file_path}')
                epub_to_chapters(f'{file_name}.epub')
                time.sleep(1)
                self.chapter_window = ChapterWindow(file_name)
                self.chapter_window.show()
                self.close()
            except Exception as e:
                self.label.setText(f'Error saving file: {str(e)}')
        else:
            self.label.setText('No file selected or no file path specified')


# Create an instance of QApplication
app = QApplication([])

# window = QWidget()
# window.setWindowTitle("Ebook Reader App")
# window.setGeometry(300, 200, 300, 200)
#
# layout = QGridLayout()
#
# helloMsg = QLabel("<h3>Upload the .epub file</h3>", parent=window)
# helloMsg.move(60, 15)
#
# window.show()
# Run the application's event loop
ex = FileUploadApp()
ex.show()
sys.exit(app.exec())