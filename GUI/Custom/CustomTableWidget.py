from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QTableWidget

class CustomTableWidget(QTableWidget):
    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self.viewport())
        pen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        
        for row in range(self.rowCount()):
            for col in range(1, 3): 
                start_button = self.cellWidget(row, col)
                end_button = self.cellWidget(row, col + 1)
                
                if start_button is not None and end_button is not None:
                    start_pos = start_button.geometry().center() + QPoint(start_button.width() / 2, 0)
                    end_pos = end_button.geometry().center() - QPoint(end_button.width() / 2, 0)
                    
                    painter.drawLine(start_pos, end_pos)
