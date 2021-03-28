import os
import sys
from typing import Any

import django


from PyQt5 import QtWidgets

sys.dont_write_bytecode = True
os.environ['DJANGO_SETTINGS_MODULE'] = 'n2edm.settings'
django.setup()

from ....core.objects import *


