import sys
import os
from .impl.widgets.main_window import MainWindow

from PyQt5 import QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)
    GUI = MainWindow()
    GUI.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
