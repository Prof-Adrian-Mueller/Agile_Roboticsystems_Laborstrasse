from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QGroupBox, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QLabel, QLineEdit, QTableWidgetItem, QAbstractItemView, QHeaderView, QScrollArea, QFileDialog
from PyQt6.QtGui import QPainter, QPen, QIcon, QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QObject, QEvent, QTimer, QThread, QRect, QPoint

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class CustomWidget(QWidget):
    """
    Custom view for the Live View Table. Still on Work.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        scroll = QScrollArea(self)
        self.layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Disable horizontal scrolling

        frame = QFrame(scroll)
        scroll.setWidget(frame)

        layout = QVBoxLayout(frame)

        for i in range(10):
            widget = QWidget()
            widget.setObjectName("itemRowLiveData")
            layout.addWidget(widget)
            h_layout = QHBoxLayout(widget)

            buttons = []
            label = QLabel('ProbeNr')
            h_layout.addWidget(label)

            for j in range(3):
                button = QPushButton(f'{j + 1}')
                h_layout.addWidget(button)
                buttons.append(button)

            if len(buttons) > 1:
                arrow = ArrowWidget(buttons[0], buttons[1])
                arrow.setStyleSheet("margin:10px;background-color:#FF0000;")
                h_layout.addWidget(arrow)


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
