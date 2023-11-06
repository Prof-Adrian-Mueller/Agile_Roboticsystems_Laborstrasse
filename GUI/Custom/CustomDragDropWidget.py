from PyQt6.QtWidgets import QWidget

class DragDropWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

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
                print(f'Dropped Excel file: {path}')
            else:
                print(f'Ignored non-Excel file: {path}')