import traceback

from DBService.DBUIAdapter import DBUIAdapter
from GUI.Custom.CustomDialog import ContentType, CustomDialog
from GUI.Custom.CustomLiveWidget import CustomLiveWidget
from GUI.Menu.ExperimentPreparationWidget import ExperimentPreparationWidget
from GUI.Menu.QRCodesWidget import QRCodesWidget
from GUI.Navigation import Ui_MainWindow
from PyQt6.QtCore import pyqtSignal, QDate
import datetime

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '03/12/2023'

from GUI.Storage.BorgSingleton import ExperimentSingleton, TubesSingleton, CurrentExperimentSingleton, \
    MainWindowSingleton
from GUI.Utils.CheckUtils import CheckUtils


class ExperimentPreparation:
    """
    Experiment Preparation window functionalities.
    """
    sendButtonClicked = pyqtSignal(str)

    def __init__(self, ui: Ui_MainWindow, main_window):
        self.is_current_experiment = False
        self.tube_information = TubesSingleton()
        self.experiment_data = ExperimentSingleton()
        self.ui = ui
        self.main_window = main_window
        self.ui.experimentIdLE.editingFinished.connect(lambda: self.checkExperimentID(self.ui.experimentIdLE.text()))
        self.ui.nameLE.editingFinished.connect(lambda: self.create_experiment_id(self.ui.nameLE.text()))
        self.dialog = CustomDialog(self.ui.centralwidget)
        self.ui_database = main_window.ui_db
        self.current_experiment = None

        # Set the datumLE to current Date
        today = datetime.datetime.today()
        qdate = QDate(today.year, today.month, today.day)
        self.ui.datumLE.setDate(qdate)

    def create_experiment_id(self, text):
        try:
            exp_id_data = self.ui_database.adapter.get_experiment_by_id(text)
            print(exp_id_data)
        except Exception as ex:
            print(ex)

    def checkExperimentID(self, exp_id):
        # TODO: check in db
        try:
            exp_id_data = self.ui_database.adapter.get_experiment_by_id(exp_id)
            plasmids = self.ui_database.get_plasmids_for_experiment(exp_id)
            if exp_id_data:
                all_experiments = self.ui_database.get_all_experiments()
                last_exp_id = all_experiments[-1].exp_id
                self.check_if_current_experiment(exp_id, last_exp_id)

                self.ui.nameLE.setText(exp_id_data.name)
                self.ui.vornameLE.setText(exp_id_data.vorname)
                self.ui.anzahlTubesLE.setText(str(exp_id_data.anz_tubes))
                self.ui.anzahlPlasmidLE.setText(str(exp_id_data.anz_plasmid))
                # Convert a date string to a datetime.date object
                date = datetime.datetime.strptime(exp_id_data.datum, '%Y-%m-%d').date()
                # Convert a datetime.date to QDate
                qdate = QDate(date.year, date.month, date.day)
                # Set the date of the QDateEdit widget
                self.ui.datumLE.setDate(qdate)
                print(exp_id_data)
                if plasmids:
                    plasmid_list = list(set(plasmids))
                    plasmid_string = ','.join(plasmid_list)
                    self.ui.plasmidListEV_LE.setText(plasmid_string)

        except Exception as ex:
            print(ex)

    def check_if_current_experiment(self, exp_id, current_exp_id):
        if exp_id == current_exp_id:
            print(f"Experiment ID {exp_id} is the latest one.")
            self.is_current_experiment = True
        else:
            dialog = CustomDialog(self.main_window)
            dialog.add_titlebar_name("Experiment Update Message")
            dialog.addContent(
                f"Die Experiment-ID {exp_id} ist nicht die neueste. Die neueste ID lautet {current_exp_id}.",
                ContentType.ERROR)
            dialog.addContent(f"Sie dürfen nur das aktuelle Experiment aktualisieren.", ContentType.ERROR)
            self.is_current_experiment = False
            dialog.show()

    def nextPage(self):
        current_index = self.ui.vorbereitungStackedTab.currentIndex()
        if current_index < self.ui.vorbereitungStackedTab.count() - 1:
            self.ui.vorbereitungStackedTab.setCurrentIndex(current_index + 1)

    def nextPageWithControl(self, page_data):
        global live_widget
        if page_data == 'CreateExperiment':
            # TODO: verify if plasmid exists
            try:
                self.experiment_creation(page_data)
            except Exception as ex:
                display_msg = "Could not create Experiment.\n"
                self.main_window.dialogBoxContents.append(
                    self.main_window.dialog.addContent(f"{display_msg} {ex}", ContentType.OUTPUT))
                self.main_window.dialogBoxContents.append(
                    self.main_window.dialog.addContent(f"{traceback.format_exc()}", ContentType.OUTPUT))
                self.main_window.dialog.show()

        elif page_data == 'AddProbeToPlasmid':
            print("AddProbeToPlasmid")
            self.tube_information.clear_cache()
            self.main_window.removeDialogBoxContents()

            if self.check_duplicates(self.experiment_data.plasmid_tubes):
                display_msg = "Experiment has duplicates, please re-enter!"
                self.show_message_in_dialog(display_msg)

            else:
                dialog = CustomDialog(self.main_window)
                dialog.add_titlebar_name("Experimenttubes Details")
                count_tubes = []

                try:
                    # available_tubes = self.ui_database.available_qrcode(self.current_experiment.experiment_id, )
                    all_input_tubes = []
                    for plasmid, tubes_list in self.experiment_data.plasmid_tubes.items():

                        # for tube in tubes_list:
                        #     all_input_tubes.append(int(tube))
                        #     if tube not in available_tubes:
                        #         dialog.addContent(f"{tube} ist nicht verfügbar für {plasmid}", ContentType.ERROR)
                        #         dialog.show()
                        #         return

                        if not CheckUtils.is_last_sequence_in_order(tubes_list):
                            dialog.addContent(f"{tubes_list} sind nicht in einer Reihenfolge für Plasmid {plasmid}",
                                              ContentType.ERROR)
                            dialog.addContent(
                                f"Geben Sie bitte die Tube Nr in einer Reihenfolge ein, wie z.B. 1,2,3",
                                ContentType.OUTPUT)
                            dialog.show()
                            return

                    # if len(available_tubes) != len(all_input_tubes):
                    #     dialog.addContent(f"Verfügbare Tubes und Eingegebene Tubes sind nicht gleich.", ContentType.ERROR)
                    #     dialog.show()
                    #     return

                    for plasmid, tubes_list in self.experiment_data.plasmid_tubes.items():
                        try:
                            self.ui_database.insert_tubes(tubes_list, self.experiment_data.experiment_id, plasmid)
                            display_msg = f"Created Tubes successfully for {plasmid} : {tubes_list}. \n"
                            dialog.addContent(f"{display_msg}", ContentType.OUTPUT)
                            count_tubes.append(tubes_list)
                        except Exception as ex:
                            dialog.addContent(f"{ex}", ContentType.OUTPUT)
                            count_tubes.append(tubes_list)

                    tube_info_data = self.ui_database.adapter.get_tubes_by_exp_id(self.experiment_data.experiment_id)
                    probe_list = []
                    for tube in tube_info_data:
                        self.tube_information.add_tube(tube['probe_nr'], tube['qr_code'],
                                                       tube['plasmid_nr'])
                        probe_list.append(tube['qr_code'])

                    self.main_window.qr_codes_widget.refresh_data()
                    self.main_window.experiment_dashboard.refresh_data()
                    # TODO layout anpassen
                    # qr_codes_list = self.ui_database.adapter.get_next_qr_codes(len(count_tubes))
                    # for qr_code in qr_codes_list:
                    #     print(qr_code)

                except Exception as ex:
                    display_msg = f"Could not create tubes. \n{ex}"
                    dialog.addContent(f"{display_msg}", ContentType.OUTPUT)
                    return

                # self.nextPage()
                # Load back dashboard
                display_msg = "Prima! Alle Daten sehen Gut aus."
                dialog.addContent(f"{display_msg}", ContentType.OUTPUT)
                dialog.show()
                experiment_preparation_widget = ExperimentPreparationWidget(self.ui.vorbereitungStackedTab,
                                                                            self.ui.test_page_home)
                experiment_preparation_widget.reset_input_of_past_experiments()
                experiment_preparation_widget.removeFromMainWindow(self.main_window)
                # load start ent app
                self.main_window.home_dashboard.show_start_button()
                self.main_window.home_dashboard.add_other_page_nav_btns()

                # load live view
                # Add CustomLiveWidget to the layout if it doesn't exist
                current_exp = CurrentExperimentSingleton()
                self.main_window.home_dashboard.nr_of_tubes = str(
                    len(self.ui_database.get_tubes_by_exp_id(current_exp.experiment_id)))

                # Use the existing MainWindowSingleton instance
                main_win_singleton = MainWindowSingleton()

                # Determine the correct main window to use
                main_window = main_win_singleton.main_window if main_win_singleton.main_window else self.main_window

                # Check if the "Live" tab already exists
                live_tab_found = False
                for index in range(main_window.tab_widget_home_dashboard.count()):
                    if main_window.tab_widget_home_dashboard.tabText(index) == "Live":
                        live_tab_found = True
                        break

                # If "Live" tab does not exist, create and add it
                if not live_tab_found:
                    live_widget = CustomLiveWidget(self.ui.test_page_home, main_window)
                    main_window.tab_widget_home_dashboard.addTab(live_widget, "Live")
                    live_index = main_window.tab_widget_home_dashboard.indexOf(live_widget)
                    main_win_singleton.add_stacked_tab_index("live", live_index)

                # Load and display tube information if the "Live" tab is added
                if not live_tab_found and tube_info_data:
                    tube_info_data = self.ui_database.adapter.get_tubes_by_exp_id(self.experiment_data.experiment_id)
                    if tube_info_data:
                        live_widget.display_tubes_data(tube_info_data)
                        live_widget.refresh_data()

    def show_message_in_dialog(self, display_msg):
        self.main_window.dialog.add_titlebar_name("Experiment Vorbereitung")
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
        global exp_data, all_tubes_of_exp
        # Clear Cache before saving
        self.experiment_data.clear_cache()

        plasmid_list = [str(plasmid) for plasmid in self.ui.plasmidListEV_LE.text().split(',')]
        # If all checks pass, go to the next page
        # Create empty list for each plasmid and saving in dict
        plasmid_dict = {plasmid: None for plasmid in plasmid_list}
        plasmid_dict = {plasmid: i for i, plasmid in enumerate(plasmid_list)}
        # Storing runtime Experiment data

        # Ensure plasmidListEV_LE.text() is not None
        plasmid_text = self.ui.plasmidListEV_LE.text() or ""
        plasmid_list = [str(plasmid) for plasmid in plasmid_text.split(',')]

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
        empty_fields = [key for key, value in data.items() if not value and key != 'exp_id']

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

        if len(plasmid_list) != len(set(plasmid_list)):
            display_msg = "Kein Duplikat für Plasmid wird akzeptiert. \n"
            self.show_message_in_dialog(display_msg)
            return

        # Check if 'anz_plasmid' is not greater than 'anz_tubes'
        if int(data['anz_plasmid']) > int(data['anz_tubes']):
            display_msg = "Anzahl von Plasmid soll größer als Anzahl von Tubes sein.\n"
            self.show_message_in_dialog(display_msg)
            return

        try:
            for elem in plasmid_list:
                check_if_plasmid_exists_data = self.ui_database.metadata_adapter.get_plasmid_data_by_nr(elem)
                if check_if_plasmid_exists_data:
                    print("Plasmid data : " + str(check_if_plasmid_exists_data))
                else:
                    raise ValueError(f"Plasmid {elem} existiert nicht. \n")

        except Exception as ex:
            self.show_message_in_dialog(ex)
            return

        is_experiment_new = True
        total_nr_of_tubes = data['anz_tubes']
        total_old_nr_of_tubes = 0

        try:
            date_str = '-'.join(map(str, data['date']))
            experiment_id = data['exp_id'] or None
            exp_id_data = None

            if experiment_id:
                exp_id_data = self.ui_database.adapter.get_experiment_by_id(experiment_id)

            if exp_id_data is None:
                exp_data = self.ui_database.add_experiment(data['firstname'], data['lastname'],
                                                           data['anz_tubes'],
                                                           data['anz_plasmid'], date_str, None)
                self.ui.experimentIdLE.setText(str(exp_data))
                self.experiment_data = ExperimentSingleton(firstname=data['firstname'], lastname=data['lastname'],
                                                           exp_id=exp_data, plasmids=data['plasmid_list'],
                                                           date=data['date'])
                self.current_experiment = CurrentExperimentSingleton(self.experiment_data.experiment_id)
                print(self.main_window.save_cache("exp_id", self.experiment_data.experiment_id))
                self.main_window.cache_data = self.main_window.load_cache()
                is_experiment_new = True
            else:
                if exp_id_data.anz_tubes:
                    total_old_nr_of_tubes = exp_id_data.anz_tubes
                self.main_window.cache_data = self.main_window.load_cache()
                if self.main_window.cache_data.experiment_id:
                    self.check_if_current_experiment(experiment_id, self.main_window.cache_data.experiment_id)
                if not self.is_current_experiment:
                    return
                exp_data = self.ui_database.add_experiment(data['firstname'], data['lastname'],
                                                           data['anz_tubes'],
                                                           data['anz_plasmid'], date_str, experiment_id)
                self.ui.experimentIdLE.setText(str(exp_data))
                self.experiment_data = ExperimentSingleton(firstname=data['firstname'], lastname=data['lastname'],
                                                           exp_id=exp_data, plasmids=data['plasmid_list'],
                                                           date=data['date'])
                self.current_experiment = CurrentExperimentSingleton(self.experiment_data.experiment_id)

                self.main_window.cache_data = self.main_window.load_cache()
                is_experiment_new = False

            all_tubes_of_exp = self.ui_database.get_tubes_by_exp_id(self.main_window.cache_data.experiment_id)
            print("------------------------------------")
            print(all_tubes_of_exp)
        except Exception as ex:
            print(f"An error occurred: {ex}")

        # TODO Load all tubes for plasmids and while creating check if the id exists, if exists dont add in db , only add if not

        if self.current_experiment.experiment_id:
            tubes_required = abs(int(total_nr_of_tubes) - int(total_old_nr_of_tubes))
            if all_tubes_of_exp:
                self.main_window.plasmidTubesList.displayPlasmidTubes(plasmid_list, self.ui_database.available_qrcode(
                    self.current_experiment.experiment_id, tubes_required), all_tubes_of_exp)
            else:
                self.main_window.plasmidTubesList.displayPlasmidTubes(plasmid_list, self.ui_database.available_qrcode(
                    self.current_experiment.experiment_id, tubes_required), [])
            self.nextPage()

    def map_prev_next(self, ui):
        ui.vorbereitungPrev_2.clicked.connect(self.prevPage)
        ui.vorbereitungPrev_4.clicked.connect(self.prevPage)
        ui.vorbereitungNext.clicked.connect(
            lambda: self.nextPageWithControl("CreateExperiment"))
        ui.probe_to_plasmid_next.clicked.connect(
            lambda: self.nextPageWithControl("AddProbeToPlasmid"))
        ui.vorbereitungWeiter_3.clicked.connect(self.nextPage)
