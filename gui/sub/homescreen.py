from PySide.QtGui import QWidget, QPalette, QPixmap, QGridLayout, QLabel
from PySide.QtCore import Qt
from libs import json_reader

class HomeScreen(QWidget):

    def __init__(self, parent):
        self.parent = parent
        QWidget.__init__(self)
        print "Application started"
        self.setAutoFillBackground(True)
        bgCol = QPalette()
        bgCol.setColor(QPalette.Background, Qt.black)
        self.setPalette(bgCol)
        self.initUI()

    def initUI(self):
        self.mainframe.setWindowTitle("1972 Sports Illustrated Football")

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        imageLabel = QLabel(self)
        logo = QPixmap(json_reader.buildPath("homescreen.png"))
        imageLabel.setPixmap(logo)
        self.grid.addWidget(imageLabel, 0, 0)
