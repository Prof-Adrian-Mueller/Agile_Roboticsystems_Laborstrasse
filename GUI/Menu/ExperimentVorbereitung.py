from GUI.Navigation import Ui_MainWindow


class ExperimentVorbereitung:
    def __init__(self, ui: Ui_MainWindow, main_window):
        self.ui = ui
        self.main_window = main_window
        

    def nextPage(self):
        print("weiter clicked")
        current_index = self.ui.vorbereitungStackedTab.currentIndex()
        if current_index < self.ui.vorbereitungStackedTab.count() - 1:
            self.ui.vorbereitungStackedTab.setCurrentIndex(current_index + 1)

    def prevPage(self):
        print("prev clicked")
        current_index = self.ui.vorbereitungStackedTab.currentIndex()
        if current_index > 0:
            self.ui.vorbereitungStackedTab.setCurrentIndex(current_index - 1)