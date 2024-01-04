import pandas as pd
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QDesktopServices, QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, \
    QAbstractScrollArea, QPushButton, QHBoxLayout
from PyQt6.uic.properties import QtCore

from GUI.Custom.CustomDialog import CustomDialog, ContentType
from GUI.Menu.QRCodesWidget import QRCodesWidget
from GUI.Navigation import Ui_MainWindow
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
        self.current_table.cellDoubleClicked.connect(self.open_image)
        self.filename_to_export = None
        self.text_qlabel_option = QLabel("")
        # combo_option_class_type

    def load_and_display_tube_info(self):
        tubeid_input_text = self.ui.tube_info_tubeid_input.text()
        if tubeid_input_text:
            self.append_info_to_view(tubeid_input_text, self.ui.combo_option_class_type.currentText())
        else:
            self.main_window.dialog.add_titlebar_name("Query Info")
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

    def append_info_to_view(self, input_id, current_option):

        data_for_table = None
        is_tube_selected = False
        text_label_for_option = ""
        try:
            if current_option == 'Experiment':
                # Create the left-aligned label
                text_label_for_option = f"{current_option} {input_id} details: "
                data_for_table = self.main_window.ui_db.adapter.get_experiment_by_id(input_id)
                # Convert the Experimente instance to a dictionary
                if data_for_table:
                    data_for_table = vars(data_for_table)
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
                pixmap, image_location = qr_code_widget.generate_qr_code(data_for_table['qr_code'])
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
        # Add a stretch item
        h_layout.addStretch()

        # Add the export_btn
        export_btn = self.create_export_btn()
        h_layout.addWidget(export_btn)

        # Add the horizontal layout to the grid layout
        self.ui.tube_info_grid_layout.addLayout(h_layout, 0, 0)

        if not data_for_table:
            self.text_qlabel_option.setText(f"Could not load data for {current_option} with id {input_id}")
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

            # Populate the table with data
            for i, (key, value) in enumerate(data_for_table.items()):
                key_item = QTableWidgetItem(key)
                key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item non-editable
                self.current_table.setItem(i, 0, key_item)

                if key == 'pixmap':
                    label = QLabel()
                    label.setPixmap(value)
                    self.current_table.setCellWidget(i, 1, label)
                elif key == 'image_location':
                    value_item = QTableWidgetItem(value)
                    value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item non-editable
                    self.current_table.setItem(i, 1, value_item)
                else:
                    value_item = QTableWidgetItem(str(value))
                    value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item non-editable
                    self.current_table.setItem(i, 1, value_item)

            # Remove the background
            table.setObjectName('tube_info_table')

            # Set the size policy to expand to the available space
            table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # Add the table to the grid layout
            self.ui.tube_info_grid_layout.addWidget(table, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            self.data_for_table = data_for_table

        except Exception as ex:
            dialog = CustomDialog(self)
            dialog.addContent(f"{ex}", ContentType.OUTPUT)
            dialog.show()

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
