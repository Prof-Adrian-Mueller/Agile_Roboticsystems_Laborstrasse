from PyQt6.QtWidgets import QApplication, QPushButton, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal, QObject

class SignalClass(QWidget):
    # Define a new signal called 'sendButtonClicked' that takes a single string argument.
    sendButtonClicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.input_line_edit = QLineEdit(self)
        self.input_line_edit.textChanged.connect(self.emitTextChanged)
        self.layout.addWidget(self.input_line_edit)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(lambda: self.sendButtonClicked.emit(self.input_line_edit.text()))
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)
        self.setWindowTitle('PyQt Signal example')
        self.show()

    def emitTextChanged(self, text):
        print(f'Text changed: {text}')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create an instance of the SignalClass.
        self.signal_class = SignalClass()

        # Connect the 'sendButtonClicked' signal to the target function.
        self.signal_class.sendButtonClicked.connect(self.target_function)

        self.setWindowTitle('PyQt Signal example')
        self.show()

    def target_function(self, text):
        print(f'Send button clicked! Text: {text}')

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
