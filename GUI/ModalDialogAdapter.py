from PyQt6.QtWidgets import QWidget
from GUI.Navigation import Ui_MainWindow

class ModalDialogAdapter(QWidget):
    def __init__(self, parent=None, ui=Ui_MainWindow):
        super().__init__(parent)
        self.parent = parent
        self.ui = ui
        self.ui.closeBtnModal.clicked.connect(self.close_btn)

    def close_btn(self):
        self.ui.modalDialogBackground.hide()
        print("close btn clicked!")