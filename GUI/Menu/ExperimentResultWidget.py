from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QCursor, QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, \
    QScrollArea, QApplication, QToolTip, QAbstractItemView, QPushButton, QHBoxLayout

from DBService.DBUIAdapter import DBUIAdapter
from GUI.Custom.CustomDialog import CustomDialog, ContentType
from GUI.Model.ExperimentResult import ExperimentResult
from GUI.Storage.BorgSingleton import CurrentExperimentSingleton
from GUI.Utils.FileUtils import FileUtils


class ExperimentResultWidget(QWidget):
    """
    Custom Widget to display the results of an experiment.
    """

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.experiments_results = None
        self.main_window = main_window
        self.db_adapter = main_window.ui_db
        self.initUI()

    def initUI(self):
        # Set up the layout and any widgets you want in your custom widget
        self.layout = QVBoxLayout(self)

        self.result_label = QLabel("Experiment Results")

        h_layout = QHBoxLayout()
        self.export_button = self.create_export_btn()
        self.refresh_button = self.create_refresh_btn()
        h_layout.addWidget(self.result_label)
        h_layout.addStretch(1)
        h_layout.addWidget(self.export_button)
        h_layout.addWidget(self.refresh_button)

        self.layout.addLayout(h_layout)

        # Initialize scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)

        # Create a widget for the scroll area
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        # Create a vertical layout for the scroll widget
        scroll_layout = QVBoxLayout(scroll_widget)

        # Initialize table widget and add it to the scroll widget layout
        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widget.cellDoubleClicked.connect(self.copy_to_clipboard)
        self.table_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        scroll_layout.addWidget(self.table_widget)
        self.current_experiment = CurrentExperimentSingleton()
        self.main_window.cache_data = self.main_window.load_cache()

        if self.main_window.cache_data:
            if self.main_window.cache_data.experiment_id:
                self.current_experiment.experiment_id = self.main_window.cache_data.experiment_id
                self.fetch_and_display_results(self.main_window.cache_data.experiment_id)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

    def create_export_btn(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/img/file-export.svg"), QIcon.Mode.Normal,
                       QIcon.State.Off)
        export_btn = QPushButton("")
        export_btn.clicked.connect(self.export_table_data)
        export_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
            }
            QPushButton:hover {
                background: #eee;
            }
        """)
        export_btn.setToolTip("Export")
        export_btn.setIcon(icon)

        return export_btn

    def create_refresh_btn(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/img/refresh-double.svg"), QIcon.Mode.Normal,
                       QIcon.State.Off)
        refresh_btn = QPushButton("")
        refresh_btn.clicked.connect(lambda: self.fetch_and_display_results(self.current_experiment.experiment_id))
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
            }
            QPushButton:hover {
                background: #eee;
            }
        """)
        refresh_btn.setToolTip("Refresh")
        refresh_btn.setIcon(icon)
        return refresh_btn

    def fetch_and_display_results(self, experiment_id):
        try:
            # Fetch the data
            data = self.db_adapter.get_tracking_logs_by_exp_id(experiment_id)

            if not data:
                return

            # Map the data to model objects
            mapped_results = ExperimentResult.map_data_to_model(data)
            self.experiment_date = mapped_results[0].start_time.strftime('%d-%m-%Y')

            # Convert mapped results to a list of tuples for the table
            table_data = [(result.id, result.tube_nr, result.start_station,
                           result.start_time.strftime('%H:%M:%S.%f'), result.end_station,
                           result.end_time.strftime('%H:%M:%S.%f'), result.duration,
                           result.video_timestamp) for result in mapped_results]

            self.result_label.setText(f"Ergebnis der Experimente mit Id {experiment_id} erstellt am {self.experiment_date}")

            self.add_results_to_table(table_data)
        except Exception as ex:
            dialog = CustomDialog()
            dialog.addContent(ex, ContentType.ERROR)
            dialog.show()

    def add_results_to_table(self, results):
        """
        Method to add the results to the table widget.
        :param results: A list of tuples with the results data.
        """
        self.clear_table()
        self.experiments_results = results
        # Set the table dimensions
        self.table_widget.setColumnCount(len(results[0]))  # Assuming all tuples have the same number of elements
        self.table_widget.setRowCount(len(results))

        # Set table headers (if applicable)
        headers = ["ID", "Tube Nr.", "Start Station", "Start Time", "End Station", "End Time", "Duration",
                   "Video Timestamp"]
        self.table_widget.setHorizontalHeaderLabels(headers)

        # Adding the results to the table
        for row_index, row_data in enumerate(results):
            for column_index, item in enumerate(row_data):
                self.table_widget.setItem(row_index, column_index, QTableWidgetItem(str(item)))

        # Adjust the column widths and rows to fit the content
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

        # Update the layout
        self.layout.update()
        self.table_widget.update()

        #Force update
        self.layout.activate()

    def export_table_data(self):
        self.fetch_and_display_results(self.current_experiment.experiment_id)
        if not self.experiments_results:
            return
        try:
            if not self.experiments_results:
                return

            headers = ["ID", "Tube Nr.", "Start Station", "Start Time", "End Station", "End Time", "Duration",
                       "Video Timestamp"]

            data_to_export = [
                ["Experiment ID", self.current_experiment.experiment_id, "Date", self.experiment_date],
                []
            ]

            data_to_export += [headers] + self.experiments_results
            FileUtils.save_data_to_excel(self, data_to_export,
                                         "experiment_result_" + self.current_experiment.experiment_id)
        except Exception as ex:
            print(ex)

    def copy_to_clipboard(self, row, column):
        item = self.table_widget.item(row, column)
        if item is not None:
            try:
                QApplication.clipboard().setText(item.text())
                QToolTip.showText(QCursor.pos(), "Copied")
                QTimer.singleShot(5000, QToolTip.hideText)
            except Exception as ex:
                print(ex)

    def clear_table(self):
        # Method to clear all the results from the table widget.
        self.table_widget.setRowCount(0)
        self.table_widget.clearContents()
