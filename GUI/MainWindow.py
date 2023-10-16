import sys
import typing
import os
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QObject, QEvent
from CustomTitleBar import CustomTitleBar

from Navigation import Ui_MainWindow
import resource_rc

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.homeBtn.setChecked(True)
        self.setWindowTitle("Dashboard GUI")
        self.setGeometry(100, 100, 800, 600)

        title_bar = CustomTitleBar(self)
        self.setMenuWidget(title_bar)
        # Make the window frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.apply_stylesheet()

        self.ui.homeBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.homePage)))
        self.ui.statistik.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.statistikPage)))
        self.ui.importBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.impotPage)))
        self.ui.qrGenBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.qrGenPage)))
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.settingsPage)))

        self.ui.generateQrBtn.clicked.connect(self.add_qr_generation_info)
        

    def apply_stylesheet(self):
        print(os.getcwd())
        if os.path.isfile('qt_designer/stylesheet/stylen.qss') and os.access('qt_designer/stylesheet/stylen.qss', os.R_OK):
            print("File exists and is readable")
            with open('qt_designer/stylesheet/stylen.qss', 'r') as file:
                stylesheet = file.read()
            self.setStyleSheet(stylesheet)
        else:
            print("Stylesheet File is either missing or not readable")

    def add_qr_generation_info(self):
        nrOfQr = self.ui.qrNrInputBox.text()
        self.ui.infoBoxQr.setText(f"{nrOfQr} QR Code Generated")
        self.ui.qrNrInputBox.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    

    sys.exit(app.exec())
