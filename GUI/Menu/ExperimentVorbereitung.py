import numpy as np
import pandas as pd

from GUI.CustomDialog import ContentType, CustomDialog
from GUI.Navigation import Ui_MainWindow
from PyQt6.QtCore import pyqtSignal, QDate
import datetime

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class ExperimentVorbereitung:
    """
    This is an Example comment.
    """
    sendButtonClicked = pyqtSignal(str)

    def __init__(self, ui: Ui_MainWindow, main_window):
        self.ui = ui
        self.main_window = main_window
        self.ui.experimentIdLE.textChanged.connect(self.checkExperimentID)
        self.dialog = CustomDialog(self.ui.centralwidget)

        # Set the datumLE to current Date
        today = datetime.datetime.today()
        qdate = QDate(today.year, today.month, today.day)
        self.ui.datumLE.setDate(qdate)

    def checkExperimentID(self, text):
        print(text)

    def nextPage(self):
        current_index = self.ui.vorbereitungStackedTab.currentIndex()
        if current_index < self.ui.vorbereitungStackedTab.count() - 1:
            self.ui.vorbereitungStackedTab.setCurrentIndex(current_index + 1)

    def nextPageWithControl(self, pageData):
        if pageData == 'CreateExperiment':
            print("weiter clicked " + pageData)
            plasmid_list = [str(plasmid) for plasmid in self.ui.plasmidListEV_LE.text().split(',')]
            data = {
                "exp_id": self.ui.experimentIdLE.text(),
                "name": self.ui.nameLE.text(),
                "vorname": self.ui.vornameLE.text(),
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
                displayMsg = "Anzahl Plasmid und Anzahl Tubes sollen Zahlen sein. Bitte Zahlen eingeben.\n"
                self.main_window.dialogBoxContents.append(
                    self.main_window.dialog.addContent(f"{displayMsg}", ContentType.OUTPUT))
                self.main_window.dialog.show()
                return

            if int(data['anz_tubes']) % 2 != 0:
                displayMsg = "Anzahl Tubes soll eine gerade Zahl sein.\n"
                self.main_window.dialogBoxContents.append(
                    self.main_window.dialog.addContent(f"{displayMsg}", ContentType.OUTPUT))
                self.main_window.dialog.show()
                return

            if int(data['anz_tubes']) > 32 and int(data['anz_tubes']) > 32:
                displayMsg = "Anzahl Tubes oder Anzahl Plasmid sollen nicht größer als 32 sein.\n"
                self.main_window.dialogBoxContents.append(
                    self.main_window.dialog.addContent(f"{displayMsg}", ContentType.OUTPUT))
                self.main_window.dialog.show()
                return

            # Check if the count of plasmids matches 'anz_plasmid'
            if len(plasmid_list) != int(data['anz_plasmid']):
                displayMsg = "Anzahl von Plasmid und Plasmid Liste stimmen nicht zu. \n"
                self.main_window.dialogBoxContents.append(
                    self.main_window.dialog.addContent(f"{displayMsg}", ContentType.OUTPUT))
                self.main_window.dialog.show()
                return

            # Check if 'anz_plasmid' is not greater than 'anz_tubes'
            if int(data['anz_plasmid']) > int(data['anz_tubes']):
                displayMsg = "Anzahl von Plasmid soll größer als Anzahl von Tubes sein.\n"
                self.main_window.dialogBoxContents.append(
                    self.main_window.dialog.addContent(f"{displayMsg}", ContentType.OUTPUT))
                self.main_window.dialog.show()
                return

            # If all checks pass, go to the next page
            self.main_window.plasmidTubesList.displayPlasmidTubes(plasmid_list)
            print(data)
            self.nextPage()

    def prevPage(self):
        print("prev clicked")
        current_index = self.ui.vorbereitungStackedTab.currentIndex()
        if current_index > 0:
            self.ui.vorbereitungStackedTab.setCurrentIndex(current_index - 1)
