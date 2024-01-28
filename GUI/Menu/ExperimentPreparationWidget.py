from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QLineEdit, QTextEdit, QComboBox, QSpinBox, \
    QDoubleSpinBox, QDateEdit

from GUI.Custom.CustomDialog import CustomDialog, ContentType
from GUI.Storage.BorgSingleton import MainWindowSingleton


class ExperimentPreparationWidget(QWidget):
    def __init__(self, vorbereitungStackedTab, parent=None):
        super().__init__(parent)
        self.vorbereitung_index = None
        self.vorbereitungStackedTab = vorbereitungStackedTab

        # Make sure the QStackedWidget has an expanding size policy
        self.vorbereitungStackedTab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add the QStackedWidget to the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.vorbereitungStackedTab)

        self.setLayout(layout)

        for index in range(vorbereitungStackedTab.count()):
            widget = vorbereitungStackedTab.widget(index)
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            if isinstance(widget, QWidget):
                widget.update()
        vorbereitungStackedTab.update()

    def addToMainWindow(self, main_window):
        try:
            if main_window and main_window.tab_widget_home_dashboard:
                self.remove_vorbereitung_tab_if_exists(main_window)
                main_window.tab_widget_home_dashboard.addTab(self, "Vorbereitung")
                main_window_singleton = MainWindowSingleton(main_window)
                vorbereitung_index = main_window.tab_widget_home_dashboard.indexOf(self)
                main_window.tab_widget_home_dashboard.setCurrentIndex(vorbereitung_index)
                main_window_singleton.add_stacked_tab_index("vorbereitung", vorbereitung_index)
        except Exception as ex:
            dialog = CustomDialog(self)
            dialog.add_titlebar_name("Experiment Preparation Widget")
            dialog.addContent(ex, ContentType.ERROR)
            dialog.show()

    def remove_vorbereitung_tab_if_exists(self, main_window):
        tab_widget = main_window.tab_widget_home_dashboard
        vorbereitung_tab_title = "Vorbereitung"

        # Iterate over the tabs to find the "Vorbereitung" tab
        for index in range(tab_widget.count()):
            if tab_widget.tabText(index) == vorbereitung_tab_title:
                # "Vorbereitung" tab found, remove it
                tab_widget.removeTab(index)
                break  # Exit the loop once the tab is found and removed

    def removeFromMainWindow(self, main_window):
        try:
            if main_window and main_window.tab_widget_home_dashboard:
                # Remove the tab using the stored index
                main_window_singleton = MainWindowSingleton(main_window)
                index = main_window_singleton.get_stacked_tab_index("vorbereitung")
                main_window.tab_widget_home_dashboard.removeTab(index)
        except Exception as ex:
            dialog = CustomDialog(self)
            dialog.add_titlebar_name("Experiment Preparation Widget")
            dialog.addContent(ex, ContentType.OUTPUT)
            dialog.show()

    def reset_input_of_past_experiments(self):
        for index in range(self.vorbereitungStackedTab.count()):
            widget = self.vorbereitungStackedTab.widget(index)

            # Reset all QLineEdit widgets to an empty string
            for line_edit in widget.findChildren(QLineEdit):
                line_edit.clear()

            # Reset all QTextEdit widgets to an empty string
            for text_edit in widget.findChildren(QTextEdit):
                text_edit.clear()

            # Reset all QComboBox widgets to the first index
            for combo_box in widget.findChildren(QComboBox):
                combo_box.setCurrentIndex(0)

            # Reset all QSpinBox and QDoubleSpinBox widgets to their minimum value
            for spin_box in widget.findChildren(QSpinBox):
                spin_box.setValue(spin_box.minimum())
            for double_spin_box in widget.findChildren(QDoubleSpinBox):
                double_spin_box.setValue(double_spin_box.minimum())

            # Reset all QDateEdit widgets to their default date, if one is specified
            for date_edit in widget.findChildren(QDateEdit):
                date_edit.setDate(date_edit.minimumDate())

        self.vorbereitungStackedTab.setCurrentIndex(0)
