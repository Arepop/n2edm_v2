from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic

class colorQPushButton(QtWidgets.QPushButton):
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
