from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy

from GUI.Navigation import Ui_MainWindow


class TubeInformation(QWidget):

    def __init__(self, ui: Ui_MainWindow, main_window):
        super().__init__()
        self.ui = ui
        self.main_window = main_window
        # combo_option_class_type

    def load_and_display_tube_info(self):
        tubeid_input_text = self.ui.tube_info_tubeid_input.text()
        if tubeid_input_text:
            print(tubeid_input_text)
            self.append_info_to_view(tubeid_input_text)
        else:
            self.main_window.show_message_in_dialog("Please Enter Tube Id to proceed!")

    def append_info_to_view(self, tube_id):
        # Create the left-aligned label
        left_label = QLabel(f"Tube {tube_id} details:")
        left_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Create the right-aligned label
        right_label = QLabel("Right-aligned text")
        right_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Add the labels to the grid layout
        self.ui.tube_info_grid_layout.addWidget(left_label, 0, 0)  # Add to row 0, column 0
        self.ui.tube_info_grid_layout.addWidget(right_label, 0, 1)  # Add to row 0, column 1

        # Create the table
        table = QTableWidget()
        table.setRowCount(5)
        table.setColumnCount(2)
        table.setMinimumSize(500, 500)

        table.setHorizontalHeaderLabels(['Key Name', 'Value'])
        # Hide the row and column headers
        table.verticalHeader().hide()

        for i in range(5):
            for j in range(3):
                item = QTableWidgetItem(f'Item {i + 1}-{j + 1}')
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item non-editable
                table.setItem(i, j, item)

            # Remove the background
            table.setObjectName('tube_info_table')

            # Set the size policy to expand to the available space
            table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # Add the table to the grid layout
            self.ui.tube_info_grid_layout.addWidget(table, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
