import sys
import os
from .impl.widgets.base import Base

from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Base()
    GUI.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
