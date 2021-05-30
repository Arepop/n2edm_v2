import sys
import os
import traceback as trs
import logging
from datetime import datetime
import django

sys.dont_write_bytecode = True
os.environ["DJANGO_SETTINGS_MODULE"] = "n2edm.settings"
django.setup()

from .impl.widgets.base import Base
from ..widgets.dialogs import ErrorDialog

from PyQt5 import QtWidgets

current_time = datetime.now().strftime("%Y_%m_%d_%H_%M")

logging.basicConfig(filename=f"logs/log_{current_time}.txt",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.WARN)

logger = logging.getLogger('n2edm')

def exception_hook(exctype, value, traceback):
    traceback_formated = trs.format_exception(exctype, value, traceback)
    traceback_string = "".join(traceback_formated) + "\n"
    dialog = ErrorDialog(exctype, value, traceback, traceback_string)
    logging.exception(traceback_string)    
    dialog.exec()

def main():
    sys.excepthook = exception_hook
    app = QtWidgets.QApplication(sys.argv)
    GUI = Base()
    GUI.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


