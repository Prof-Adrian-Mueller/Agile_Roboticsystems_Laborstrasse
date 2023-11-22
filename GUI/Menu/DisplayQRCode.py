import os
import qrcode
from GUI.Navigation import Ui_MainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QApplication, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt
from GUI.Navigation import Ui_MainWindow


class DisplayQRCode(QWidget):
    def __init__(self, ui: Ui_MainWindow, main_window):
        super().__init__()
        self.ui = ui
        self.main_window = main_window


        scroll = QScrollArea(self)
        self.ui.qrCodesListForExp.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Disable horizontal scrolling

        frame = QFrame(scroll)
        scroll.setWidget(frame)
        self.outputLayout = QVBoxLayout(frame)


    def displayQrCode(self, number):
        pixmap = self.generate_qr_code(number)
        if pixmap is not None:
            layoutField = QLabel()
            layoutField.setPixmap(pixmap)
            self.appendOutput(layoutField, number)

    def generate_qr_code(self, number):
        # Check if the number is 6 digits
        if len(number) == 6 and number.isdigit():
            # Generate the QR code
            img = qrcode.make(number)

            # Create the directory if it doesn't exist
            if not os.path.exists("QRCodeImages"):
                os.makedirs("QRCodeImages")
                
            img.save(f"QRCodeImages/qrcode{number}.png")
            pixmap = QPixmap(f"QRCodeImages/qrcode{number}.png")
            pixmap_resized = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            return pixmap_resized
        else:
            print("Invalid number. Please enter a 6-digit number.")
            return None

    def appendOutput(self, label: QLabel,qrCodeNr):
        widget = QWidget()
        widget.setObjectName("displayQrCode")
        self.outputLayout.addWidget(widget)
        # Create the buttons and line edit
        speichern = QPushButton("Speichern")
        drucken = QPushButton("Drucken")
        plasmidNr = QLineEdit()
        plasmidNr.setPlaceholderText("Plasmid Nr eingeben")
        plasmidNr.setFixedWidth(120)
        qrCodeLabel = QLabel()
        qrCodeLabel.setObjectName("qrCodeLabel")
        qrCodeLabel.setText(qrCodeNr)
        h_layout = QHBoxLayout(widget)
        qrVerticalBox = QVBoxLayout()
        qrVerticalBox.addWidget(label)
        qrVerticalBox.addWidget(qrCodeLabel)
        # Create a QWidget and set the QVBoxLayout on it
        v_widget = QWidget()
        v_widget.setLayout(qrVerticalBox)
        # Add the QWidget to the QHBoxLayout
        h_layout.addWidget(v_widget)
        h_layout.addWidget(plasmidNr)
        h_layout.addWidget(speichern)
        h_layout.addWidget(drucken)


        

