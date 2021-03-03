from PySide.QtGui import QWidget, QGridLayout, QPushButton, QPixmap, QIcon
from libs import json_reader
from src import GAME

class TeamSelect(QWidget):

    def __init__(self, parent):
        self.parent = parent
        QWidget.__init__(self)
        self.initUI()


    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        teamnames = json_reader.readJSON('teams.json')

        i = 0
        j = 0
        for team in teamnames:
            tbutton = QPushButton(team['name'])
            team_pic = QPixmap("%s.jpg"%team['name'])
            tbutton.setIcon(QIcon(team_pic))
            tbutton.setIconSize(team_pic.rect().size())
            tbutton.clicked.connect(lambda t=team: self.chooseTeam(t))
            self.grid.addWidget(tbutton, i % 10, j)
            i += 1
            j = j + 1 if i % 10 == 0 else j # this is the dumb


    def chooseTeam(self, team):
        GAME.setTeam(team)
        self.parent.changeState(GAME.state)
