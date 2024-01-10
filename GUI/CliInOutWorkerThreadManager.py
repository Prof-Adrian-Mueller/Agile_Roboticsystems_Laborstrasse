from collections import deque

from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QApplication, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from GUI.Navigation import Ui_MainWindow
import sys
import os

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'

from GUI.Utils.LiveObservable import MessageDisplay
from GUI.Utils.LiveObservable import LiveObservable
from GUI.Utils.LiveViewMessageDisplay import LiveViewMessageDisplay


class CliInOutWorkerThreadManager(QWidget):
    """
    Standard Input/Output/Error redirection to GUI.
    """

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

        # Creating Observable
        self.message_service = LiveObservable()

        # Creating Observers
        display = LiveViewMessageDisplay()

        # Registering the Observer
        self.message_service.register_observer(display)

        # Max 20 Messages will be shown
        self.total_messages_displayed = deque(maxlen=20)

    def displayDefault(self, message):
        self.defaultWidget = QWidget()
        self.defaultWidget.setObjectName("clioutputwidgetdesign")
        self.outputLayout.addWidget(self.defaultWidget)
        h_layout = QHBoxLayout(self.defaultWidget)

        self.defaultLabel = QLabel(message)
        self.defaultLabel.setWordWrap(True)
        h_layout.addWidget(self.defaultLabel)

    def startProcess(self, nr_of_tubes):
        """
        Start the monitoring application.
        """
        if not self.isProcessStarted():
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self.normalOutputWritten)
            self.process.readyReadStandardError.connect(self.errorOutputWritten)

            # Path to your script
            script_path = os.path.join('.', 'Main', 'main.py')
            # Get the current directory
            current_dir = os.getcwd()
            # Construct the path to the virtual environment's Python executable
            venv_python_path = os.path.join(current_dir, 'venv', 'Scripts', 'python')
            # Start the process with the venv Python
            self.process.start(venv_python_path, ['-u', script_path, nr_of_tubes])

            for i in range(1, 50):
                self.appendOutput(f"Count : {i}")
        # else:
        #     self.appendOutput("Process has already been started.")

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
        """
        Appends text to CLI Interface on GUI.
        """
        # Add the new message to the deque
        self.total_messages_displayed.append(text)

        # If the maximum number of messages has been reached, remove the oldest message
        if len(self.total_messages_displayed) == self.total_messages_displayed.maxlen:
            widget = self.outputLayout.itemAt(0).widget()
            self.outputLayout.removeWidget(widget)
            widget.deleteLater()

        widget = QWidget()
        widget.setObjectName("clioutputwidgetdesign")
        self.outputLayout.addWidget(widget)
        h_layout = QHBoxLayout(widget)

        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # Enables text selection
        h_layout.addWidget(label)

        clipboard = QApplication.clipboard()
        clipboard.setText(label.text())

    def normalOutputWritten(self):
        """
        Display output text on CLI GUI
        """
        try:
            output = self.process.readAllStandardOutput().data().decode().strip()
            if output.startswith("LIVE"):
                message = output[len("LIVE "):].strip()
                self.message_service.notify_observers(message)
            elif output.startswith("RESULT"):
                message = output[len("RESULT "):].strip()
                self.message_service.notify_observers(message)
            elif len(output) < 1:
                pass
            else:
                self.appendOutput(output)
        except Exception as ex:
            print(ex)

    def errorOutputWritten(self):
        """
        Display error text on CLI GUI
        """
        output = self.process.readAllStandardError().data().decode().strip()
        if output:
            if output.startswith("LIVE"):
                print(f"It has {output.split()[0]} Data")
            else:
                self.appendOutput(output)
