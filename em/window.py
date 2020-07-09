from PySide2 import QtCore, QtGui, QtWidgets

class Window(QtWidgets.QLabel):
    def __init__(self, gif, geometry):
        super().__init__()

        width, height = gif.dimensions()

        self.setWindowTitle('Loading Emacs...')
        self.resize(width, height)
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight,
                QtCore.Qt.AlignCenter,
                self.size(),
                geometry))
        self.show()
