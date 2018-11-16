"""
_
"""
from PySide.QtGui import QWidget, QPalette, QPixmap, QGridLayout, QLabel
from PySide.QtCore import Qt
from libs import json_reader

class Header(QWidget):
    """
    _
    :param QWidget parent: the widget's parent
    """
    def __init__(self, parent):
        self.parent = parent
        QWidget.__init__(self)
        self.setAutoFillBackground(True)
        bgCol = QPalette()
        bgCol.setColor(QPalette.Background, Qt.yellow)
        self.setPalette(bgCol)
        self.initUI()

    def initUI(self):
        """
        _
        """
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        imageLabel = QLabel(self)
        logo = QPixmap(json_reader.buildPath("gameheader.png"))
        imageLabel.setPixmap(logo)
        self.grid.addWidget(imageLabel, 0, 0, 2, 4)

        self.score1 = QLabel("0")
        self.score2 = QLabel("0")
        self.timer = QLabel("00:00")
        self.down = QLabel("1st")
        self.quarter = QLabel("1")

        self.grid.addWidget(self.score1, 0, 0, 2, 1)
        self.grid.addWidget(self.score2, 0, 3, 2, 1)
        self.grid.addWidget(self.timer, 0, 1, 1, 2)
        self.grid.addWidget(self.down, 1, 1)
        self.grid.addWidget(self.quarter, 1, 2)
