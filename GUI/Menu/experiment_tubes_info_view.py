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
        self.back_button = None
        self.details_table = None
        self.title = None
        self.main_window = main_window
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout(self)
        # Back button.
        icon_pixmap = QPixmap(":/icons/img/arrow-left.svg").scaled(
            200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        self.back_button = CustomBackButton('Zurück', icon_pixmap, self)
        self.back_button.setStyleSheet("background:#FF0000;")
        self.back_button.setGeometry(50, 20, 100, 50)
        self.back_button.clicked.connect(self.on_back_clicked)

        # layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.title = QLabel('Experiment Details', self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.title)

        # Initialize the details table
        self.initialize_details_table()
        layout.addWidget(self.details_table)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def initialize_details_table(self):
        self.details_table = QTableWidget(10, 2)  # 10 rows, 2 columns
        self.details_table.setHorizontalHeaderLabels(['Field', 'Value'])

    def update_details(self, experiment_data):
        try:
            # Update the title
            self.title.setText(f"Experiment ID: {experiment_data['probe_nr']}")

            # Reset the table rows
            self.details_table.setRowCount(10)
            self.main_window.title_bar.add_back_btn(self.back_button)

            # Populate the table with the data
            fields = ['Probe Nr', 'QR Code', 'Plasmid Nr', 'Vektor', 'Insert', 'Name', 'Vorname', 'Exp ID', 'Datum',
                      'Anz Fehler']
            for i, field in enumerate(fields):
                value = str(experiment_data[field.lower().replace(' ', '_')])

                item_field = QTableWidgetItem(field)
                item_field.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.details_table.setItem(i, 0, item_field)

                item_value = QTableWidgetItem(value)
                item_value.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.details_table.setItem(i, 1, item_value)

            # Add the table to the layout
            self.layout().addWidget(self.details_table)
        except Exception as ex:
            print(ex)

    def on_back_clicked(self):
        self.back_button.setParent(None)
        self.back_to_dashboard.emit()


class ExperimentTubesInfoDashboard(QWidget):
    experiment_selected = pyqtSignal(dict)  # Signal to indicate an experiment is selected

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.db_ui = None
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.ui_db = self.main_window.ui_db
        layout = QVBoxLayout(self)

        # Header area
        header_label = QLabel('Experiments Overview')
        layout.addWidget(header_label)

        # Creates the experiments table
        self.experiments_table = QTableWidget(10, 10)
        self.experiments_table.setHorizontalHeaderLabels(
            ['Probe Nr', 'QR Code', 'Plasmid Nr', 'Vektor', 'Insert', 'Name', 'Vorname', 'Exp ID', 'Datum',
             'Anz Fehler'])
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

        self.experiments_data = self.ui_db.experiment_adapter.get_tubes_data_for_experiment("Ujwal2")

        for i, experiment in enumerate(self.experiments_data):
            self.experiments_table.setItem(i, 0, QTableWidgetItem(str(experiment['probe_nr'])))
            self.experiments_table.setItem(i, 1, QTableWidgetItem(experiment['qr_code']))
            self.experiments_table.setItem(i, 2, QTableWidgetItem(experiment['plasmid_nr']))
            self.experiments_table.setItem(i, 3, QTableWidgetItem(experiment['vektor']))
            self.experiments_table.setItem(i, 4, QTableWidgetItem(experiment['insert']))
            self.experiments_table.setItem(i, 5, QTableWidgetItem(experiment['name']))
            self.experiments_table.setItem(i, 6, QTableWidgetItem(experiment['vorname']))
            self.experiments_table.setItem(i, 7, QTableWidgetItem(experiment['exp_id']))
            self.experiments_table.setItem(i, 8, QTableWidgetItem(experiment['datum']))
            self.experiments_table.setItem(i, 9, QTableWidgetItem(str(experiment['anz_fehler'])))

    def row_selected(self, row, column):
        experiment_data = self.experiments_data[row]
        self.experiment_selected.emit(experiment_data)
