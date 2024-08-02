from enum import Enum
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel, QScrollArea, QWidget, QHBoxLayout, \
    QLineEdit, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QColor
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QScrollArea, QWidget
import GUI.resource
from PyQt6 import sip

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class CustomTitleBarForDialogBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._dragging = False
        # Custom Styles
        self.setStyleSheet("""
                background-color: #FFFFFF; 
                color: black;  # White text
                font-size: 14px;  # Adjust font size as needed
                font-weight: bold;  # Bold font
        """)

        self.title = QLabel("")
        self.layout.addWidget(self.title)
        self.title.setStyleSheet("background-color:transparent; font-weight: bold;")

        self.layout.addStretch()

        # Close 'X' Icon
        self.close_icon = QLabel("X", self)
        self.close_icon.setObjectName('closeIconDialog')  # Use object name for specific styling
        self.close_icon.setStyleSheet("""
            QLabel#closeIconDialog {
                font-size: 12px; /* Larger font size for the 'X' */
                color: #818181; /* White color for the close icon */
                margin-right: 10px; /* Spacing from the right edge */
                cursor: pointer; /* Change cursor to indicate clickable */
                padding: 5px 8px; /* Padding to make the 'X' look centered and increase clickable area */
                border-radius: 10px; /* Rounded corners */
                border: 1px solid #fef2d7; /* White border to match the 'X' */
                background-color: transparent; /* Transparent background by default */
            }
            QLabel#closeIconDialog:hover {
                background-color: #818181; /* Grey background on hover */
                color: #FFFFFF;
            }
        """)

        self.close_icon.mouseReleaseEvent = self.closeEvent
        self.layout.addWidget(self.close_icon, alignment=Qt.AlignmentFlag.AlignRight)

    def closeEvent(self, event):
        self.parent().close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_position = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._dragging = False
        event.accept()


class ContentType(Enum):
    INPUT = 1,
    OUTPUT = 2,
    ERROR=3


class CustomDialog(QDialog):
    """
    Main Dialog Box to show any Error or Message
    """
    sendButtonClicked = pyqtSignal(str)

    def __init__(self, parent=None, max_percentage=0.75):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint)

        self.setMinimumWidth(600)
        self.scroll_area = None
        self.layout = None
        self.titleBar = None
        self.row_widgets = None
        self.max_percentage = max_percentage
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: transparent;")
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                border-radius: 8px; 
                border: 1px solid #F2F0EB;
            }
            QWidget {
                background-color: #FFFFF;
            }
            QPushButton {
                border-radius: 15px; 
                padding: 10px 20px; 
                font-size: 16px; 
                margin: 5px; 
                border: 1px solid #F2F0EB; 
                background:color: #FFFFFF;
            }
            QPushButton#closeButton {
                background-color: #FF3B30; 
                color: white;
            }
            QPushButton#saveButton {
                background-color: #34C759; 
                color: white;
            }
            QScrollArea {
                border: none; /* Remove scroll area border */
            }
        """)

        self.row_widgets = []

        # Custom Title Bar
        self.titleBar = CustomTitleBarForDialogBox(self)
        self.layout.addWidget(self.titleBar)
        self.add_titlebar_name("Custom Title Bar")

        # Scroll Area
        self.scroll_area = QScrollArea(self)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget_contents)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Apply shadow effect
        self.shadow_effect = QGraphicsDropShadowEffect(self)
        self.shadow_effect.setBlurRadius(20)
        self.shadow_effect.setColor(QColor(0, 0, 0, 80))
        self.shadow_effect.setOffset(2, 2)
        self.setGraphicsEffect(self.shadow_effect)
        # Update the size of the dialog dynamically
        self.update_size()

        self.lineEditTextChanged = ""

    def clear(self):
        for row_widget in self.row_widgets:
            for child in row_widget.children():
                if isinstance(child, QLineEdit) and child is self.input_line_edit:
                    continue

            self.scroll_area_layout.removeWidget(row_widget)
            row_widget.deleteLater()

    def add_titlebar_name(self, name):
        self.titleBar.title.setText(name)

    def removeItems(self, row_data):
        """
        Remove contents of the Dialog Box
        """
        for row_widget in row_data:
            # Check if the widget is valid and not deleted
            if row_widget is not None and not sip.isdeleted(row_widget):
                # Safely remove the widget from the layout
                self.scroll_area_layout.removeWidget(row_widget)
                # Delete the widget
                row_widget.deleteLater()

                # Remove the widget from the row_widgets list if it's there
                if row_widget in self.row_widgets:
                    self.row_widgets.remove(row_widget)

    def addContent(self, content, content_type=ContentType):
        global label
        row_widget = QWidget()
        row_box = QHBoxLayout()
        if content_type == ContentType.ERROR:
            row_widget.setStyleSheet("QLabel { color: red }")
            self.content_addition_template(content, row_box)

        if content_type == ContentType.OUTPUT:
            self.content_addition_template(content, row_box)

        elif content_type == ContentType.INPUT:
            label = QLabel(content, self)
            row_box.addWidget(label)
            input_line_edit = QLineEdit(self)
            input_line_edit.textChanged.connect(self.emitTextChanged)
            row_box.addWidget(input_line_edit)
            send_button = QPushButton("Send")
            send_button.clicked.connect(lambda: self.sendButtonClicked.emit(input_line_edit.text()))
            row_box.addWidget(send_button)

        # Set the layout for the row widget
        row_widget.setLayout(row_box)


        # Add the row widget to the scroll area's layout
        self.scroll_area_layout.addWidget(row_widget)
        self.row_widgets.append(row_widget)
        return row_widget

    def content_addition_template(self, content, row_box):
        row_widget = QWidget()
        if isinstance(content, str):
            # If the content is a string, create a label and a copy button
            label = QLabel(content)
            label.setWordWrap(True)
            row_box.addWidget(label)

            copy_button = QPushButton("")
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/img/contentcopy.svg"), QIcon.Mode.Normal, QIcon.State.Off)
            copy_button.setIcon(icon1)
            copy_button.clicked.connect(lambda: QApplication.clipboard().setText(content))
            copy_button.setFixedHeight(30)
            copy_button.setFixedWidth(30)
            row_box.addWidget(copy_button)
        else:
            row_box.addWidget(content)
        row_widget.setLayout(row_box)
        self.scroll_area_layout.addWidget(row_widget)
        self.row_widgets.append(row_widget)

    def emitTextChanged(self, text):
        self.lineEditTextChanged = text

    def update_size(self):
        self.setFixedWidth(int(self.parent().width() * 0.8))
        self.setMaximumHeight(int(self.parent().height() * 0.8))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main_window = QDialog()
    main_window.resize(800, 600)

    dialog = CustomDialog(main_window)
    dialog.show()

    sys.exit(app.exec())
