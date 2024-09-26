import logging

from PyQt5.QtCore import QRect, Qt, QSize, QLine, QEvent
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QSizePolicy,
    QScrollArea,
    QPushButton,
    QAction,
)
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont, QHelpEvent, QCursor


from ..api import ScheduleAPI, BaseItemAPI
from .dialogs import ScheduleItemCreateDialog, ScheduleItemEditDialog
from .helpers import QMenu
from typing import Any, Union

logger = logging.getLogger("n2edm")


BASE_API = BaseItemAPI()
SCHEDULE_API = ScheduleAPI()


class ScheduleWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.group_scroll = QScrollArea()
        self.groups = Groups(self)
        self.group_scroll.setWidget(self.groups)
        self.group_scroll.setWidgetResizable(True)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(self.group_scroll)
        self.setLayout(self.main_layout)

        self.main_layout.setSpacing(1)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        logger.info("ScheduleWindow initialized successfully")

        h_bar = self.group_scroll.horizontalScrollBar()
        h_bar.valueChanged.connect(self.groups.bar_moved)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()

        pen.setColor(QColor("black"))
        pen.setStyle(Qt.SolidLine)
        pen.setWidthF(1)
        brush = QBrush(QColor("white"))
        painter.setPen(pen)
        painter.setBrush(brush)
        rect = QRect(0, 0, painter.device().width(), painter.device().height())
        painter.drawRect(rect)

    def add_schedule_item(self, set_item):
        schedule_dialog = ScheduleItemCreateDialog(self, set_item)
        schedule_dialog.exec()
        if schedule_dialog.closed:
            return
        start_time, stop_time, sequence, continuous = list(schedule_dialog.attributes.values())
        schedule_item_data = {
            "set_item": set_item,
            "start_time": start_time,
            "stop_time": stop_time,
            "sequence": sequence,
            "continuous": continuous,
        }
        schedule_item = SCHEDULE_API.create_item(schedule_item_data)

        group = self.get_or_create_group(schedule_item)
        group.add_item(schedule_item)

    def get_or_create_group(self, schedule_item):
        item = schedule_item.group_item if schedule_item.group_item else schedule_item.set_item
        group = self.get_group(item)
        if not group:
            group = self.add_group(item)
        return group

    def add_group(self, group_item):
        group = self.groups.add_group(group_item.name, group_item.uid)
        return group

    def get_group(self, group_item):
        group = [x for x in self.groups.findChildren(Group) if x.uid == group_item.uid]
        return group[0] if group else None

    def bulk_create_items(self, items: list):
        self.clear()
        for item in items:
            schedule_item = SCHEDULE_API.create_item(item)
            group = self.get_or_create_group(schedule_item)
            group.add_item(schedule_item)

    def clear(self):
        self.groups.clear()

    def remove_items(self, item):
        uids = [x.uid for x in item.children()]
        for iframe in self.findChildren(Item):
            if iframe.uid in uids:
                iframe.deleteLater()

        group = self.get_group(item)
        if group:
            group.deleteLater()

    def update_items(self, set_item):
        children_uids = [item.uid for item in set_item.children()]
        for iframe in self.findChildren(Item):
            if iframe.uid in children_uids:
                iframe.update_item()


class Groups(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 10, 10, 10)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.max_width = 0
        self.offset_left = 100

    def add_group(self, label, uid: int = 0):
        group = Group(self, label, uid)
        self.layout.addWidget(group)
        return group

    def paintEvent(self, event):
        pen = QPen()
        pen.setColor(QColor("white"))
        pen.setStyle(Qt.SolidLine)
        pen.setWidthF(1.5)
        painter = QPainter(self)
        brush = QBrush(QColor("white"))
        painter.setBrush(brush)
        painter.setPen(pen)
        rect = QRect(0, 0, painter.device().width(), painter.device().height())
        painter.drawRect(rect)
        self.setFixedWidth(max(self.parent.width(), self.max_width))
        color_primary = QColor("black")
        color_primary.setAlpha(70)
        color_secondary = QColor("black")
        color_secondary.setAlpha(40)
        pen.setColor(color_primary)
        color_text = QColor("black")
        horizontal_line_y = max(painter.device().height() - 30, painter.device().height() * 0.9)
        for wh in range(0, painter.device().width(), 10):
            line = QLine(wh + self.offset_left, 1, wh + self.offset_left, horizontal_line_y)
            if not wh % 100:
                pen.setColor(color_primary)
                painter.setPen(pen)
                painter.drawLine(line)
                pen.setColor(color_text)
                painter.setPen(pen)
                painter.drawText(
                    wh - 25 + self.offset_left,
                    horizontal_line_y + 1,
                    50,
                    max(30, painter.device().height()),
                    4,
                    str(wh),
                )
            else:
                pen.setColor(color_secondary)
                painter.setPen(pen)
                painter.drawLine(line)

        color_primary.setAlpha(255)
        pen.setColor(color_primary)

        line = QLine(
            0,
            horizontal_line_y - 10,
            painter.device().width() + 50,
            horizontal_line_y - 10,
        )
        painter.setPen(pen)
        painter.drawLine(line)

    def clear(self):
        for frame in self.findChildren(QWidget):
            frame.deleteLater()

    def remove_selection(self):
        for item in self.findChildren(Item):
            item.remove_selection()

    def mousePressEvent(self, event):
        self.remove_selection()

    def bar_moved(self, pos):
        self.bar_position = pos


class Group(QWidget):
    def __init__(self, parent, label, uid):

        super().__init__(parent)
        self.setMinimumHeight(30)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.uid = uid
        self.parent = parent
        self.offset_left = self.parent.offset_left
        self.text = label

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    def add_item(self, schedule_item):
        start = schedule_item.start_time
        width = schedule_item.stop_time - schedule_item.start_time
        item = Item(self, schedule_item)
        item.show()
        self.parent.max_width = start + width
        logger.info(f"{self.add_item.__name__}:{schedule_item}, 0")

    def delete(self):
        for frame in self.findChildren(QFrame):
            frame.delete()
        self.deleteLater()

    def delete_set_children(self): ...

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()

        pen.setColor(QColor("black"))
        pen.setStyle(Qt.SolidLine)

        line = QLine(
            self.offset_left - 4,
            painter.device().height() / 2,
            painter.device().width(),
            painter.device().height() / 2,
        )
        painter.setPen(pen)
        painter.drawLine(line)

        pen.setColor(QColor("black"))
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)

        painter.drawText(
            0,
            0,
            self.offset_left - 6,
            painter.device().height(),
            Qt.AlignVCenter | Qt.AlignRight,
            self.text,
        )

    def contextMenuEvent(self, event: QEvent) -> None:
        """Context menu controller for Item

        Args:
            event (QtCore.QEvent): QContextEvent
        """
        if event.pos().x() >= self.offset_left:
            return
        self.menu = QMenu(self)
        remove_group_item_action = QAction("Delete", self)
        remove_group_item_action.triggered.connect(self.delete)
        self.menu.addAction(remove_group_item_action)
        self.menu.popup(QCursor.pos())


class Item(QFrame):
    def __init__(self, parent, schedule_item):
        super().__init__(parent)
        self.parent = parent
        self.offset_left = self.parent.offset_left
        self.color = schedule_item.color
        self.uid = schedule_item.uid
        self.text = schedule_item.set_item.name
        self.start = schedule_item.start_time
        self.stop = schedule_item.stop_time
        self.initial_scpi_command = schedule_item.set_item.initial_scpi_command
        self.final_scpi_command = schedule_item.set_item.final_scpi_command
        self.selected = False
        self.highlight = QColor(self.color).darker().name()
        self.selected_color = QColor(self.color).darker(135).name()
        self.setMinimumWidth(1)
        self.setMinimumHeight(10)
        self.setGeometry(
            self.start + self.offset_left,
            self.parent.height() / 4,
            self.stop - self.start,
            self.parent.height() / 2,
        )
        self.setMouseTracking(True)
        self.setStyleSheet(
            f"""
        Item {{
            background-color: {self.color}; 
        }}
        Item:hover {{
            background-color: {self.highlight}; 
        }}
        """
        )

    def update_item(self):
        schedule_item = SCHEDULE_API.get_item(self.uid)
        self.color = schedule_item.color
        self.uid = schedule_item.uid
        self.text = schedule_item.set_item.name
        self.start = schedule_item.start_time
        self.stop = schedule_item.stop_time
        self.initial_scpi_command = schedule_item.set_item.initial_scpi_command
        self.final_scpi_command = schedule_item.set_item.final_scpi_command
        self.highlight = QColor(self.color).darker().name()
        self.selected_color = QColor(self.color).darker(135).name()
        if self.selected:
            self.setStyleSheet(
                f"""
        Item {{
            background-color: {self.selected_color};
        }}
        """
            )
        else:
            self.setStyleSheet(
                f"""
        Item {{
            background-color: {self.color}; 
        }}
        Item:hover {{
            background-color: {self.highlight}; 
        }}
        """
            )
        self.setGeometry(
            self.start + self.offset_left,
            self.parent.height() / 4,
            self.stop - self.start,
            self.parent.height() / 2,
        )
        self.update()

    def remove_selection(self):
        self.selected = False
        self.setStyleSheet(
            f"""
        Item {{
            background-color: {self.color}; 
        }}
        Item:hover {{
            background-color: {self.highlight}; 
        }}
        """
        )

    def mousePressEvent(self, event):
        self.parent.parent.remove_selection()
        self.selected = not self.selected
        if self.selected:
            self.setStyleSheet(
                f"""
        Item {{
            background-color: {self.selected_color};
        }}
        """
            )
        else:
            self.setStyleSheet(
                f"""
        Item {{
            background-color: {self.color}; 
        }}
        Item:hover {{
            background-color: {self.highlight}; 
        }}
        """
            )

    def delete(self):
        SCHEDULE_API.remove_item(self.uid)
        self.deleteLater()

    def contextMenuEvent(self, event: QEvent) -> None:
        """Context menu controller for Item

        Args:
            event (QtCore.QEvent): QContextEvent
        """
        self.menu = QMenu(self)
        update_schedule_item_action = QAction("Edit", self)
        remove_schedule_item_action = QAction("Delete", self)
        update_schedule_item_action.triggered.connect(self.open_schedule_item_update_dialog)
        remove_schedule_item_action.triggered.connect(self.delete)
        self.menu.addAction(update_schedule_item_action)
        self.menu.addAction(remove_schedule_item_action)
        self.menu.popup(QCursor.pos())

    def open_schedule_item_update_dialog(self):
        schedule_item = SCHEDULE_API.get_item(self.uid)
        schedule_dialog = ScheduleItemEditDialog(self, schedule_item)
        schedule_dialog.exec()
        start_time, stop_time, sequence, continuous = list(schedule_dialog.attributes.values())
        schedule_item_data = {
            "start_time": start_time,
            "stop_time": stop_time,
            "sequence": sequence,
            "continuous": continuous,
        }
        if not schedule_dialog.closed:
            SCHEDULE_API.update_item(self.uid, schedule_item_data)
            self.update_item()
