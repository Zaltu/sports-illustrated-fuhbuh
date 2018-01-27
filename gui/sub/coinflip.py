from PySide.QtGui import QWidget

class CoinFlip(QWidget):

	def __init__(self, parent):
		self.parent = parent
		QWidget.__init__(self)