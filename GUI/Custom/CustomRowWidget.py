from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt

class CustomRowWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.start_button = QPushButton("Start")
        self.middle_button = QPushButton("Middle")
        self.end_button = QPushButton("End")
        
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.middle_button)
        self.layout.addWidget(self.end_button)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        # Draw arrow from start button to middle button
        start_pos = self.start_button.geometry().topRight()
        end_pos = self.middle_button.geometry().topLeft()
        painter.drawLine(start_pos, end_pos)

        # Draw arrow from middle button to end button
        start_pos = self.middle_button.geometry().topRight()
        end_pos = self.end_button.geometry().topLeft()
        painter.drawLine(start_pos, end_pos)
