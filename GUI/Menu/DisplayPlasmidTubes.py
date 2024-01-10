import os

from GUI.Custom.CustomDialog import ContentType
from GUI.Navigation import Ui_MainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QApplication, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt
from GUI.Navigation import Ui_MainWindow
from PyQt6 import sip

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'

from GUI.Storage.BorgSingleton import ExperimentSingleton


class DisplayPlasmidTubes(QWidget):
    """
    Shows the List of Plasmid and an Input field which accepts Probe Nr as a List in comma Separated Values like 5,6,9.
    """

    def __init__(self, ui: Ui_MainWindow, main_window):
        super().__init__()
        self.ui = ui
        self.main_window = main_window

        scroll = QScrollArea(self)
        self.ui.plasmidProbeList.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Disable horizontal scrolling

        frame = QFrame(scroll)
        scroll.setWidget(frame)
        self.outputLayout = QVBoxLayout(frame)
        self.experiment_data = ExperimentSingleton()
        self.plasmid_tubes = {}
        self.tubes_input_fields = []

    def displayPlasmidTubes(self, plasmid_nr_list, availiable_tubes_dict, exp_all_info):

        for i in reversed(range(self.outputLayout.count())):
            widget = self.outputLayout.itemAt(i).widget().setParent(None)
            if widget is not None:
                widget.setParent(None)
                sip.delete(widget)

        starting_info_txt = QLabel(
            f"Experiment Id: {self.experiment_data.experiment_id} | {self.experiment_data.firstname}, {self.experiment_data.lastname}")
        availiable_tube_list = QLabel(str(availiable_tubes_dict))
        availiable_tube_label = QLabel("Verfügbare Tubes : ")
        text_widget = QWidget()  # Create a QWidget
        text_layout = QHBoxLayout()  # Create a QHBoxLayout
        text_layout.addWidget(starting_info_txt)
        text_layout.addStretch()
        text_layout.addWidget(availiable_tube_label)
        text_layout.addWidget(availiable_tube_list)
        text_widget.setLayout(text_layout)  # Set the layout of the QWidget to your QHBoxLayout
        self.outputLayout.addWidget(text_widget)

        mapped_plasmid_tubes = self.map_plasmid_tubes(exp_all_info)

        for elem in plasmid_nr_list:
            self.appendOutput(elem, mapped_plasmid_tubes)

    def map_plasmid_tubes(self, data):
        mapping = {}
        if not data:
            return mapping
        # Loop over the list of dictionaries
        for item in data:
            # Get the plasmid number and the probe number from the current item
            plasmid_nr = item['plasmid_nr']
            probe_nr = item['probe_nr']

            # Check if the plasmid number is already in the mapping
            if plasmid_nr in mapping:
                # If yes, append the probe number to the existing list
                mapping[plasmid_nr].append(probe_nr)
            else:
                # If not, create a new list with the probe number
                mapping[plasmid_nr] = [probe_nr]

        return mapping

    def appendOutput(self, plasmid_nr, mapped_plasmid_tubes):
        widget = QWidget()
        widget.setObjectName("displayPlasmidTubes")
        self.outputLayout.addWidget(widget)
        # Create the buttons and line edit
        plasmid_nr_label = QLabel(plasmid_nr)
        probe_nr_input = QLineEdit()
        plasmid_tubes = mapped_plasmid_tubes.get(plasmid_nr)
        if plasmid_tubes:
            probe_nr_input.setPlaceholderText(",".join(str(x) for x in plasmid_tubes))
        else:
            probe_nr_input.setPlaceholderText("Probe Nr eingeben. Bsp : 1,2,3")

        self.tubes_input_fields.append(probe_nr_input)
        probe_nr_input.editingFinished.connect(
            lambda: self.save_tubes_to_plasmid(probe_nr_input.text(), plasmid_nr))

        # probe_nr_input.setFixedWidth(120)
        h_layout = QHBoxLayout(widget)

        # Create a QWidget and set the QVBoxLayout on it
        v_widget = QWidget()
        # Add the QWidget to the QHBoxLayout
        h_layout.addWidget(v_widget)
        h_layout.addWidget(plasmid_nr_label)
        h_layout.addWidget(probe_nr_input)

    def save_tubes_to_plasmid(self, text, plasmid_nr):
        # add tubes in the borg list for each plasmid
        print("input probe")
        print(text)
        print(plasmid_nr)
        try:
            self.experiment_data.plasmid_tubes[plasmid_nr] = [int(num) for num in text.split(',')]
            print(self.experiment_data.plasmid_tubes)
        except Exception as ex:
            self.main_window.dialogBoxContents.append(
                self.main_window.dialog.addContent(f"Please check the Input. \n{ex}", ContentType.OUTPUT))
            self.main_window.dialog.show()

    def check_duplicate_inputs(self):
        input_values = []
        for field in self.tubes_input_fields:
            input_values.extend(field.text().split(','))

        if len(input_values) != len(set(input_values)):
            print("Duplicate inputs found.")
            return True
        else:
            print("No duplicate inputs.")
            return False

    def check_max_input(self):
        input_values = []
        for field in self.tubes_input_fields:
            input_values.extend(field.text().split(','))

        if len(input_values)>32:
            return False

        return True

