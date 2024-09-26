import sys
import traceback as trs
import logging
from datetime import datetime
from pathlib import Path

from .frontend.main_window import MainWindow
from .frontend.dialogs import ErrorDialog
from PyQt5 import QtWidgets

current_time = datetime.now().strftime("%Y_%m_%d")
path_to_logs = Path("/home/arek/Documents/Scripts/logs")

if not path_to_logs.exists():
    path_to_logs.mkdir()

logging.basicConfig(
    filename=f"{path_to_logs.as_posix()}/log_{current_time}.txt",
    filemode="a",
    format="%(asctime)s:%(msecs)d | %(name)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger("n2edm")


def exception_hook(exctype, value, traceback):
    """Catcheng errors to Dialog window.

    Args:
        exctype (str): exepion type
        value (str): value of excepiton
        traceback (str): text of exception
    """
    traceback_formated = trs.format_exception(exctype, value, traceback)
    traceback_string = "".join(traceback_formated) + "\n"
    dialog = ErrorDialog(exctype, value, traceback, traceback_string)
    logging.exception(traceback_string)
    dialog.exec()


def main():
    """Runs main application window"""
    sys.excepthook = exception_hook
    app = QtWidgets.QApplication(sys.argv)
    GUI = MainWindow()
    GUI.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
