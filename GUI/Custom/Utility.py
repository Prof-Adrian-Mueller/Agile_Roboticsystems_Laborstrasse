from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import QSize
from PyQt6.QtSvg import QSvgRenderer


class Utility:
    @staticmethod
    def get_colored_svg_pixmap(svg_path, color, size=QSize(32, 32)):
        # Create a QPixmap with the appropriate size
        pixmap = QPixmap(size)
        pixmap.fill(QColor("transparent"))  # Start with a transparent pixmap

        # Create a QPainter to draw on the pixmap
        painter = QPainter(pixmap)

        # Create an SVG renderer for the SVG data
        svg_renderer = QSvgRenderer(svg_path)

        # Render the SVG onto the pixmap
        svg_renderer.render(painter)

        # Set the composition mode to 'SourceIn' to apply the color
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)

        # Fill the pixmap with the specified color
        painter.fillRect(pixmap.rect(), QColor(color))

        # End the painting operation
        painter.end()

        return pixmap


# Then, when you create your QIcon and want to add the pixmap:
icon1 = QIcon()
white_pixmap = Utility.get_colored_svg_pixmap(":/icons/img/contentcopy.svg", "white")
icon1.addPixmap(white_pixmap, QIcon.Mode.Normal, QIcon.State.Off)
