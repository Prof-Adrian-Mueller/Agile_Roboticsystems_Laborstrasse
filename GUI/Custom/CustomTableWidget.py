from PyQt6.QtWidgets import QTableWidget, QPushButton, QTableWidgetItem, QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QPoint

class CustomTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arrows = {}  # Dictionary to store arrows

    def add_row(self, row_name):
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.setItem(row_position, 0, QTableWidgetItem(row_name))
        
        start_button = QPushButton("")
        end_button = QPushButton("")
        self.setCellWidget(row_position, 1, start_button)
        self.setCellWidget(row_position, 2, end_button)
        
        self.arrows[start_button] = (start_button, end_button)  # Save the arrow

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)

        for start_button, (start_button, end_button) in self.arrows.items():
            start_pos = self.cellWidget_position(start_button)
            end_pos = self.cellWidget_position(end_button)
            
            if start_pos is not None and end_pos is not None:
                painter.drawLine(start_pos, end_pos)

    def cellWidget_position(self, widget):
        if widget is not None:
            rect = widget.geometry()
            center = rect.center()
            return widget.mapToParent(center)
        return None
