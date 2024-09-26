from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class colorQPushButton(QtWidgets.QPushButton):
    """QPush button that serves as color lookout and selector

    Args:
        QtWidgets (_type_): _description_
    """

    def __init__(self, name):
        super().__init__()
        self.rgba = "#000000"
        self.setStyleSheet("QPushButton {background-color:%s;}" % self.rgba)

    def mousePressEvent(self, event):
        self.q_color = QtWidgets.QColorDialog.getColor()
        self.rgba = self.q_color.name()
        self.setStyleSheet("QPushButton {background-color:%s;}" % self.rgba)

    def color(self):
        return self.rgba

    def set_color(self, color):
        self.rgba = color
        self.setStyleSheet("QPushButton {background-color:%s;}" % color)


class QMenu(QtWidgets.QMenu):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    def mouseReleaseEvent(self, event):
        print(event)
        if event.button() == 2:
            event.ignore()
        else:
            super().mouseReleaseEvent(event)
