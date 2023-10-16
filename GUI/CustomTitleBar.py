from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.draggable = True
        self.startPos = None
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        # App logo
        app_logo = QLabel(self)
        pixmap = QPixmap("img/laboratory.svg")
        scaled_pixmap = pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        app_logo.setPixmap(scaled_pixmap)
        layout.addWidget(app_logo)

        layout.addStretch(1)

        # Minimize button
        minimize_btn = QPushButton("-")
        minimize_btn.clicked.connect(self.parent.showMinimized)
        minimize_btn.setObjectName("minimizeButton")
        layout.addWidget(minimize_btn)

        # Close button
        close_btn = QPushButton("X")
        close_btn.clicked.connect(self.parent.close)
        close_btn.setObjectName("closeButton")
        layout.addWidget(close_btn)

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.MouseButton.LeftButton:
            self.startPos = event.globalPosition()
            self.clickPos = event.position()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & Qt.MouseButton.LeftButton:
            if self.startPos:
                move = event.globalPosition() - self.startPos
                self.parent.move(self.parent.pos() + move.toPoint())  # Convert move to QPoint
                self.startPos = event.globalPosition()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPos = None

    def setDraggable(self, draggable):
        self.draggable = draggable