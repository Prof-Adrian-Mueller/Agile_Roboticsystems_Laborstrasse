from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QSizePolicy
import sys

from GUI.Custom.DummyDataGenerator import DummyDataGenerator

class CustomDataTable(QTableWidget):
    def __init__(self, df, parent=None):
        super().__init__(parent)
        self.df = df
        self.setRowCount(len(df))
        self.setColumnCount(len(df.columns))
        self.setHorizontalHeaderLabels(df.columns)
        self.setVerticalHeaderLabels(df.index.astype(str))
        self.fill_table()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.resizeColumnsToContents()

    def fill_table(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem(str(self.df.iat[i, j])))


