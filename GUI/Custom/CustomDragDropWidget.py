from PyQt6.QtWidgets import QWidget
from DBService.DBUIAdapter import DBUIAdapter

class DragDropWidget(QWidget):
    def __init__(self, parent=None, db_ui=DBUIAdapter):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.db_ui = db_ui

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.endswith('.xls') or path.endswith('.xlsx'):
                # TODO provide data to importer
                self.db_ui.insert_metadaten(path)
                print(f'Dropped Excel file: {path}')
            else:
                print(f'Ignored non-Excel file: {path}')