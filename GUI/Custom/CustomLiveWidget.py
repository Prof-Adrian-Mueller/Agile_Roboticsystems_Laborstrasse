import ast

from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QGroupBox, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QLabel, QLineEdit, QTableWidgetItem, QAbstractItemView, QHeaderView, QScrollArea, QFileDialog, \
    QSizePolicy
from PyQt6.QtGui import QPainter, QPen, QIcon, QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QObject, QEvent, QTimer, QThread, QRect, QPoint

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'

from GUI.Custom.CustomDialog import ContentType, CustomDialog
from GUI.Menu.QRCodesWidget import QRCodesWidget
from GUI.Model.LiveTubeStatus import LiveTubeStatus
from GUI.Storage.BorgSingleton import ExperimentSingleton, TubesSingleton, CurrentExperimentSingleton, \
    TubeLayoutSingleton


class CustomLiveWidget(QWidget):
    """
    Custom view for the Live View Table. Still on Work.
    """

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.dialogBoxContents = []
        self.current_experiment = None
        self.main_window = main_window

        self.layout = QVBoxLayout(self)
        self.experiment_data = ExperimentSingleton()

        h_label_layout = QHBoxLayout()
        probe_label = QLabel("Tube Nr.")
        start_label = QLabel("Beladung")
        middle_label = QLabel("Thymio")
        end_label = QLabel("Deckelentnahme")
        probe_label.setObjectName("live_row_label")
        start_label.setObjectName("live_row_label")
        middle_label.setObjectName("live_row_label")
        end_label.setObjectName("live_row_label")
        h_label_layout.addWidget(probe_label)
        h_label_layout.addWidget(start_label)
        h_label_layout.addSpacing(75)
        h_label_layout.addWidget(middle_label)
        h_label_layout.addSpacing(75)
        h_label_layout.addWidget(end_label)
        h_label_layout.addStretch(1)
        self.refresh_btn = self.create_refresh_btn()
        h_label_layout.addWidget(self.refresh_btn)
        self.layout.addLayout(h_label_layout)

        scroll = QScrollArea(self)
        self.layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Disable horizontal scrolling

        frame = QFrame(scroll)
        scroll.setWidget(frame)

        self.layout = QVBoxLayout(frame)
        self.qr_code_widget = QRCodesWidget(self.main_window)
        # self.design_layout(self.layout, 1)

    def create_refresh_btn(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/img/refresh-double.svg"), QIcon.Mode.Normal, QIcon.State.Off)

        refresh_btn = QPushButton("")
        refresh_btn.clicked.connect(self.refresh_data)
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

    def refresh_data(self):
        try:
            self.main_window.cache_data = self.main_window.load_cache()
            if self.main_window.cache_data:
                tube_info_data = self.main_window.ui_db.adapter.get_tubes_by_exp_id(
                    self.main_window.cache_data.experiment_id)
                self.display_tubes_data(tube_info_data)

        except Exception as ex:
            self.main_window.removeDialogBoxContents()
            self.main_window.show_message_in_dialog(ex)

    def display_tubes_data(self, tube_info_data):
        print('-------\n' + str(tube_info_data))
        self.clear_layout(self.layout)
        if tube_info_data:
            for tube in tube_info_data:
                self.design_layout(self.layout, tube)

    def design_layout(self, layout, tube):
        widget = QWidget()
        widget.setObjectName("itemRowLiveData")
        layout.addWidget(widget)
        h_layout = QHBoxLayout(widget)
        tube_nr = tube['probe_nr']
        label = QLabel(str(tube_nr))
        h_layout.addWidget(label)
        buttons = [QPushButton(f'{j + 1}') for j in range(3)]
        tube_layout_singleton = TubeLayoutSingleton()
        stations = []

        # Creating buttons
        buttons = [QPushButton(f'{i}') for i in range(1, 4)]
        tube_station_info = TubeLayoutSingleton()
        for index, button in enumerate(buttons):
            h_layout.addWidget(button)
            h_layout.addStretch(10)
            stations.append(button)
            station_nr = index + 1
            # TODO change station details
            # tube_station_info.add_station_info(str(tube_nr), station_nr,
            #                                    {"name": f"Station {station_nr}",
            #                                     "details": f"Details about Station {station_nr}"})

            def create_click_handler(station_number):
                return lambda: self.show_station_info(station_number, tube_nr)

            button.clicked.connect(create_click_handler(station_nr))

            # For the first and second buttons, add arrow indicators
            if index < len(buttons) - 1:
                arrow_layout = QVBoxLayout()  # This layout will stack arrows vertically

                # Upper arrow (right-facing)
                arrow_right_label = QLabel()
                arrow_right_pixmap = QPixmap(":/icons/img/arrow-right.svg").scaled(300, 80,
                                                                                   Qt.AspectRatioMode.KeepAspectRatio)
                arrow_right_label.setPixmap(arrow_right_pixmap)
                arrow_layout.addWidget(arrow_right_label)

                # Lower arrow (left-facing)
                arrow_left_label = QLabel()
                arrow_left_pixmap = QPixmap(":/icons/img/arrow-left.svg").scaled(300, 80,
                                                                                 Qt.AspectRatioMode.KeepAspectRatio)
                arrow_left_label.setPixmap(arrow_left_pixmap)
                arrow_layout.addWidget(arrow_left_label)

                # Add the vertical layout of arrows to the main horizontal layout
                h_layout.addLayout(arrow_layout)

        widget.setLayout(h_layout)  # Set the layout on the main widget

        tube_layout_singleton.add_button_layout(tube_nr, stations)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/img/info.svg"), QIcon.Mode.Normal, QIcon.State.Off)
        more_btn = QPushButton()
        more_btn.setIcon(icon)
        more_btn.setObjectName("more_btn")
        more_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        more_btn.clicked.connect(lambda: self.more_btn_layout(tube))
        h_layout.insertStretch(h_layout.indexOf(more_btn), 1)
        h_layout.addWidget(more_btn)

    def more_btn_layout(self, tube):
        global layout_field
        try:
            # self.main_window.removeDialogBoxContents()
            self.dialog = CustomDialog(self.main_window)
            self.dialog.add_titlebar_name("Details")
            if tube:
                for key, value in tube.items():
                    if key == 'qr_code':
                        pixmap, location = self.qr_code_widget.generate_qr_code(value)
                        if pixmap is not None:
                            layout_field = QLabel()
                            layout_field.setPixmap(pixmap)
                        self.dialogBoxContents.append(
                            self.dialog.addContent(f"QR : {value}", ContentType.OUTPUT))
                        self.dialogBoxContents.append(
                            self.dialog.addContent(layout_field, ContentType.OUTPUT))
                    else:
                        self.dialogBoxContents.append(
                            self.dialog.addContent(f"{key.capitalize()} : {value}", ContentType.OUTPUT))
                self.dialog.show()
        except Exception as ex:
            print(ex)

    def show_station_info(self, station, tube_nr):
        try:
            station_dialog = CustomDialog(self.main_window)
            station_dialog.add_titlebar_name(f"Station {station} of Tube {tube_nr} Status")
            tube_station_info = TubeLayoutSingleton()
            if 'tube_station_info' in locals() and tube_station_info:
                station_dialog.addContent(f"Station {station}", ContentType.OUTPUT)
                station_info = tube_station_info.get_station_info(str(tube_nr))[station - 1]
                if station_info:
                    status_str = station_info['details']
                    try:
                        status = ast.literal_eval(status_str)
                        status_lines = [f"{key}: {value}" for key, value in status.items()]
                        formatted_status = "\n".join(status_lines)
                        station_dialog.addContent(formatted_status, ContentType.OUTPUT)
                    except ValueError:
                        station_dialog.addContent("Invalid data format", ContentType.ERROR)
                else:
                    station_dialog.addContent(f"No Data", ContentType.OUTPUT)
            else:
                station_dialog.addContent(f"Station {station}", ContentType.OUTPUT)
                station_dialog.addContent(f"No Data", ContentType.OUTPUT)
            station_dialog.show()
        except Exception as ex:
            station_dialog = CustomDialog(self.main_window)
            station_dialog.add_titlebar_name(f"Station {station} of Tube {tube_nr} Status")
            station_dialog.addContent(f"{ex}", ContentType.ERROR)
            station_dialog.show()


    def clear_layout(self, layout):
        """
        Remove all widgets from the given layout.
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class ArrowWidget(QWidget):
    def __init__(self, start_widget, end_widget):
        super().__init__()
        self.start_widget = start_widget
        self.end_widget = end_widget

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.GlobalColor.black, 2)
        qp.setPen(pen)

        start_pos = self.start_widget.pos()
        end_pos = self.end_widget.pos()

        qp.drawLine(
            QPoint(start_pos.x() + self.start_widget.width(), int(start_pos.y() + self.start_widget.height() / 2)),
            QPoint(end_pos.x(), int(end_pos.y() + self.end_widget.height() / 2)))

        qp.end()
