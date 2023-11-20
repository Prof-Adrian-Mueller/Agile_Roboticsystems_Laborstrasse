from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QApplication, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from GUI.Navigation import Ui_MainWindow
import sys
import os

class CliInOutManager(QWidget):
    def __init__(self, ui_main: Ui_MainWindow):
        super().__init__()
        self.ui = ui_main

        self.layout = QVBoxLayout(self.ui.cliOutputArea)

        scroll = QScrollArea(self)
        self.layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Disable horizontal scrolling

        frame = QFrame(scroll)
        scroll.setWidget(frame)

        self.outputLayout = QVBoxLayout(frame)

        # Set size policy for text area
        self.sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.ui.cliOutputArea.setSizePolicy(self.sizePolicy)

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
        widget = QWidget()
        widget.setObjectName("clioutputwidgetdesign")
        self.outputLayout.addWidget(widget)
        h_layout = QHBoxLayout(widget)

        label = QLabel(text)
        label.setWordWrap(True)
        h_layout.addWidget(label)

    def normalOutputWritten(self):
        new_text = self.process.readAllStandardOutput().data().decode().strip()
        self.appendOutput(new_text)

    def errorOutputWritten(self):
        new_text = self.process.readAllStandardError().data().decode().strip()
        self.appendOutput(new_text)
