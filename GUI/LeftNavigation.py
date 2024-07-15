from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QPushButton

# from GUI.Utils.ColoredSVGIcon import ColoredSVGIcon


class LeftNavigation:
    """
    Left Navigation Buttons
    """

    def __init__(self, ui, main_window):
        self.ui = ui
        self.main_window = main_window
        self.buttons = [self.ui.home_btn_dashboard, self.ui.statistik, self.ui.importBtn,
                        self.ui.settingsBtn, self.ui.cliBtn,
                        self.ui.experimentPreparationBtn,
                        self.ui.experiment_info_btn]

    def map_buttons_to_pages(self):

        # Connect all the buttons to its respective button and highlight it
        for button in self.buttons:
            button.clicked.connect(lambda checked, b=button: self.highlight_button(b))

        # Connect all the buttons to its respective button
        # self.ui.homeBtn.clicked.connect(
        #     lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.homePage)))
        self.ui.home_btn_dashboard.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.test_page_home)))
        self.ui.statistik.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.statistikPage)))
        self.ui.importBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.importPage)))
        self.ui.settingsBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.settingsPage)))
        self.ui.cliBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.cliPage)))
        self.ui.experimentPreparationBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(
            self.ui.stackedWidget.indexOf(self.ui.experimentPreparationPage)))
        self.ui.experiment_info_btn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.experiment_info_view)))

    def highlight_button(self, button):
        try:
            # Reset all buttons color to default
            for btn in self.buttons:
                btn.setStyleSheet("")

            # Change the color of the clicked (active) button
            button.setStyleSheet("background-color: #1B5E20")
            self.update_title_bar(button)
        except Exception as ex:
            print(f"Error while highlighting button: {ex}")

    def update_title_bar(self, button):
        # Check which button was clicked and update the title bar text
        if button == self.ui.home_btn_dashboard:
            self.main_window.setCustomWindowTitle("Dashboard UI | Home Dashboard")
        elif button == self.ui.statistik:
            self.main_window.setCustomWindowTitle("Dashboard UI | Statistics")
        elif button == self.ui.importBtn:
            self.main_window.setCustomWindowTitle("Dashboard UI | Import")
        elif button == self.ui.settingsBtn:
            self.main_window.setCustomWindowTitle("Dashboard UI | Settings")
        elif button == self.ui.cliBtn:
            self.main_window.setCustomWindowTitle("Dashboard UI | Command Line Interface")
        elif button == self.ui.experimentPreparationBtn:
            self.main_window.setCustomWindowTitle("Dashboard UI | Search")
        elif button == self.ui.experiment_info_btn:
            self.main_window.setCustomWindowTitle("Dashboard UI | Experiment Information")
