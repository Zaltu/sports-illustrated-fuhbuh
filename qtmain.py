# --coding:utf-8--
import sys

from PySide.QtGui import QApplication, QIcon
from gui.qtmainframe import MainFrame
from libs import json_reader

APP = QApplication(sys.argv)
APP.setWindowIcon(QIcon(json_reader.buildPath('icon.gif')))
M = MainFrame(APP)
sys.exit(APP.exec_())
