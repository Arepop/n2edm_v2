import sys
import os
import django
from typing import Any
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as mpe
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from time import time

sys.dont_write_bytecode = True
os.environ["DJANGO_SETTINGS_MODULE"] = "n2edm.settings"
django.setup()

from ....widgets.views import SchedulerView
from ....core.objects import *
from ....core.handlers import *
from ....widgets.dialogs import CustomActorTime


class Scheduler(SchedulerView):

    actor_and_artist = {}

    def __init__(self, parent: Any) -> None:
        super().__init__(parent=parent)
        self.create_canvas()
        self.set_canvas_attributes(100)
        self.set_canvas_labels()

        self.event = None
        self.pick_event = self.canvas.mpl_connect("pick_event", self.pick_event)
        self.button_press_event = self.canvas.mpl_connect(
            "button_press_event", self.lmb_double_click)
        self.motion_notify_event = self.canvas.mpl_connect(
            "motion_notify_event", self.on_hover)

    def draw_actor(self, actor):
        bbox = self.ax.get_window_extent().transformed(
            self.figure.dpi_scale_trans.inverted()
        )
        WIDTH = 2 * bbox.height
        outline = mpe.withStroke(linewidth=1.1, capstyle="butt")

        (line2d,) = self.ax.plot(
            [actor.start, actor.stop],
            [actor.position, actor.position],
            lw=WIDTH,
            color=actor.color,
            picker=True,
            pickradius=5,
            ms=0,
        )

        line2d.set_path_effects([outline])
        self.actor_and_artist[actor] = line2d
        self.canvas.draw()

    def draw_infinit_actor(self, actor, color="blue"):
        bbox = self.ax.get_window_extent().transformed(
            self.figure.dpi_scale_trans.inverted()
        )
        WIDTH = 2 * bbox.height
        outline = mpe.withStroke(linewidth=1.1, capstyle="projecting")

        (line2d,) = self.ax.plot(
            [actor.start, self.ax.get_xlim()[1]],
            [actor.group.position, actor.group.position],
            lw=WIDTH,
            color=color,
            picker=True,
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

    def create_custom_actor(self, action):
        # attributes for actor to create
        attributes = {
            "name": action.name,
            "group": action.group,
            "action": action,
            "execution_time": 0,
            "start": 0,
            "stop": 0,
            "duration": action.duration,
            "color": action.color,
            "params": action.params,
            "annotate": action.name,
            "text": action.name,
            "position": action.position,
            "execution_time": time(),
        }

        custom_dialog = CustomActorTime(self, attributes)
        custom_dialog.exec()

        # creating actor
        actor = ActorObject.create(**attributes)
        # print(vars(actor))
        self.draw_actor(actor)

    def create_actor(self, action):
        attributes = {
            "name": action.name,
            "group": action.group,
            "action": action,
            "execution_time": 0,
            "start": 0,
            "stop": 0,
            "duration": action.duration,
            "color": action.color,
            "params": action.params,
            "annotate": action.name,
            "text": action.name,
            "position": action.position,
            "execution_time": time(),
        }

        # creating actor
        actor = ActorObject.create(**attributes)
        self.draw_actor(actor)

    def object_deleted(self, obj):
        for actor, artist in self.actor_and_artist.items():
            if actor in Object.deleted_objects:
                try:
                    artist.remove()
                except ValueError:
                    continue

        self.update_line2d_position()

        self.canvas.draw()

    def update_line2d_position(self):
        for actor, artist in self.actor_and_artist.items():
            artist.set_ydata([actor.position, actor.position])


    def pick_event(self, event: Any) -> None:
        """Gets clicked actor

        Args:
            event (MouseEvent): Mouse click event
        """
        self.event = event
            
    def contextMenuEvent(self, event: Any) -> None:
        """Context menu for actors

        Args:
            event (event): Mouse rbm click event

        """
        self.menu = QtWidgets.QMenu(self)
        del_action = QtWidgets.QAction("Delete...", self)
        del_action.triggered.connect(
            lambda: self.delete_actor(self.artist))
        self.menu.addAction(del_action)
        self.menu.popup(QtGui.QCursor.pos())

    def lmb_double_click(self, event: Any) -> None:
        """Opens time wizzard window after db click on actor

        Args:
            event (event): Mouse db click event
        """
        pass

    def on_hover(self, event: Any) -> None:
        """Handles hover events and annotations in schedule

        Args:
            event (event): Mouse move event

        """
        pass

    def delete_actor(self, picked_line2d):
        for actor, line2d in self.actor_and_artist.items():
            if picked_line2d == line2d:
                actor.delete()
                self.object_deleted(actor)

    