from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QApplication, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from GUI.Navigation import Ui_MainWindow
import sys
import os


class CliInOutWorkerThreadManager(QWidget):
    def __init__(self, ui_main: Ui_MainWindow):
        super().__init__()
        self.defaultWidget = None
        self.defaultLabel = None
        self.ui = ui_main
        self.process = None
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

        self.displayDefault("Process has not been still started.")

    def displayDefault(self, message):
        self.defaultWidget = QWidget()
        self.defaultWidget.setObjectName("clioutputwidgetdesign")
        self.outputLayout.addWidget(self.defaultWidget)
        h_layout = QHBoxLayout(self.defaultWidget)

        self.defaultLabel = QLabel(message)
        self.defaultLabel.setWordWrap(True)
        h_layout.addWidget(self.defaultLabel)

    def startProcess(self):
        if not self.isProcessStarted():
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self.normalOutputWritten)
            self.process.readyReadStandardError.connect(self.errorOutputWritten)

            script_path = os.path.join('.', 'Main', 'main.py')
            self.process.start('python', ['-u', script_path])
            self.appendOutput("Process has been started.")
        else:
            self.appendOutput("Process has already been started.")

    def stopProcess(self):
        if self.isProcessStarted():
            self.process.write('exit\n'.encode())
            self.ui.inputTextFromCli.clear()

    def isProcessStarted(self):
        return self.process and self.process.state() == QProcess.ProcessState.Running

    def send_input(self):
        input_text = self.ui.inputTextFromCli.text() + '\n'
        if self.isProcessStarted():
            self.process.write(input_text.encode())
            self.ui.inputTextFromCli.clear()  # Clear the input field
        else:
            self.appendOutput(
                "The subprocess has been already terminated, please start the process in order to send message.")
            self.ui.inputTextFromCli.clear()

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
