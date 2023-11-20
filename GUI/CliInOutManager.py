from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QApplication
from PyQt6.QtWidgets import QSizePolicy
from GUI.Navigation import Ui_MainWindow
import sys
import os

class CliInOutManager(QWidget):
    def __init__(self, ui_main: Ui_MainWindow):
        super().__init__()
        self.ui = ui_main

        self.outputLayout = QVBoxLayout(self.ui.cliOutputArea)
        self.text_area_stdout = QTextEdit()
        self.text_area_stdout.setReadOnly(True)
        self.outputLayout.addWidget(self.text_area_stdout)

        # Set size policy for text area
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.text_area_stdout.setSizePolicy(sizePolicy)

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.normalOutputWritten)
        self.process.readyReadStandardError.connect(self.errorOutputWritten)

        if self.process.state() != QProcess.ProcessState.Running:
            script_path = os.path.join('.', 'GUI', 'subprocess_script.py')
            self.process.start('python', ['-u', script_path])
        else:
            self.appendOutput("Process is already running.")


    def send_input(self):
        input_text = self.ui.inputTextFromCli.text() + '\n'
        if self.process.state() == QProcess.ProcessState.Running:
            self.process.write(input_text.encode())
            self.ui.inputTextFromCli.clear()  # Clear the input field
        else:
            self.appendOutput("The subprocess has already terminated.")

    def appendOutput(self, text):
        current_text = self.text_area_stdout.toPlainText()
        self.text_area_stdout.setPlainText(current_text + '\n' + text)

    def normalOutputWritten(self):
        new_text = self.process.readAllStandardOutput().data().decode().strip()
        self.appendOutput(new_text)

    def errorOutputWritten(self):
        new_text = self.process.readAllStandardError().data().decode().strip()
        self.appendOutput(new_text)

