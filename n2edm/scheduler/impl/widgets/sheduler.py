import sys
import os
import django
from typing import Any
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as mpe
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

sys.dont_write_bytecode = True
os.environ["DJANGO_SETTINGS_MODULE"] = "n2edm.settings"
django.setup()

from ....widgets.views import SchedulerView
from ....core.objects import *
from ....core.handlers import *

class Scheduler(SchedulerView):
    def __init__(self, parent: Any) -> None:
        super().__init__(parent=parent)
        self.create_canvas()
        self.set_canvas_attributes(100)
        self.set_canvas_labels()
        self.group_handler = GroupHandler()
        self.action_handler = ActionHandler()
        self.actor_handler = ActorHandler()
        self.seq_handler = SequenceHandler("file")

    def draw_actor(self, actor):
        bbox = self.ax.get_window_extent().transformed(
            self.figure.dpi_scale_trans.inverted()
        )
        WIDTH = 2 * bbox.height
        outline = mpe.withStroke(linewidth=1.1, capstyle="butt")

        (line2d,) = plt.plot(
            [actor.start, actor.stop],
            [actor.position, actor.position],
            lw=WIDTH,
            color=actor.color,
            pickradius=5,
            ms=0,
        )

        line2d.set_path_effects([outline])
        self.canvas.draw()

    def draw_infinit_actor(self, actor, color="blue"):
        bbox = self.ax.get_window_extent().transformed(
            self.figure.dpi_scale_trans.inverted()
        )
        WIDTH = 2 * bbox.height
        outline = mpe.withStroke(linewidth=1.1, capstyle="projecting")

        (line2d,) = plt.plot(
            [actor.start, self.ax.get_xlim()[1]],
            [actor.group.position, actor.group.position],
            lw=WIDTH,
            color=color,
            pickradius=5,
            ms=0,
        )

        line2d.set_path_effects([outline])
        self.canvas.draw()
        

    def create_canvas(self) -> None:
        """Create matplotlib canvas and tollbar"""
        self.figure, self.ax = plt.subplots()

        self.canvas = FigureCanvas(self.figure)
        self.main_layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.main_layout.addWidget(self.toolbar)

    def set_canvas_attributes(self, Y_MAX) -> None:
        """Sets canvas attributes"""
        bbox = self.ax.get_window_extent().transformed(
            self.figure.dpi_scale_trans.inverted()
        )
        WIDTH = 2 * bbox.height

        mpl.rcParams["lines.solid_capstyle"] = "butt"
        self.ax.grid(True)
        self.ax.set_xbound(0)
        self.ax.set_ylim(25, -1)
        self.ax.set_xlim(-1, 200)
        plt.yticks(range(-2, 25))
        self.set_canvas_labels()

    def set_canvas_labels(self) -> None:
        self.ax.set_yticklabels(["", "Timeline"] + [""] * 25)
        self.figure.tight_layout()
        self.canvas.draw()

    def update_canvas(self):
        for actor in ActorObject.all():
            self.canvas.draw()

    def create_actor(self, action):

        #positioning of actors in y axis (vertical line)
        if action.group == None and action.position == None:
            ActionHandler.set_position(action)

        elif action.group != None and action.group.position == None:
            GroupHandler.set_position(action.group)
   
        #attributes for actor to create
        attributes = {
            "name": action.name,
            "group": action.group,
            "action": action,
            "start": 0,
            "stop": 0,
            "duration": action.duration,
            "color": action.color,
            "params": action.params,
            "annotate": action.name,
            "text": action.name,
            "position": action.position,
        }

        #creating actor
        actor = ActorObject.create(**attributes)

        ActorHandler.calculate_vertical_position(actor)

        # print(vars(actor))
        self.draw_actor(actor)
