import os
import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QEvent, QRect
from PyQt6.QtWidgets import QSizePolicy, QApplication, QMainWindow, QVBoxLayout, \
    QFileDialog
from PyQt6.QtWidgets import QWidget

from DBService.DBUIAdapter import DBUIAdapter
from GUI.CliInOutWorkerThreadManager import CliInOutWorkerThreadManager
from GUI.Custom.CustomDataTable import CustomDataTable
from GUI.Custom.CustomDragDropWidget import DragDropWidget
from GUI.Custom.CustomTitleBar import CustomTitleBar
from GUI.Custom.CustomWidget import CustomWidget
from GUI.Custom.DummyDataGenerator import DummyDataGenerator
from GUI.Custom.CustomDialog import ContentType, CustomDialog
from GUI.LeftNavigation import LeftNavigation
from GUI.Menu.DisplayPlasmidTubes import DisplayPlasmidTubes
from GUI.Menu.DisplayQRCode import DisplayQRCode
from GUI.Menu.ExperimentPreparation import ExperimentPreparation
from GUI.Menu.Settings import Settings
from GUI.Navigation import Ui_MainWindow
from GUI.ResizeGripWidget import ResizeGripWidget

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class MainWindow(QMainWindow):
    """
    This is the Main Window for all the Graphical User Interface to Work and bind together. Most of the Initializations are stated here.
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        # UI Mainwindow Configuration
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.homeBtn.setChecked(True)
        self.setWindowTitle("Dashboard GUI")
        self.resizeGrip = ResizeGripWidget(self)
        self.resizeGrip.setGeometry(self.width() - 16, self.height() - 16, 16, 16)
        self.resizeGrip.show()
        self.apply_stylesheet()

        # self.setGeometry(100, 100, 800, 600)
        self.process = any

        # Database Service Connection Adapter
        self.ui_db = DBUIAdapter()

        # Custom Titlebar
        title_bar = CustomTitleBar(self)
        self.setMenuWidget(title_bar)
        self.setWindowTitle("Dashboard UI")

        # Save all the contents of the dialog box, before adding anything , it is better idea to remove contents
        # which are saved here
        self.dialogBoxContents = []

        # drag & drop import concept
        self.ui.importAreaDragDrop.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        self.ui.importAreaDragDrop = DragDropWidget(self.ui.importPage, self.ui_db)
        self.ui.importAreaDragDrop.setObjectName(u"dragdropwidget")
        self.ui.importAreaDragDrop.setGeometry(QRect(130, 90, 461, 261))
        self.ui.importAreaDragDrop.setStyleSheet(u"background-color:#666;")
        self.ui.chooseFileFromExplorer.clicked.connect(self.openFileDialog)

        # Custom ModalDialogBox
        self.dialog = CustomDialog(self)
        self.dialog.sendButtonClicked.connect(self.send_button_dialog_clicked)
        # self.dialogBox.hideDialog()

        left_navigation = LeftNavigation(self.ui)
        left_navigation.map_buttons_to_pages()

        self.ui.generateQrBtn.clicked.connect(self.add_qr_generation_info)

        self.ui.startEnTBtn.clicked.connect(self.startEnTProcess)

        # Live view widget
        widget_live_layout = QVBoxLayout(self.ui.widgetLive)
        custom_widget = CustomWidget(self.ui.widgetLive)
        widget_live_layout.addWidget(custom_widget)

        # Cli stdin stdout
        self.cliInOutWorkerThreadManager = CliInOutWorkerThreadManager(self.ui)
        self.ui.sendBtnInputFromCli.clicked.connect(self.cliInOutWorkerThreadManager.send_input)

        # Experiment Data
        experiment_table_layout = QVBoxLayout()
        generator = DummyDataGenerator()
        generator.generate_random_entries_experiment(15)
        df_exp = generator.to_dataframe_experiment()
        experiment_data_table = CustomDataTable(df_exp, self.ui.experimentView)
        experiment_table_layout.addWidget(experiment_data_table)
        self.ui.experimentView.setLayout(experiment_table_layout)

        plasmid_table_layout = QVBoxLayout()
        generator.generate_random_entries_plasmid(15)
        df_exp = generator.to_dataframe_plasmid()
        plasmid_table = CustomDataTable(df_exp, self.ui.plasmidMetadatenView)
        plasmid_table_layout.addWidget(plasmid_table)
        self.ui.plasmidMetadatenView.setLayout(plasmid_table_layout)

        # settings
        self.settings = Settings(self.ui, self)
        self.ui.windowResizeSlider.valueChanged.connect(self.settings.resize_window)

        # ExperimentPreparation Pages
        self.experiment_preparation = ExperimentPreparation(self.ui, self)
        self.experiment_preparation.map_prev_next(self.ui)

        # Display Plasmid Tubes
        self.plasmidTubesList = DisplayPlasmidTubes(self.ui, self)

        self.ui.experimentImportierenVorbereitung.clicked.connect(lambda: self.openFileDialog('experiment'))
        self.ui.importPlasmidMetadaten.clicked.connect(lambda: self.openFileDialog('plasmid'))
        self.ui.plasmidMetaDataImport.clicked.connect(lambda: self.openFileDialog('plasmid'))

        # Display QR Codes
        qr_code_display = DisplayQRCode(self.ui, self)
        qr_data = self.ui_db.adapter.get_next_qr_codes(8)
        for qrElem in qr_data:
            qr_code_display.displayQrCode(qrElem[0])

    def set_expanding_size_policy(self, widget):
        """
        Set the size policy of all child widgets of 'widget' to Expanding.
        """
        for child in widget.findChildren(QWidget):
            child.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def removeDialogBoxContents(self):
        """
        Removes all the Contents of the Dialog Box. It is better to call this method before showing new contents in the Box.
        """
        if self.dialogBoxContents.count:
            self.dialog.removeItems(self.dialogBoxContents)

    def openFileDialog(self, file_type):
        """
        Shows a Window File Selector UI Widget to select an Excel File to be imported.
        """
        file_name, _ = QFileDialog.getOpenFileName(self.ui.centralwidget, "Open File", "", "Excel Files (*.xls *.xlsx)")
        if file_name:
            print(f'Selected file: {file_name}')
            try:
                # df = pd.read_excel(file_name)
                # TODO show message in dialogbox
                self.removeDialogBoxContents()

                if file_type == 'experiment':
                    message = self.ui_db.insert_experiment_data(file_name)
                elif file_type == 'plasmid':
                    message = self.ui_db.insert_metadaten(file_name)
                if message is not None:
                    display_msg = " ".join(str(item) for item in message)
                else:
                    display_msg = "No Display Text"
                self.dialogBoxContents.append(self.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))

            except Exception as e:
                print(f'Error occurred while importing Excel file: {file_name}\n{str(e)}')
                self.dialogBoxContents.append(
                    self.dialog.addContent(f"Error occurred while importing Excel file: {file_name}",
                                           ContentType.OUTPUT))
                self.dialogBoxContents.append(self.dialog.addContent(f" {str(e)}", ContentType.OUTPUT))
            finally:
                print(f'Successfully imported Excel file: {file_name}')
                self.dialogBoxContents.append(
                    self.dialog.addContent(f'Successfully imported Excel file: {file_name}', ContentType.OUTPUT))
            self.dialog.show()

    def eventFilter(self, source, event):
        if source == self.ui.tableWidgetLiveAction and event.type() == QEvent.Type.Resize:
            self.arrow_overlay.setGeometry(self.ui.tableWidgetLiveAction.geometry())
        return super().eventFilter(source, event)

    def startEnTProcess(self):
        """
        Start the Monitoring App, change button color on the current situation of the Process.
        """
        # TODO Start monitoring app using python process

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
            self.dialogBoxContents.append(
                self.dialog.addContent(f"Bitte {message_split[1]} eingeben: ", ContentType.INPUT))

            if not self.dialog.isVisible():
                self.dialog.show()

    def send_button_dialog_clicked(self):
        text = self.dialog.lineEditTextChanged
        self.worker_thread.send_message("ANZAHL_TUBES " + text)
        if self.dialogBoxContents:
            self.dialog.removeItems(self.dialogBoxContents)
        self.dialogBoxContents.append(
            self.dialog.addContent(f"Erfassung & Tracking gestartet mit {text} Tubes. \n ", ContentType.OUTPUT))
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
                self.dialogBoxContents.append(
                    self.dialog.addContent(f'Successfully imported Excel file: {fileName}', ContentType.OUTPUT))
                message = self.ui_db.insert_metadaten(fileName)
                if message is not None:
                    displayMsg = " ".join(str(item) for item in message)
                else:
                    displayMsg = "No Display Text"
                self.dialogBoxContents.append(self.dialog.addContent(f"{displayMsg}", ContentType.OUTPUT))

            except Exception as e:
                print(f'Error occurred while importing Excel file: {fileName}\n{str(e)}')
                self.dialogBoxContents.append(
                    self.dialog.addContent(f"Error occurred while importing Excel file: {fileName}",
                                           ContentType.OUTPUT))
                self.dialogBoxContents.append(self.dialog.addContent(f" {str(e)}", ContentType.OUTPUT))

    def apply_stylesheet(self):
        """
        Load Stylesheet from the file and implement it to the UI.
        """
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
            qr_code_generated = "Folgende QR Codes sind generiert: \n" + "\n".join(
                [f"{qr_code.qr_code} - {qr_code.datum}" for qr_code in data])
            self.ui.infoBoxQr.setText(qr_code_generated)
        else:
            self.ui.infoBoxQr.setText("No QR codes were generated.")
        self.ui.qrNrInputBox.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
