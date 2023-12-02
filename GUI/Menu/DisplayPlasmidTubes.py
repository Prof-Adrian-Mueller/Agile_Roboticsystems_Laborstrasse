import os
import qrcode
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

    def displayPlasmidTubes(self, plasmidNrList):
        for i in reversed(range(self.outputLayout.count())):
            widget = self.outputLayout.itemAt(i).widget().setParent(None)
            if widget is not None:
                widget.setParent(None)
                sip.delete(widget)

        for elem in plasmidNrList:
            self.appendOutput(elem)

    def appendOutput(self, plasmidNr):
        widget = QWidget()
        widget.setObjectName("displayPlasmidTubes")
        self.outputLayout.addWidget(widget)
        # Create the buttons and line edit
        plasmidNr = QLabel(plasmidNr)
        probeNrInput = QLineEdit()
        probeNrInput.setPlaceholderText("Probe Nr eingeben. Bsp : 1,3,4,7")
        # probeNrInput.setFixedWidth(120)
        h_layout = QHBoxLayout(widget)

        # Create a QWidget and set the QVBoxLayout on it
        v_widget = QWidget()
        # Add the QWidget to the QHBoxLayout
        h_layout.addWidget(v_widget)
        h_layout.addWidget(plasmidNr)
        h_layout.addWidget(probeNrInput)
