import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QTextEdit, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import QProcess
import select

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.text_area_stdout = QTextEdit()  # Initialize QTextEdit for stdout
        self.text_area_stderr = QTextEdit()  # Initialize QTextEdit for stderr
        self.text_area_stdin = QLineEdit()   # Initialize text_area_stdin
        self.send_button = QPushButton('Send Input')

        layout = QVBoxLayout()
        layout.addWidget(self.text_area_stdout)
        layout.addWidget(self.text_area_stderr)
        layout.addWidget(self.text_area_stdin)
        layout.addWidget(self.send_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.normalOutputWritten)
        self.process.readyReadStandardError.connect(self.errorOutputWritten)
        self.process.start('python', ['-u', '.\GUI\subprocess_script.py'])

        self.send_button.clicked.connect(self.send_input)

    def send_input(self):
        input_text = self.text_area_stdin.text() + '\n'
        if self.process.state() == QProcess.ProcessState.Running:
            self.process.write(input_text.encode())
            self.text_area_stdin.clear()  # Clear the input field
        else:
            print("The subprocess has already terminated.")

    def normalOutputWritten(self):
        text = self.process.readAllStandardOutput().data().decode()
        self.text_area_stdout.append(text.strip())  # Append new message to the QTextEdit

    def errorOutputWritten(self):
        text = self.process.readAllStandardError().data().decode()
        self.text_area_stderr.append(text.strip())  # Append new error message to the QTextEdit

    def closeEvent(self, event):
        self.process.kill()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()