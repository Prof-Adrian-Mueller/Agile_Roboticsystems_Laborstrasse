import re
from functools import partial
from typing import Callable

import pandas as pd
from PyQt6.QtCore import Qt, QUrl, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QDesktopServices, QIcon, QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, \
    QAbstractScrollArea, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QToolTip
from PyQt6.uic.properties import QtCore

from DBService.Model.Experiment import Experiment
from GUI.Custom.CustomDialog import CustomDialog, ContentType
from GUI.Menu.QRCodesWidget import QRCodesWidget
from GUI.Navigation import Ui_MainWindow
from GUI.Utils.CheckUtils import CheckUtils
from GUI.Utils.FileUtils import FileUtils


class TableInformationFetchByParameter(QWidget):
    """
    It manages the Search function for different type of variables.
    """

    def __init__(self, ui: Ui_MainWindow, main_window):
        super().__init__()
        self.data_for_table = None
        self.current_table = QTableWidget()
        self.ui = ui
        self.main_window = main_window
        self.filename_to_export = None
        self.text_qlabel_option = QLabel("")
        self.ui.tube_info_tubeid_input.setPlaceholderText("Bsp. Max2_2024-1-28 oder 2024-1-28")
        self.ui.combo_option_class_type.currentIndexChanged.connect(
            lambda index: self.update_placeholder_text(self.ui.combo_option_class_type.itemText(index))
        )
        # combo_option_class_type

    def update_placeholder_text(self, text):
        if text == "Experiment":
            self.ui.tube_info_tubeid_input.setPlaceholderText("Bsp. Max2_2024-1-28 oder 2024-1-28")
        elif text == "Tube":
            self.ui.tube_info_tubeid_input.setPlaceholderText("Bsp. 1")
        elif text == "Plasmid":
            self.ui.tube_info_tubeid_input.setPlaceholderText("Bsp. PHB655")

    def load_and_display_tube_info(self):
        tubeid_input_text = self.ui.tube_info_tubeid_input.text()
        if tubeid_input_text:
            self.append_info_to_view(tubeid_input_text, self.ui.combo_option_class_type.currentText())
        else:
            self.main_window.dialog.add_titlebar_name("Abfrage-Infos")
            self.main_window.show_message_in_dialog("Bitte geben Sie eine gültige ID ein, um fortzufahren!")

    def open_image(self, row, column):
        # TODO Open image in an image viewer
        item = self.table.item(row, column)
        if item:
            key = item.text()
            if key == 'image_location':
                image_path = self.data_for_table.get('image_location')
                if image_path:
                    QDesktopServices.openUrl(QUrl.fromLocalFile(image_path))
            # else:
            #     self.copy_to_clipboard(row, column)

    def append_info_to_view(self, input_id, current_option):
        data_for_table = None
        is_tube_selected = False
        delete_button = None
        text_label_for_option = ""
        try:
            if current_option == 'Experiment':

                if CheckUtils.is_date(input_id):
                    data_for_table = self.main_window.ui_db.get_experiments_by_date(input_id)
                    # data_for_table = vars(data_for_table)
                    print(data_for_table)
                else:
                    # Create the left-aligned label
                    text_label_for_option = f"{current_option} {input_id} details: "
                    data_for_table = self.main_window.ui_db.adapter.get_experiment_by_id(input_id)
                    # Convert the Experimente instance to a dictionary
                    if data_for_table:
                        data_for_table = vars(data_for_table)
                        if data_for_table['exp_id']:
                            delete_button = self.create_delete_btn(input_id,
                                                                   f"Möchten Sie das Experiment {input_id} wirklich löschen?")
                    else:
                        data_for_table = {}
                        dialog = CustomDialog(self)
                        dialog.add_titlebar_name("Experiment Query")
                        dialog.addContent(f"Kein Ergebnis für {input_id}", ContentType.OUTPUT)
                        dialog.show()
            elif current_option == 'Plasmid':
                text_label_for_option = f"{current_option} {input_id} details: "
                data_for_table = self.main_window.ui_db.metadata_adapter.get_plasmid_data_by_nr(input_id)
            elif current_option == 'Tube':
                text_label_for_option = f"{current_option} {input_id} details: "
                data_for_table = self.main_window.ui_db.tube_adapter.get_tube_data_by_probe_nr(input_id)

                qr_code_widget = QRCodesWidget(self.main_window)
                pixmap, image_location = qr_code_widget.generate_micro_qr_code(data_for_table['qr_code'])
                data_for_table['pixmap'] = pixmap
                data_for_table['image_location'] = image_location
            self.filename_to_export = current_option
        except Exception as ex:
            self.main_window.removeDialogBoxContents()
            self.main_window.show_message_in_dialog(ex)

        self.text_qlabel_option.setText(text_label_for_option)
        self.text_qlabel_option.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a horizontal layout
        h_layout = QHBoxLayout()
        h_layout.setObjectName("title_export_box")
        h_layout.addWidget(self.text_qlabel_option)
        h_layout.addStretch()

        if delete_button:
            if h_layout.indexOf(delete_button) != -1:
                delete_button.setParent(None)
            else:
                h_layout.addWidget(delete_button)

        # Add the export_btn
        export_btn = self.create_export_btn()
        h_layout.addWidget(export_btn)

        # Add the horizontal layout to the grid layout
        self.ui.tube_info_grid_layout.addLayout(h_layout, 0, 0)

        if not data_for_table:
            self.text_qlabel_option.setText(f"Daten für {current_option} mit der ID {input_id} konnten nicht abgerufen werden.")
            pass

        try:
            # Remove the old table from the layout, if it exists
            if hasattr(self, 'current_table') and self.current_table:
                self.ui.tube_info_grid_layout.removeWidget(self.current_table)
                self.current_table.deleteLater()

            # Create the table
            table = QTableWidget()
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            table.setMinimumSize(400, 500)

            # QSS for table
            table.setStyleSheet("""
                QTableWidget {
                    gridline-color: #E0E0E0;
                    background-color: transparent;
                }
                QTableWidget::item {
                    padding: 10px;
                }
                QHeaderView::section {
                    background-color: #F5F5F5;
                    padding: 10px;
                    border: 1px solid #E0E0E0;
                }
            """)
            self.current_table = table

            # Set the number of rows and columns based on the data
            if data_for_table:
                table.setRowCount(len(data_for_table))
                table.setColumnCount(2)

            table.setHorizontalHeaderLabels(['Key Name', 'Value'])
            # Hide the row and column headers
            table.verticalHeader().hide()

            if CheckUtils.is_date(input_id):
                for i, experiment in enumerate(data_for_table):
                    key_item = QTableWidgetItem(experiment.exp_id)
                    key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    experiment_str = f"{experiment.vorname}, {experiment.name}"
                    self.current_table.setItem(i, 0, key_item)
                    value_item = QTableWidgetItem(experiment_str)
                    value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.current_table.setItem(i, 1, value_item)
                    self.current_table.cellClicked.connect(
                        partial(self.handle_cell_click_experiment_date, experiment=experiment))

            else:
                # Populate the table with data
                for i, (key, value) in enumerate(data_for_table.items()):
                    key_item = QTableWidgetItem(key)
                    key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.current_table.setItem(i, 0, key_item)

                    if key == 'pixmap':
                        label = QLabel()
                        label.setPixmap(value)
                        self.current_table.setCellWidget(i, 1, label)
                    elif key == 'image_location':
                        value_item = QTableWidgetItem(value)
                        value_item.setFlags(
                            value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                        self.current_table.setItem(i, 1, value_item)
                    else:
                        value_item = QTableWidgetItem(str(value))
                        value_item.setFlags(
                            value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item non-editable
                        self.current_table.setItem(i, 1, value_item)
                        # if key == 'anz_tubes':
                        #     # TODO load Logging MonitoringData
                        #     self.current_table.clicked.connect(
                        #         partial(self.show_all_tubes_of_experiment, key=key))

            # Remove the background
            table.setObjectName('tube_info_table')

            # Set the size policy to expand to the available space
            table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.current_table.cellDoubleClicked.connect(self.copy_to_clipboard)

            # Add the table to the grid layout
            self.ui.tube_info_grid_layout.addWidget(table, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            self.data_for_table = data_for_table

        except Exception as ex:
            dialog = CustomDialog(self)
            dialog.addContent(f"{ex}", ContentType.OUTPUT)
            dialog.show()

    def copy_to_clipboard(self, row, column):
        item = self.current_table.item(row, column)
        if item is not None:
            text = item.text()
            if text:
                try:
                    QApplication.clipboard().setText(text)
                    QToolTip.showText(QCursor.pos(), "Copied")
                    QTimer.singleShot(5000, QToolTip.hideText)
                except Exception as ex:
                    print(ex)

    def export_table_data(self):
        if not self.data_for_table:
            return
        try:
            data_df = pd.DataFrame([self.data_for_table])
            FileUtils.save_data_to_excel(self, data_df,
                                         "search_result_" + self.filename_to_export)
        except Exception as ex:
            print(ex)

    def create_export_btn(self):
        return self.create_button(":/icons/img/file-export.svg", "Export", self.export_table_data)

    def create_delete_btn(self, id, message):
        return self.create_button(":/icons/img/trash.svg", "Delete", lambda: self.delete_table_data(id, message))

    def create_button(self, icon_path: str, tooltip: str, on_click: Callable) -> QPushButton:
        icon = QIcon()
        icon.addPixmap(QPixmap(icon_path), QIcon.Mode.Normal, QIcon.State.Off)
        button = QPushButton("")
        button.clicked.connect(on_click)
        button.setStyleSheet("""
            QPushButton {
                background: transparent;
            }
            QPushButton:hover {
                background: #eee;
            }
        """)
        button.setToolTip(tooltip)
        button.setIcon(icon)

        return button

    def delete_table_data(self, id, message):
        try:
            dialog = CustomDialog(self.main_window)
            dialog.addContent(message, ContentType.OUTPUT)
            dialog.add_titlebar_name("Delete Info")

            # Create buttons
            yes = QPushButton("Ja")
            no = QPushButton("Nein")

            # Connect buttons to functions
            yes.clicked.connect(lambda: self.confirm_delete(id, dialog))
            yes.setStyleSheet("background-color: red;")
            no.clicked.connect(dialog.close)

            # Create a horizontal layout and add buttons to it
            h_layout = QHBoxLayout()

            dialog.content_addition_template(yes, h_layout)
            dialog.content_addition_template(no, h_layout)

            dialog.show()
        except Exception as ex:
            print(ex)

    def confirm_delete(self, id, dialog):
        dialog_new = CustomDialog(self.main_window)
        dialog_new.add_titlebar_name("Delete Info")
        try:
            dialog.close()
            self.main_window.ui_db.delete_experiment(id)
            dialog_new.addContent(f"Experiment mit der ID {id} wurde gelöscht.", ContentType.OUTPUT)
            dialog_new.show()
            self.append_info_to_view(id, "Experiment")
        except Exception as ex:
            dialog_new.addContent(f"Experiment mit der ID {id} könnte nicht gelöscht werden.", ContentType.ERROR)
            dialog_new.addContent(ex, ContentType.ERROR)
            dialog_new.show()

    def handle_cell_click_experiment_date(self, row, col, experiment):
        experiment_id = self.current_table.item(row, 0).text()

        if experiment.exp_id == experiment_id:
            print(f"Cell ({row}, {col}) clicked for experiment {experiment_id} - \n - {experiment}")
            self.append_info_to_view(experiment_id, 'Experiment')
