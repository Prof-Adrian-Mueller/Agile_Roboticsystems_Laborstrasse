from enum import Enum
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel, QScrollArea, QWidget, QHBoxLayout, QLineEdit
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
import GUI.resource_rc

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        # self.titleLabel = QLabel("")
        # self.layout.addWidget(self.titleLabel)
        self.layout.addStretch()
        self._dragging = False
        # Custom Styles
        self.setStyleSheet("""
            CustomTitleBar {
                background-color: #808080;  # Gray background
                color: white;  # White text
                font-size: 14px;  # Adjust font size as needed
                font-weight: bold;  # Bold font
            }
        """)

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
    OUTPUT = 2

class CustomDialog(QDialog):
    def __init__(self, parent=None, max_percentage=0.75):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint)
        self.max_percentage = max_percentage
        self.init_ui()
        

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.setStyleSheet("""
            QDialog {
                border: 1px solid #5B5B5B;
                background-color: #FFFFFF;
            }
        """)
        self.row_widgets = []
        # Custom Title Bar
        self.titleBar = CustomTitleBar(self)
        self.layout.addWidget(self.titleBar)

        self.send_button = QPushButton("Send")
        self.input_line_edit = QLineEdit(self)

        # Scroll Area
        self.scroll_area = QScrollArea(self)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget_contents)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)     

        # Close Button
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.hide)
        self.layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Update the size of the dialog dynamically
        self.update_size()

    def clear(self):
        for row_widget in self.row_widgets:
            self.scroll_area_layout.removeWidget(row_widget)
            row_widget.deleteLater()

    def addContent(self, content,content_type = ContentType):
        row_widget = QWidget()
        row_box = QHBoxLayout()
        if content_type == ContentType.OUTPUT:
            # Create and configure the label
            label = QLabel(content)
            label.setWordWrap(True)
            row_box.addWidget(label)

            # Create and configure the copy button
            copy_button = QPushButton("")
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/img/contentcopy.svg"), QIcon.Mode.Normal, QIcon.State.Off)
            copy_button.setIcon(icon1)
            copy_button.clicked.connect(lambda: QApplication.clipboard().setText(content))
            copy_button.setFixedHeight(30)
            copy_button.setFixedWidth(30)
            # Add the copy button to the horizontal layout
            row_box.addWidget(copy_button)

        elif content_type == ContentType.INPUT:
            label = QLabel(content, self)           
            row_box.addWidget(label)
            row_box.addWidget(self.input_line_edit)                     
            row_box.addWidget(self.send_button)


        # Set the layout for the row widget
        row_widget.setLayout(row_box)

        # Add the row widget to the scroll area's layout
        self.scroll_area_layout.addWidget(row_widget)
        self.row_widgets.append(row_widget)
        return row_widget

    

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
