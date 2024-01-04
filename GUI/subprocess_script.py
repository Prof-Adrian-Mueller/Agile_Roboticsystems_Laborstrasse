from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QWidget, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Set up the main layout and dialog properties
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)  # This is the viewport offset
        self.layout.setSpacing(10)
        self.setWindowTitle("Custom Dialog")

        # Apply shadow effect to the dialog
        shadow_effect = QGraphicsDropShadowEffect(blurRadius=15, color=QColor(0, 0, 0, 150))
        self.setGraphicsEffect(shadow_effect)

        # Header with close button
        self.header_layout = QHBoxLayout()
        self.header_label = QLabel("<Header>", self)
        self.close_button = QLabel("X", self)
        self.close_button.setStyleSheet("font-size: 18px; cursor: pointer;")
        self.close_button.mouseReleaseEvent = self.closeEvent
        self.header_layout.addWidget(self.header_label)
        self.header_layout.addStretch()  # This will push the close button to the right
        self.header_layout.addWidget(self.close_button)

        # Body content
        self.body_label = QLabel("<Body>", self)

        # Footer with buttons
        self.footer_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel", self)
        self.save_button = QPushButton("Save", self)
        self.footer_layout.addWidget(self.cancel_button)
        self.footer_layout.addStretch()  # This will push the save button to the right
        self.footer_layout.addWidget(self.save_button)

        # Adding header, body, and footer to the main layout
        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.body_label)
        self.layout.addLayout(self.footer_layout)

        # Styling
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                border-radius: 8px;
            }
            QLabel {
                font-size: 16px;
            }
            QPushButton {
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 16px;
                margin: 5px;
            }
        """)

        # Connect buttons
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.accept)

    def closeEvent(self, event):
        self.close()


import sys
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    # Create and show the custom dialog
    dialog = CustomDialog()
    dialog.show()

    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
