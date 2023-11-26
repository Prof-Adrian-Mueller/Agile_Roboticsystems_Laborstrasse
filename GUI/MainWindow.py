from multiprocessing import process
import subprocess
import sys
import typing
import os
from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QGroupBox, QApplication, QMainWindow, QWidget, QVBoxLayout,QGridLayout, QStackedWidget, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidgetItem, QAbstractItemView,QHeaderView, QScrollArea, QFileDialog
from PyQt6.QtGui import QPainter, QPen, QIcon, QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QObject, QEvent, QTimer, QThread, QRect, QPoint
import pandas as pd
from GUI.CliInOutWorkerThreadManager import CliInOutWorkerThreadManager
from GUI.Custom.CustomDataTable import CustomDataTable
from GUI.Custom.CustomDragDropWidget import DragDropWidget
from GUI.Custom.ArrayOverlay import ArrowOverlay
from GUI.Custom.CustomTableWidget import CustomTableWidget
from GUI.Custom.CustomTitleBar import CustomTitleBar
from DBService.DBUIAdapter import DBUIAdapter
from GUI.Custom.CustomWidget import CustomWidget
from GUI.Custom.DummyDataGenerator import DummyDataGenerator
from GUI.CustomDialog import ContentType, CustomDialog
from GUI.Menu.DisplayQRCode import DisplayQRCode
from GUI.Menu.ExperimentVorbereitung import ExperimentVorbereitung
from GUI.Menu.Settings import Settings
from GUI.ModalDialogAdapter import ModalDialogAdapter

from GUI.Navigation import Ui_MainWindow
import GUI.resource_rc
from PyQt6.QtCore import QProcess

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #UI Mainwindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.central_widget = QWidget()
        # self.setCentralWidget(self.central_widget)
        # layout = QVBoxLayout(self.central_widget) 

        # layout.addWidget(self.ui.stackedWidget)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.homeBtn.setChecked(True)
        self.setWindowTitle("Dashboard GUI")
        # self.setWindowFlags(Qt.Window)
        self.showMaximized()
        self.setCentralWidget(self.ui.centralwidget)
        
        # self.setGeometry(100, 100, 800, 600)
        self.process = any
       
        self.ui_db = DBUIAdapter()
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
        self.cliInOutWorkerThreadManager = CliInOutWorkerThreadManager(self.ui)
        self.ui.sendBtnInputFromCli.clicked.connect(self.cliInOutWorkerThreadManager.send_input)

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

        #settings
        self.settings = Settings(self.ui, self)
        self.ui.windowResizeSlider.valueChanged.connect(self.settings.resize_window)
         
        #ExperimentVorbereitung Pages
        self.experimentVorbereitung = ExperimentVorbereitung(self.ui, self)
        self.ui.vorbereitungPrev.clicked.connect(self.experimentVorbereitung.prevPage)
        self.ui.vorbereitungPrev_2.clicked.connect(self.experimentVorbereitung.prevPage)
        self.ui.vorbereitungPrev_4.clicked.connect(self.experimentVorbereitung.prevPage)
        self.ui.vorbereitungPrev_5.clicked.connect(self.experimentVorbereitung.prevPage)
        self.ui.vorbereitungNext.clicked.connect(self.experimentVorbereitung.nextPage)
        self.ui.vorbereitungWeiter_2.clicked.connect(self.experimentVorbereitung.nextPage)
        self.ui.vorbereitungWeiter_3.clicked.connect(self.experimentVorbereitung.nextPage)
        self.ui.vorbereitungWeiter_5.clicked.connect(self.experimentVorbereitung.nextPage)
        self.ui.vorbereitungWeiter_6.clicked.connect(self.experimentVorbereitung.nextPage)

        self.ui.experimentImportierenVorbereitung.clicked.connect(lambda: self.openFileDialog('experiment'))
        self.ui.importPlasmidMetadaten.clicked.connect(lambda: self.openFileDialog('plasmid'))

        #Display QR Codes
        qrCodeDisplay = DisplayQRCode(self.ui, self)
        qrData = self.ui_db.adapter.get_next_qr_codes(8)
        for qrElem in qrData:
            qrCodeDisplay.displayQrCode(qrElem[0])

    def resizeEvent(self, event):
        if self.ui.centralwidget is not None:
            try:
                self.ui.centralwidget.adjustSize()
            except RuntimeError as e:
                print("Error adjusting size:", e)
        super().resizeEvent(event)

        
    def openFileDialog(self, fileType):
        fileName, _ = QFileDialog.getOpenFileName(self.ui.centralwidget, "Open File", "", "Excel Files (*.xls *.xlsx)")
        if fileName:
            print(f'Selected file: {fileName}')
            try:
                # df = pd.read_excel(fileName)
                # TODO show message in dialogbox
                if self.dialogBoxContents.count:
                    self.dialog.removeItems(self.dialogBoxContents)
               
                if fileType == 'experiment':
                    message = self.ui_db.insert_experiment_data(fileName)
                elif fileType == 'plasmid':
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
            finally:
                print(f'Successfully imported Excel file: {fileName}')
                self.dialogBoxContents.append(self.dialog.addContent(f'Successfully imported Excel file: {fileName}', ContentType.OUTPUT))
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
            self.cliInOutWorkerThreadManager.displayDefault("Process has been started.")
            self.cliInOutWorkerThreadManager.startProcess()
                     
        else:
            self.ui.startEnTBtn.setStyleSheet("QPushButton { background-color: #45a049 }")
            self.cliInOutWorkerThreadManager.stopProcess()
            self.cliInOutWorkerThreadManager.displayDefault("Process has been stopped.")
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
