from PySide.QtGui import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from PySide.QtCore import Qt

class Connect(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setWindowModality(Qt.ApplicationModal)


    def showUI(self):
        self.show()


    def finish(self):
        self.close()


class AskConnect(Connect):

    def __init__(self):
        Connect.__init__(self)
        self.initUI()
        Connect.showUI(self)

    def initUI(self):
        title = QLabel("Enter IP address of the person you wish to connect to.")
        self.grid.addWidget(title, 0, 0, 2, 1)

        ipL = QLabel("IP:")
        self.grid.addWidget(ipL, 0, 1)

        ip = QLineEdit()
        self.grid.addWidget(ip, 1, 1)

        attemptConnection = QPushButton("Connect")
        attemptConnection.clicked.connect(self.tryConnect)
        self.grid.addWidget(attemptConnection, 0, 2)

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.cancel)
        self.grid.addWidget(cancel, 1, 2)


    def tryConnect(self):
        pass


    def cancel(self):
        Connect.finish(self)

class AskedConnect(Connect):

    def __init__(self):
        Connect.__init__(self)
