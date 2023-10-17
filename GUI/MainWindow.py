import sys
import typing
import os
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QObject, QEvent
from GUI.Custom.CustomTitleBar import CustomTitleBar
from DBService.DBUIAdapter import DBUIAdapter
from GUI.ModalDialogAdapter import ModalDialogAdapter

from GUI.Navigation import Ui_MainWindow
import GUI.resource_rc

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #UI Mainwindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.homeBtn.setChecked(True)
        self.setWindowTitle("Dashboard GUI")
        self.setGeometry(100, 100, 800, 600)

        self.ui_db = DBUIAdapter()

        #Custom Titlebar
        title_bar = CustomTitleBar(self)
        self.setMenuWidget(title_bar)
        # Makes the window frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        #Custom ModalDialogBox
        dialogBox = ModalDialogAdapter(self,self.ui)

        self.apply_stylesheet()

        self.ui.homeBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.homePage)))
        self.ui.statistik.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.statistikPage)))
        self.ui.importBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.impotPage)))
        self.ui.qrGenBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.qrGenPage)))
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.settingsPage)))

        self.ui.generateQrBtn.clicked.connect(self.add_qr_generation_info)
        

    def apply_stylesheet(self):
        print(os.getcwd())
        if os.path.isfile('GUI/stylesheet/stylen.qss') and os.access('GUI/stylesheet/stylen.qss', os.R_OK):
            print("File exists and is readable")
            with open('GUI/stylesheet/stylen.qss', 'r') as file:
                stylesheet = file.read()
            self.setStyleSheet(stylesheet)
        else:
            print("Stylesheet File is either missing or not readable")

    def add_qr_generation_info(self):
        
        nrOfQr = self.ui.qrNrInputBox.text()
        data = self.ui_db.create_qr_code(int(nrOfQr))
        qr_code_generated = "Folgende QR Codes sind generiert: \n"
        for qr_code in data:
            qr_code_generated += str(qr_code.qr_code) + " - "+ str(qr_code.datum)+"\n"
        self.ui.infoBoxQr.setText(f"{qr_code_generated} ")
        self.ui.qrNrInputBox.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    

    sys.exit(app.exec())
