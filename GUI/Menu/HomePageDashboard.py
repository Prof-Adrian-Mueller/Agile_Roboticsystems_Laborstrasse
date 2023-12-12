from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy


class HomePageDashboard(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)

        # Set size policy to expanding
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a QVBoxLayout
        self.vbox_layout = QVBoxLayout(self)
        self.setStyleSheet("border:1px solid #FF0000;")

        # Create a label and add it to the layout
        label = QLabel("Label")
        self.vbox_layout.addWidget(label)

        # Create a horizontal layout for buttons
        hbox_layout = QHBoxLayout()

        # Create buttons and add them to the horizontal layout
        button1 = QPushButton("Button 1")
        hbox_layout.addWidget(button1)

        # Add a stretch to push the next widget (button2) to the right
        hbox_layout.addStretch()

        button2 = QPushButton("Button 2")
        hbox_layout.addWidget(button2)

        # Add the horizontal layout to the vertical layout
        self.vbox_layout.addLayout(hbox_layout)

        # Example usage of show_start_button
        self.show_start_button()

    def create_refresh_btn(self):
        return QPushButton("Refresh")

    def show_start_button(self):
        # Create a widget and set its object name
        widget = QWidget()
        widget.setObjectName("displayQrCode")

        # Create a horizontal layout for the widget
        h_layout = QHBoxLayout(widget)

        # Create a vertical box layout
        qr_vertical_box = QVBoxLayout()

        # Add a label and a QR code label to the vertical box layout
        label = QLabel("Your Text")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        qr_code_label = QLabel("Your QR Code")
        qr_code_label.setObjectName("qrCodeLabel")
        qr_vertical_box.addWidget(label)
        qr_vertical_box.addWidget(qr_code_label)

        # Create a widget for the vertical box layout
        v_widget = QWidget()
        v_widget.setLayout(qr_vertical_box)

        # Create a label for the probe number
        probe_nr_text = QLabel("Your Probe Number")
        probe_nr_text.setFixedWidth(120)

        # Create the buttons
        drucken = QPushButton("Drucken")
        speichern = QPushButton("Speichern")

        # Add the widgets and buttons to the horizontal layout
        h_layout.addWidget(v_widget)
        h_layout.addWidget(probe_nr_text)

        # Add a stretch to push the buttons to the right
        h_layout.addStretch()

        h_layout.addWidget(speichern)
        h_layout.addWidget(drucken)

        # Add the widget to your main QVBoxLayout
        self.vbox_layout.addWidget(widget)

