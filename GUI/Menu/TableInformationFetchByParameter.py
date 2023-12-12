from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy

from GUI.Navigation import Ui_MainWindow


class TableInformationFetchByParameter(QWidget):

    def __init__(self, ui: Ui_MainWindow, main_window):
        super().__init__()
        self.current_table = None
        self.ui = ui
        self.main_window = main_window
        # combo_option_class_type

    def load_and_display_tube_info(self):
        tubeid_input_text = self.ui.tube_info_tubeid_input.text()
        if tubeid_input_text:
            print(tubeid_input_text)
            self.append_info_to_view(tubeid_input_text, self.ui.combo_option_class_type.currentText())
        else:
            self.main_window.show_message_in_dialog("Please Enter Tube Id to proceed!")

    def append_info_to_view(self, input_id, current_option):
        global text_label_for_option
        data_for_table = None
        if current_option == 'Experiment':
            # Create the left-aligned label
            text_label_for_option = f"{current_option} {input_id} details: "
            data_for_table = self.main_window.ui_db.get_experiment_by_id(input_id)
        elif current_option == 'Plasmid':
            text_label_for_option = f"{current_option} {input_id} details: "
            # data_for_table = self.main_window.ui_db.
            # data_for_table = self.main_window.ui_db.
        elif current_option == 'Tube':
            text_label_for_option = f"{current_option} {input_id} details: "

        text_qlabel_option = QLabel(text_label_for_option)
        text_qlabel_option.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Create the right-aligned label
        right_label = QLabel("Details")
        right_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Add the labels to the grid layout
        self.ui.tube_info_grid_layout.addWidget(text_qlabel_option, 0, 0)  # Add to row 0, column 0
        self.ui.tube_info_grid_layout.addWidget(right_label, 0, 1)  # Add to row 0, column 1

        if not data_for_table:
            text_qlabel_option.setText(f"Could not load data for {current_option} with id {input_id}")
            pass

        try:
            # Remove the old table from the layout, if it exists
            if hasattr(self, 'current_table') and self.current_table:
                self.ui.tube_info_grid_layout.removeWidget(self.current_table)
                self.current_table.deleteLater()
            # Convert the Experimente instance to a dictionary
            data_for_table = vars(data_for_table)
            # Create the table
            table = QTableWidget()
            table.setMinimumSize(500, 500)
            self.current_table = table
            
            # Set the number of rows and columns based on the data
            table.setRowCount(len(data_for_table))
            table.setColumnCount(2)

            table.setHorizontalHeaderLabels(['Key Name', 'Value'])
            # Hide the row and column headers
            table.verticalHeader().hide()

            # Populate the table with data
            for i, (key, value) in enumerate(data_for_table.items()):
                key_item = QTableWidgetItem(key)
                key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item non-editable
                table.setItem(i, 0, key_item)

                value_item = QTableWidgetItem(str(value))
                value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item non-editable
                table.setItem(i, 1, value_item)

            # Remove the background
            table.setObjectName('tube_info_table')

            # Set the size policy to expand to the available space
            table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # Add the table to the grid layout
            self.ui.tube_info_grid_layout.addWidget(table, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        except Exception as ex:
            print(ex)

