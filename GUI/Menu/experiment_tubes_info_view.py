from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QColor, QPalette, QIcon, QPixmap
from PyQt6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QAbstractItemView)
from PyQt6.uic.properties import QtGui

from GUI.button_back_design_test import CustomBackButton


class ExperimentTubesDetails(QWidget):
    back_to_dashboard = pyqtSignal()  # Signal to indicate when to go back to the dashboard

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        # Back button
        # self.back_button = QPushButton("", self)
        # self.back_button.clicked.connect(self.on_back_clicked)
        # pixmap = QPixmap(":/icons/img/arrow-left.svg")
        # scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
        #                               Qt.TransformationMode.SmoothTransformation)
        # icon1 = QIcon()
        # icon1.addPixmap(scaled_pixmap, QIcon.Mode.Normal, QIcon.State.Off)
        # self.back_button.setIcon(icon1)
        # When creating the button:
        icon_pixmap = QPixmap(":/icons/img/arrow-left.svg").scaled(
            200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        self.back_button = CustomBackButton('Zurück', icon_pixmap, self)
        self.back_button.setStyleSheet("background:#FF0000;")
        self.back_button.setGeometry(50, 20, 100, 50)
        self.back_button.clicked.connect(self.on_back_clicked)

        # layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.title = QLabel('Experiment Details', self)
        layout.addWidget(self.title)


    def update_details(self, experiment_data):
        self.title.setText(f"Experiment ID: {experiment_data['id']}")
        self.main_window.title_bar.add_back_btn(self.back_button)

    def on_back_clicked(self):
        self.back_button.setParent(None)
        self.back_to_dashboard.emit()


class ExperimentTubesInfoDashboard(QWidget):
    experiment_selected = pyqtSignal(dict)  # Signal to indicate an experiment is selected

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Header area
        header_label = QLabel('Experiments Overview')
        layout.addWidget(header_label)

        # Create the experiments table
        self.experiments_table = QTableWidget(10, 3)
        self.experiments_table.setHorizontalHeaderLabels(['ID', 'Name', 'Status'])
        self.populate_table()
        layout.addWidget(self.experiments_table)

        # Set the selection behavior to select the entire row
        self.experiments_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.experiments_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.experiments_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Change the hover color
        hover_palette = self.experiments_table.palette()
        hover_palette.setColor(QPalette.ColorRole.Highlight, QColor(200, 200, 200))
        self.experiments_table.setPalette(hover_palette)

        # Connect the cell click signal
        self.experiments_table.cellClicked.connect(self.row_selected)

        # back_button = QPushButton('Back', self)
        # self.main_window.title_bar.add_back_btn(back_button)


    def populate_table(self):
        self.experiments_data = [
            {'id': i, 'name': f'Experiment {i}', 'status': 'Running' if i % 2 == 0 else 'Stopped'}
            for i in range(10)
        ]
        for i, experiment in enumerate(self.experiments_data):
            self.experiments_table.setItem(i, 0, QTableWidgetItem(str(experiment['id'])))
            self.experiments_table.setItem(i, 1, QTableWidgetItem(experiment['name']))
            self.experiments_table.setItem(i, 2, QTableWidgetItem(experiment['status']))

    def row_selected(self, row, column):
        experiment_data = self.experiments_data[row]
        self.experiment_selected.emit(experiment_data)
