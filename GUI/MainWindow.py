from multiprocessing import process
import subprocess
import sys
import typing
import os
from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QGroupBox, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidgetItem, QAbstractItemView,QHeaderView, QScrollArea, QFileDialog
from PyQt6.QtGui import QPainter, QPen, QIcon, QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QObject, QEvent, QTimer, QThread, QRect, QPoint
import pandas as pd
from GUI.CliInOutManager import CliInOutManager
from GUI.Custom.CustomDataTable import CustomDataTable
from GUI.Custom.CustomDragDropWidget import DragDropWidget
from GUI.Custom.ArrayOverlay import ArrowOverlay
from GUI.Custom.CustomTableWidget import CustomTableWidget
from GUI.Custom.CustomTitleBar import CustomTitleBar
from DBService.DBUIAdapter import DBUIAdapter
from GUI.Custom.CustomWidget import CustomWidget
from GUI.Custom.DummyDataGenerator import DummyDataGenerator
from GUI.CustomDialog import ContentType, CustomDialog
from GUI.ModalDialogAdapter import ModalDialogAdapter

from GUI.Navigation import Ui_MainWindow
import GUI.resource_rc
from Main.WorkerThread import WorkerThread
from PyQt6.QtCore import QProcess

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
        self.process = any
       
        self.ui_db = DBUIAdapter()

        self.worker_thread = WorkerThread()
        self.worker_thread.messageSignal.connect(self.handle_message)
        self.worker = WorkerThread()
        # self.worker.start()

        #Custom Titlebar
        title_bar = CustomTitleBar(self)
        self.setMenuWidget(title_bar)
        # Makes the window frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.dialogBoxContents = []

        #drag & drop
        self.ui.importAreaDragDrop.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        self.ui.importAreaDragDrop = DragDropWidget(self.ui.impotPage,self.ui_db)
        self.ui.importAreaDragDrop.setObjectName(u"dragdropwidget")
        self.ui.importAreaDragDrop.setGeometry(QRect(130, 90, 461, 261))
        self.ui.importAreaDragDrop.setStyleSheet(u"background-color:#666;")
        self.ui.chooseFileFromExplorer.clicked.connect(self.openFileDialog)

        #Custom ModalDialogBox
        self.dialog = CustomDialog(self.ui.modalDialogBackground)
        self.dialog.sendButtonClicked.connect(self.send_button_dialog_clicked)
        # self.dialogBox.hideDialog()

        self.apply_stylesheet()

        self.ui.homeBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.homePage)))
        self.ui.statistik.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.statistikPage)))
        self.ui.importBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.impotPage)))
        self.ui.qrGenBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.qrGenPage)))
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.settingsPage)))
        self.ui.cliBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.cliPage)))

        self.ui.generateQrBtn.clicked.connect(self.add_qr_generation_info)

        self.ui.startEnTBtn.clicked.connect(self.startEnTProcess)
        self.ui.plasmidMetaDataImport.clicked.connect(self.importPlasmidMetaDaten)

        widgetLiveLayout = QVBoxLayout(self.ui.widgetLive)  # Add a layout to your existing widget
        customWidget = CustomWidget(self.ui.widgetLive)  
        widgetLiveLayout.addWidget(customWidget)  # Add the custom widget to the layout of widgetLive

        #Cli stdin stdout
        self.cliManager = CliInOutManager(self.ui)
        self.ui.sendBtnInputFromCli.clicked.connect(self.cliManager.send_input)

        #Experiment Data
        experimentTableLayout = QVBoxLayout()
        generator = DummyDataGenerator()
        generator.generate_random_entries_experiment(15)
        df_exp = generator.to_dataframe_experiment()
        experimentDataTable = CustomDataTable(df_exp, self.ui.experimentView)
        experimentTableLayout.addWidget(experimentDataTable)
        self.ui.experimentView.setLayout(experimentTableLayout)

        plasmidTableLayout = QVBoxLayout()
        generator.generate_random_entries_plasmid(15)
        df_exp = generator.to_dataframe_plasmid()
        plasmidTable = CustomDataTable(df_exp, self.ui.plasmidMetadatenView)
        plasmidTableLayout.addWidget(plasmidTable)
        self.ui.plasmidMetadatenView.setLayout(plasmidTableLayout)

    def sendButtonClicked(self, text):
        print(f'Send button clicked! Text: {text}')
        
    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self.ui.centralwidget, "Open File", "", "Excel Files (*.xls *.xlsx)")
        if fileName:
            print(f'Selected file: {fileName}')
            try:
                # df = pd.read_excel(fileName)
                # TODO show message in dialogbox
                if self.dialogBoxContents.count:
                    self.dialog.removeItems(self.dialogBoxContents)
                print(f'Successfully imported Excel file: {fileName}')
                self.dialogBoxContents.append(self.dialog.addContent(f'Successfully imported Excel file: {fileName}', ContentType.OUTPUT))
                message = self.ui_db.insert_experiment_data(fileName)
                if message is not None:
                    displayMsg = " ".join(str(item) for item in message)
                else:
                    displayMsg = "No Display Text"
                self.dialogBoxContents.append(self.dialog.addContent(f"{displayMsg}", ContentType.OUTPUT))
              
            except Exception as e:
                print(f'Error occurred while importing Excel file: {fileName}\n{str(e)}')
                self.dialogBoxContents.append(self.dialog.addContent(f"Error occurred while importing Excel file: {fileName}", ContentType.OUTPUT))
                self.dialogBoxContents.append(self.dialog.addContent(f" {str(e)}", ContentType.OUTPUT))
            self.dialog.show()

    def eventFilter(self, source, event):
        if source == self.ui.tableWidgetLiveAction and event.type() == QEvent.Type.Resize:
            self.arrow_overlay.setGeometry(self.ui.tableWidgetLiveAction.geometry())
        return super().eventFilter(source, event)

    def startEnTProcess(self):
        #TODO Start monitoring app using python process
        
        if self.ui.startEnTBtn.text() == "Start":
            self.ui.startEnTBtn.setStyleSheet("QPushButton { background-color: red }")
            self.ui.startEnTBtn.setText("Stop")
            self.worker_thread.start()
                     
        else:
            self.ui.startEnTBtn.setStyleSheet("QPushButton { background-color: #45a049 }")
            self.worker_thread.stop_child_process()
            print("E&T process Terminated!")
            self.ui.startEnTBtn.setText("Start")

    def handle_message(self, message):
        # TODO show this message in display box
        print(message + " recieved from client")
        message_split = message.split()
        if message_split[0] == "INPUT":         
            if self.dialogBoxContents:
                print(self.dialogBoxContents)
                self.dialog.removeItems(self.dialogBoxContents)
            self.dialogBoxContents.append(self.dialog.addContent(f"Bitte {message_split[1]} eingeben: ", ContentType.INPUT))
            
            if not self.dialog.isVisible():
                self.dialog.show()

    def send_button_dialog_clicked(self):
        text = self.dialog.lineEditTextChanged
        self.worker_thread.send_message("ANZAHL_TUBES "+text)
        if self.dialogBoxContents:
            self.dialog.removeItems(self.dialogBoxContents)
        self.dialogBoxContents.append(self.dialog.addContent(f"Erfassung & Tracking gestartet mit {text} Tubes. \n ", ContentType.OUTPUT))
        return text
    
    def importPlasmidMetaDaten(self):
        fileName, _ = QFileDialog.getOpenFileName(self.ui.centralwidget, "Open File", "", "Excel Files (*.xls *.xlsx)")
        if fileName:
            print(f'Selected file: {fileName}')
            try:
                # df = pd.read_excel(fileName)
                # TODO show message in dialogbox
                if self.dialogBoxContents.count:
                    self.dialog.removeItems(self.dialogBoxContents)
                print(f'Successfully imported Excel file: {fileName}')
                self.dialogBoxContents.append(self.dialog.addContent(f'Successfully imported Excel file: {fileName}', ContentType.OUTPUT))
                message = self.ui_db.insert_metadaten(fileName)
                if message is not None:
                    displayMsg = " ".join(str(item) for item in message)
                else:
                    displayMsg = "No Display Text"
                self.dialogBoxContents.append(self.dialog.addContent(f"{displayMsg}", ContentType.OUTPUT))
              
            except Exception as e:
                print(f'Error occurred while importing Excel file: {fileName}\n{str(e)}')
                self.dialogBoxContents.append(self.dialog.addContent(f"Error occurred while importing Excel file: {fileName}", ContentType.OUTPUT))
                self.dialogBoxContents.append(self.dialog.addContent(f" {str(e)}", ContentType.OUTPUT))
    
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
        if data:
            qr_code_generated = "Folgende QR Codes sind generiert: \n" + "\n".join([f"{qr_code.qr_code} - {qr_code.datum}" for qr_code in data])
            self.ui.infoBoxQr.setText(qr_code_generated)
        else:
            self.ui.infoBoxQr.setText("No QR codes were generated.")
        self.ui.qrNrInputBox.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
