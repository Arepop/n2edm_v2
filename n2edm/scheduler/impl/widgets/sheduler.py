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
from ....core.objects import (
    GroupObject,
    ActorObject,
    ActionObject,
    TimelineObject,
    InfinitActorObject,
)
from ....core.handlers import *


class Scheduler(SchedulerView):
    def __init__(self, parent: Any) -> None:
        super().__init__(parent=parent)
        self.create_canvas()
        self.set_canvas_attributes(100)
        self.set_canvas_labels()
        self.group_handler = GroupHandler()
        self.group = GroupObject.create(self.group_handler, name="mojagrupa")
        self.group2 = GroupObject.create(self.group_handler, name="mojagrupa2")

        self.handler = Handler()
        self.seq_handler = SequenceHandler("file")
        self.actor_handler = ActorHandler()
        self.action_handler = ActionHandler()
        self.infinit_actor_handler = InfinitActorHandler()

        self.action1 = ActionObject.create(
            name="name1", duration=20, start_cmd="act1_cmd", stop_cmd="act1_stop_cmd"
        )
        self.action2 = ActionObject.create(
            name="name2", duration=20, start_cmd="act2_cmd", stop_cmd="act2_stop_cmd"
        )
        self.action3 = ActionObject.create(
            name="name3", duration=30, start_cmd="act3_cmd", stop_cmd="act3_stop_cmd"
        )

        self.actor1 = ActorObject.create(
            name="act1", start=1, stop=2, action=self.action1
        )

        self.actor2 = ActorObject.create(
            name="act2", start=23, stop=26, action=self.action2
        )

        self.actor3 = ActorObject.create(
            name="act3", start=1, stop=32, action=self.action3
        )

        self.seq_handler.update_sequence()

    def draw_actor(self, actor, color="blue"):
        bbox = self.ax.get_window_extent().transformed(
            self.figure.dpi_scale_trans.inverted()
        )
        WIDTH = 2 * bbox.height
        outline = mpe.withStroke(linewidth=1.1, capstyle="projecting")

        (line2d,) = plt.plot(
            [actor.start, actor.stop],
            [actor.position, actor.position],
            lw=WIDTH,
            color=color,
            pickradius=5,
            ms=0,
        )

        line2d.set_path_effects([outline])

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

    def create_actor(self, action, a=1, b=2):
        attributes = {
            "name": action.name,
            "group": action.group,
            "action": action,
            "start": None,
            "stop": None,
            "duration": action.duration,
            "color": action.color,
            "params": action.params,
            "annotate": action.name,
            "text": action.name,
            # tutaj ma być position,jeśli jest None to ma wybrać sobie nową
        }
        if action.group == None:
            attributes["position"] = Handler.max_pos
            Handler.max_pos += 1

        else:
            attributes["position"] = action.group.position

        # tutaj powinien znajdować się qt dialog z pytaniem o start i stop
        attributes["start"] = a
        attributes["stop"] = b

        actor = ActorObject.create(self.actor_handler, **attributes)
        self.seq_handler.update_sequence()
        return actor
