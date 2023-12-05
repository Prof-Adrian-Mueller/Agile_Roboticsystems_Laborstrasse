from DBService.DBUIAdapter import DBUIAdapter
from GUI.Custom.CustomDialog import ContentType, CustomDialog
from GUI.Menu.DisplayQRCode import DisplayQRCode
from GUI.Navigation import Ui_MainWindow
from PyQt6.QtCore import pyqtSignal, QDate
import datetime

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '03/12/2023'

from GUI.Storage.BorgSingleton import ExperimentSingleton


class ExperimentPreparation:
    """
    Experiment Preparation window functionalities.
    """
    sendButtonClicked = pyqtSignal(str)

    def __init__(self, ui: Ui_MainWindow, main_window):
        self.experiment_data = ExperimentSingleton()
        self.ui = ui
        self.main_window = main_window
        self.ui.experimentIdLE.editingFinished.connect(lambda: self.checkExperimentID(self.ui.experimentIdLE.text()))
        self.dialog = CustomDialog(self.ui.centralwidget)
        self.ui_database = DBUIAdapter()
        self.qr_code_generator = DisplayQRCode(self.ui, self.main_window)

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
            # self.main_window.removeDialogBoxContents()
            # self.nextPage()
            if self.check_duplicates(self.experiment_data.plasmid_tubes):
                display_msg = "Experiment has duplicates, please reenter!"
                self.show_message_in_dialog(display_msg)
            else:
                display_msg = "All the values look good.\n"
                count_tubes = []
                try:
                    for plasmid, tubes_list in self.experiment_data.plasmid_tubes.items():
                        self.ui_database.adapter.insert_tubes(tubes_list, self.experiment_data.experiment_id, plasmid)
                        print(plasmid + " - " + ', '.join(map(str, tubes_list)))
                        display_msg += f"Created Tubes successfully for \n{plasmid} : {tubes_list}. \n"
                        count_tubes.append(tubes_list)
                        print(plasmid + " - " + ', '.join(map(str, self.ui_database.adapter.get_all_tubes())))
                        self.main_window.custom_live_widget.display_tubes_data()
                    # qr_codes_list = self.ui_database.adapter.get_next_qr_codes(len(count_tubes))
                    # for qr_code in qr_codes_list:
                    #     print(qr_code)

                except Exception as ex:
                    display_msg = f"Could not create tubes. \n{ex}"
                self.nextPage()
                self.show_message_in_dialog(display_msg)

    def show_message_in_dialog(self, display_msg):
        self.main_window.dialogBoxContents.append(
            self.main_window.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))
        self.main_window.dialog.show()

    def prevPage(self):
        print("prev clicked")
        current_index = self.ui.vorbereitungStackedTab.currentIndex()
        if current_index > 0:
            self.ui.vorbereitungStackedTab.setCurrentIndex(current_index - 1)

    def check_duplicates(self, tubes):
        flat_list = []
        for key, value in tubes.items():
            if isinstance(value, list):
                flat_list.extend(value)
            else:
                flat_list.append(value)
        return len(flat_list) != len(set(flat_list))

    def experiment_creation(self, page_data):
        # Clear Cache before saving
        self.experiment_data.clear_cache()
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
        empty_fields = [key for key, value in data.items() if not value]
        if empty_fields:
            self.show_message_in_dialog(f"Eingabe Felder sollen nicht leer sein.")
            return

        # Check if 'anz_plasmid' and 'anz_tubes' are integers
        if not (data['anz_plasmid'].isdigit() and data['anz_tubes'].isdigit()):
            display_msg = "Anzahl Plasmid und Anzahl Tubes sollen Zahlen sein. Bitte Zahlen eingeben.\n"
            self.show_message_in_dialog(display_msg)
            return

        if int(data['anz_tubes']) % 2 != 0:
            display_msg = "Anzahl Tubes soll eine gerade Zahl sein.\n"
            self.show_message_in_dialog(display_msg)
            return

        if int(data['anz_tubes']) > 32 and int(data['anz_tubes']) > 32:
            display_msg = "Anzahl Tubes oder Anzahl Plasmid sollen nicht größer als 32 sein.\n"
            self.show_message_in_dialog(display_msg)
            return

        # Check if the count of plasmids matches 'anz_plasmid'
        if len(plasmid_list) != int(data['anz_plasmid']):
            display_msg = "Anzahl von Plasmid und Plasmid Liste stimmen nicht zu. \n"
            self.show_message_in_dialog(display_msg)
            return

        # Check if 'anz_plasmid' is not greater than 'anz_tubes'
        if int(data['anz_plasmid']) > int(data['anz_tubes']):
            display_msg = "Anzahl von Plasmid soll größer als Anzahl von Tubes sein.\n"
            self.show_message_in_dialog(display_msg)
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
