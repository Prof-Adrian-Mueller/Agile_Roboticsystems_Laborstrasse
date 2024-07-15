from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QCheckBox, QPushButton, QLineEdit, QLabel, \
    QSizeGrip
from PyQt6.QtCore import QSize, Qt

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class Settings(QWidget):
    """
    Settings for changing user interface. Still on Progress.
    """

    def __init__(self, ui=None, main_window=None, parent=None):
        super().__init__(parent)
        self.ui = ui
        self.main_window = main_window
        self.original_sizes = {}

        # Create a vertical layout
        self.layout = QVBoxLayout(self)

        # Create another vertical layout for the colors
        v_layout_colors = QVBoxLayout()
        self.color_layout_title = QLabel("Change colors of Respective Field using Hex Colors ex. #FFFFFF")
        v_layout_colors.addWidget(self.color_layout_title)

        # Create a QLabel for each color
        self.table_label = QLabel("Table color")
        self.widget_label = QLabel("Widget color")
        self.button_label = QLabel("Button color")

        # Create a QLineEdit for each color
        self.table_color = QLineEdit()
        self.table_color.setPlaceholderText("Enter table color")
        self.widget_color = QLineEdit()
        self.widget_color.setPlaceholderText("Enter widget color")
        self.button_color = QLineEdit()
        self.button_color.setPlaceholderText("Enter button color")

        # Create a QHBoxLayout for each pair of label and lineedit
        self.table_layout = QHBoxLayout()
        self.widget_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()

        # Add the labels and line edits to the corresponding horizontal layouts
        self.table_layout.addWidget(self.table_label, 1)
        self.table_layout.addWidget(self.table_color, 2)
        self.widget_layout.addWidget(self.widget_label, 1)
        self.widget_layout.addWidget(self.widget_color, 2)
        self.button_layout.addWidget(self.button_label, 1)
        self.button_layout.addWidget(self.button_color, 2)

        # Add the horizontal layouts to the v_layout_colors
        v_layout_colors.addLayout(self.table_layout)
        v_layout_colors.addLayout(self.widget_layout)
        v_layout_colors.addLayout(self.button_layout)

        # Create a push button
        self.applyButton = QPushButton("Apply", self)
        self.applyButton.clicked.connect(self.apply_color)
        v_layout_colors.addWidget(self.applyButton)

        # Add the v_layout_colors to the self.layout
        self.layout.addLayout(v_layout_colors)

        # Create a size grip widget
        self.sizeGrip = QSizeGrip(self)
        # Add the size grip widget to the self.layout
        self.layout.addWidget(self.sizeGrip, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        # Set the layout for the widget
        self.setLayout(self.layout)

    def apply_color(self):
        # Get the text from each line edit for colors
        table_color = self.table_color.text()
        widget_color = self.widget_color.text()
        button_color = self.button_color.text()

        # Get the current style sheets of the main window and widgets
        main_style = self.main_window.styleSheet()
        table_style = self.table_label.styleSheet()
        button_style = self.button_label.styleSheet()

        # Update only the background color in the style sheets
        main_style = self.update_style(main_style, "QWidget", "background-color", widget_color)
        table_style = self.update_style(table_style, "QLabel", "background-color", table_color)
        button_style = self.update_style(button_style, "QPushButton", "background-color", button_color)

        # Apply the updated styles
        self.main_window.setStyleSheet(main_style)
        self.table_label.setStyleSheet(table_style)
        self.button_label.setStyleSheet(button_style)

    def update_style(self, current_style, widget_selector, property_name, new_value):
        import re

        # Regex to find the existing property value
        pattern = f"({widget_selector} \\{{[\\s\\S]*?{property_name}: )[^;]+(;[\\s\\S]*?\\}})"
        replacement = f"\\1{new_value}\\2"

        # If the property exists, update it, otherwise add it
        if re.search(pattern, current_style):
            return re.sub(pattern, replacement, current_style)
        else:
            return current_style + f"\n{widget_selector} {{{property_name}: {new_value};}}\n"

    def store_original_sizes(self):
        child_widgets = self.ui.leftNavigation.findChildren(QWidget)
        for widget in child_widgets:
            self.original_sizes[widget] = widget.size()

    def resize_child_sizes(self, value):
        child_widgets = self.ui.leftNavigation.findChildren(QWidget)
        for widget in child_widgets:
            if not isinstance(widget, (QHBoxLayout, QVBoxLayout, QGridLayout)):
                original_size = self.original_sizes.get(widget, QSize(100, 100))
                scale_factor = 1 + value / 100
                new_width = original_size.width() * scale_factor
                new_height = original_size.height() * scale_factor

                widget.setMinimumSize(new_width, new_height)
                widget.setMaximumSize(new_width * 1.1, new_height * 1.1)

    def resize_window(self, value):
        child_widgets = self.ui.leftNavigation.findChildren(QWidget)
        original_sizes = {}

        # Store original sizes of child widgets
        for widget in child_widgets:
            original_sizes[widget] = widget.size()

        # Calculate new window size and resize the window
        new_width = 800 + value * 10
        new_height = 600 + value * 10
        self.main_window.resize(QSize(new_width, new_height))

        # Resize child widget sizes based on original sizes and scale factor
        for widget in child_widgets:
            if not isinstance(widget, (QHBoxLayout, QVBoxLayout, QGridLayout)):
                original_size = original_sizes.get(widget, QSize(100, 100))
                scale_factor = 1 + value / 100
                new_width = original_size.width() * scale_factor
                new_height = original_size.height() * scale_factor

                widget.setMinimumSize(new_width, new_height)
                widget.setMaximumSize(new_width * 1.1, new_height * 1.1)

