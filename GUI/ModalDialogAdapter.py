from PyQt6.QtWidgets import QWidget
from GUI.Navigation import Ui_MainWindow
from PyQt6.QtCore import Qt

class ModalDialogAdapter(QWidget):
    def __init__(self, parent=None, ui=Ui_MainWindow):
        super().__init__(parent)
        self.parent = parent
        self.ui = ui
        # self.ui.closeBtnModal.clicked.connect(self.close_btn)

    # def close_btn(self):
    #     self.ui.modalDialogBackground.hide()
    #     print("close btn clicked!")

    # def hideDialog(self):
    #     self.ui.modalDialogBackground.hide()
    #     self.ui.modalDialog.hide()

    # def showDialog(self):
    #     self.ui.modalDialogBackground.show()
    #     self.ui.modalDialog.show()
    #     self.ui.modalDialogBackground.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
    #     self.ui.modalDialog.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

    # def displayText(self, str):
    #     self.ui.modalBoxText.setText(str)
    #     self.ui.modalBoxText.adjustSize()
    #     self.ui.modalBoxText.setWordWrap(True)