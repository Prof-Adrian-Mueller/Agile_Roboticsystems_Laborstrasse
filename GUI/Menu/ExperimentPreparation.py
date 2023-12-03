from GUI.Custom.CustomDialog import ContentType, CustomDialog
from GUI.Navigation import Ui_MainWindow
from PyQt6.QtCore import pyqtSignal, QDate
import datetime

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'

from GUI.Storage.BorgSingleton import ExperimentSingleton


class ExperimentPreparation:
    """
    This is an Example comment.
    """
    sendButtonClicked = pyqtSignal(str)

    def __init__(self, ui: Ui_MainWindow, main_window):
        self.experiment_data = ExperimentSingleton()
        self.ui = ui
        self.main_window = main_window
        self.ui.experimentIdLE.textChanged.connect(self.checkExperimentID)
        self.dialog = CustomDialog(self.ui.centralwidget)

        # Set the datumLE to current Date
        today = datetime.datetime.today()
        qdate = QDate(today.year, today.month, today.day)
        self.ui.datumLE.setDate(qdate)

    def checkExperimentID(self, text):
        # TODO: check in db
        print(text)

    def nextPage(self):
        current_index = self.ui.vorbereitungStackedTab.currentIndex()
        if current_index < self.ui.vorbereitungStackedTab.count() - 1:
            self.ui.vorbereitungStackedTab.setCurrentIndex(current_index + 1)

    def nextPageWithControl(self, page_data):
        if page_data == 'CreateExperiment':
            # TODO: verify if plasmid exists
            print("weiter clicked " + page_data)
            # self.main_window.plasmidTubesList.displayPlasmidTubes("test")
            # self.nextPage()
            try:
                self.experiment_creation(page_data)
            except Exception as ex:
                display_msg = "Could not create Experiment.\n"
                self.main_window.dialogBoxContents.append(
                    self.main_window.dialog.addContent(f"{display_msg} {ex}", ContentType.OUTPUT))
                self.main_window.dialog.show()

        elif page_data == 'AddProbeToPlasmid':
            # TODO: add data to tubes table
            print("AddProbeToPlasmid")
            if self.check_duplicates(self.experiment_data.plasmid_tubes):
                display_msg = "Experiment has duplicates, please reenter!"
            else:
                display_msg = "No Duplicates!"
            self.main_window.dialogBoxContents.append(
                self.main_window.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))
            self.main_window.dialog.show()

    def prevPage(self):
        print("prev clicked")
        current_index = self.ui.vorbereitungStackedTab.currentIndex()
        if current_index > 0:
            self.ui.vorbereitungStackedTab.setCurrentIndex(current_index - 1)

    def check_duplicates(self, tubes):
        for key, value in tubes.items():
            if isinstance(value, list) and len(value) != len(set(value)):
                return True
        return False

    def experiment_creation(self, page_data):
        print("weiter clicked " + page_data)
        plasmid_list = [str(plasmid) for plasmid in self.ui.plasmidListEV_LE.text().split(',')]
        data = {
            "exp_id": self.ui.experimentIdLE.text(),
            "firstname": self.ui.nameLE.text(),
            "lastname": self.ui.vornameLE.text(),
            "anz_plasmid": self.ui.anzahlPlasmidLE.text(),
            "anz_tubes": self.ui.anzahlTubesLE.text(),
            "plasmid_list": plasmid_list,
            "date": self.ui.datumLE.date().getDate()
        }

        self.main_window.removeDialogBoxContents()

        # Check for empty fields
        emptyFields = [key for key, value in data.items() if not value]
        if emptyFields:
            self.main_window.dialogBoxContents.append(
                self.main_window.dialog.addContent(f"Eingabe Felder sollen nicht leer sein.", ContentType.OUTPUT))
            self.main_window.dialog.show()
            return

        # Check if 'anz_plasmid' and 'anz_tubes' are integers
        if not (data['anz_plasmid'].isdigit() and data['anz_tubes'].isdigit()):
            display_msg = "Anzahl Plasmid und Anzahl Tubes sollen Zahlen sein. Bitte Zahlen eingeben.\n"
            self.main_window.dialogBoxContents.append(
                self.main_window.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))
            self.main_window.dialog.show()
            return

        if int(data['anz_tubes']) % 2 != 0:
            display_msg = "Anzahl Tubes soll eine gerade Zahl sein.\n"
            self.main_window.dialogBoxContents.append(
                self.main_window.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))
            self.main_window.dialog.show()
            return

        if int(data['anz_tubes']) > 32 and int(data['anz_tubes']) > 32:
            display_msg = "Anzahl Tubes oder Anzahl Plasmid sollen nicht größer als 32 sein.\n"
            self.main_window.dialogBoxContents.append(
                self.main_window.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))
            self.main_window.dialog.show()
            return

        # Check if the count of plasmids matches 'anz_plasmid'
        if len(plasmid_list) != int(data['anz_plasmid']):
            display_msg = "Anzahl von Plasmid und Plasmid Liste stimmen nicht zu. \n"
            self.main_window.dialogBoxContents.append(
                self.main_window.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))
            self.main_window.dialog.show()
            return

        # Check if 'anz_plasmid' is not greater than 'anz_tubes'
        if int(data['anz_plasmid']) > int(data['anz_tubes']):
            display_msg = "Anzahl von Plasmid soll größer als Anzahl von Tubes sein.\n"
            self.main_window.dialogBoxContents.append(
                self.main_window.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))
            self.main_window.dialog.show()
            return

        # If all checks pass, go to the next page
        # Create empty list for each plasmid and saving in dict
        plasmid_dict = {plasmid: None for plasmid in plasmid_list}
        plasmid_dict = {plasmid: i for i, plasmid in enumerate(plasmid_list)}
        # Storing runtime Experiment data
        self.experiment_data = ExperimentSingleton(data['firstname'], data['lastname'], data['exp_id'], plasmid_list,
                                                   plasmid_dict, data['date'])
        self.main_window.plasmidTubesList.displayPlasmidTubes(plasmid_list)
        print(data)

        # self.main_window.ui_db.add_experiment()

        self.nextPage()

    def map_prev_next(self, ui):
        ui.vorbereitungPrev.clicked.connect(self.prevPage)
        ui.vorbereitungPrev_2.clicked.connect(self.prevPage)
        ui.vorbereitungPrev_4.clicked.connect(self.prevPage)
        ui.vorbereitungPrev_5.clicked.connect(self.prevPage)
        ui.vorbereitungNext.clicked.connect(
            lambda: self.nextPageWithControl("CreateExperiment"))
        ui.probe_to_plasmid_next.clicked.connect(
            lambda: self.nextPageWithControl("AddProbeToPlasmid"))
        ui.vorbereitungWeiter_2.clicked.connect(self.nextPage)
        ui.vorbereitungWeiter_3.clicked.connect(self.nextPage)
        ui.vorbereitungWeiter_6.clicked.connect(self.nextPage)
