# ViCodePy - A video coder for psychological experiments
#
# Copyright (C) 2024 Esteban Milleret
# Copyright (C) 2024 Rafael Laboissière
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

from abc import abstractmethod
from enum import IntEnum

from PySide6.QtCore import (
    Qt,
    QRectF,
    QLine,
    QPointF,
    QSizeF,
    Signal,
)
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPolygonF,
    QPen,
    QFontMetrics,
)
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QDialog,
    QLineEdit,
    QColorDialog,
    QComboBox,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QGraphicsItem,
    QMenu,
    QMessageBox,
    QScrollBar,
    QAbstractSlider,
)

from .dialog import TimelineDialog
from .ticklocator import TickLocator
from .utils import color_fg_from_bg
from .comment import AnnotationComment
from .events import ChooseEvent, ChangeEvent


class ZoomableGraphicsView(QGraphicsView):
    MARGIN_BOTTOM = 15.0

    def __init__(self, scene: QGraphicsScene, parent=None):
        super().__init__(scene, parent)
        self.zoomFactor = 1.0
        self.zoomStep = 1.2
        self.zoomShift = None
        self.minimum_zoomFactor = 1.0

        vertical_scrollbar = QScrollBar(Qt.Orientation.Vertical, self)
        vertical_scrollbar.valueChanged.connect(
            self.on_vertical_scroll_value_changed
        )
        self.setVerticalScrollBar(vertical_scrollbar)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if not self.parent().video.media:
                return
            mouse_pos = self.mapToScene(event.position().toPoint()).x()
            if event.angleDelta().y() > 0:
                self.zoomShift = mouse_pos * (1 - self.zoomStep)
                self.zoom_in()
            else:
                self.zoomShift = mouse_pos * (1 - 1 / self.zoomStep)
                self.zoom_out()
            self.zoomShift = None
        elif event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            if event.angleDelta().y() > 0:
                action = QAbstractSlider.SliderSingleStepAdd
            else:
                action = QAbstractSlider.SliderSingleStepSub
            self.horizontalScrollBar().triggerAction(action)
        else:
            super().wheelEvent(event)

    def on_vertical_scroll_value_changed(self, value):
        if self.parent().time_pane_scale:
            self.parent().time_pane_scale.setPos(0, value)

    def zoom_in(self):
        self.zoomFactor *= self.zoomStep
        self.update_scale()

    def zoom_out(self):
        if self.zoomFactor / self.zoomStep >= self.minimum_zoomFactor:
            self.zoomFactor /= self.zoomStep
            self.update_scale()

    def update_scale(self):
        # Update the size of the scene with zoomFactor
        self.scene().setSceneRect(
            0,
            0,
            self.width() * self.zoomFactor,
            self.scene().height(),
        )

        if self.zoomShift:
            previousAnchor = self.transformationAnchor()
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.translate(self.zoomShift, 0)
            self.setTransformationAnchor(previousAnchor)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)

        # Get the position click from the scene
        map = self.mapToScene(self.scene().sceneRect().toRect())
        x = map.boundingRect().x()

        # Calculate the time of the position click
        time = int(
            (x + event.scenePosition().x())
            * self.parent().duration
            / self.scene().width()
        )

        self.parent().video.set_position(time)

    def set_position(self, time):
        # During the creation of a new annotation
        if self.parent().currentAnnotation:
            time = (
                self.parent().currentAnnotation.get_time_from_bounding_interval(
                    time
                )
            )

        # Cope with selected annotation
        for i in self.parent().scene.selectedItems():
            if isinstance(i, Annotation):
                time = i.get_time_from_bounding_interval(time)
                break

        # Set time to the video player
        self.parent().video.mediaplayer.setPosition(int(time))

    def keyPressEvent(self, event):
        pass


class TimePane(QWidget):
    CSV_HEADERS = ["timeline", "label", "begin", "end", "duration", "comment"]
    valueChanged = Signal(int)
    durationChanged = Signal(int)

    def __init__(self, video=None):
        """Initializes the timeline widget"""
        super().__init__(video)
        self._duration = 0
        self._value = 0

        self.selected_timeline = None
        self.currentAnnotation: Annotation = None
        self.video = video
        self.scene = QGraphicsScene()
        self.scene.sceneRectChanged.connect(self.on_scene_changed)
        self.scene.selectionChanged.connect(self.on_selection_changed)
        self.timeline_lines: list[Timeline] = []
        self.view = ZoomableGraphicsView(self.scene, self)
        self.cursor = None
        self.time_pane_scale = None

        self.view.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.view.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.setMouseTracking(True)
        self.scene.setSceneRect(0, 0, self.view.width(), self.view.height())

        self.valueChanged.connect(self.on_value_changed)
        self.durationChanged.connect(self.on_duration_changed)

        self.csv_needs_save = False

    def on_scene_changed(self, rect):
        # Update annotations
        for timeline_line in self.timeline_lines:
            timeline_line.update_rect_width(rect.width())
            for annotation in timeline_line.annotations:
                annotation.update_rect()

        if self.currentAnnotation:
            self.currentAnnotation.update_rect()

        # Update time_pane_scale display
        if self.time_pane_scale:
            # Update cursor
            if self.duration:
                self.time_pane_scale.cursor.setX(
                    self.value * rect.width() / self.duration
                )
            self.time_pane_scale.update_rect()

    def on_selection_changed(self):
        selected_items = self.scene.selectedItems()
        selected = None
        if len(selected_items) == 1:
            selected = selected_items[0]
            if isinstance(selected, Timeline):
                self.selected_timeline = selected
        for s in self.timeline_lines:
            s.select = s == selected

    def select_next_timeline(self):
        i, n = self.find_selected_timeline()
        self.timeline_lines[i].select = False
        if i == n - 1:
            i = 0
        else:
            i += 1
        self.select_timeline(self.timeline_lines[i])

    def select_previous_timeline(self):
        i, n = self.find_selected_timeline()
        self.timeline_lines[i].select = False
        if i == 0:
            i = n - 1
        else:
            i -= 1
        self.select_timeline(self.timeline_lines[i])

    def find_selected_timeline(self):
        n = len(self.timeline_lines)
        for i in range(n):
            if self.timeline_lines[i].select:
                break
        return i, n

    def select_timeline(self, line):
        line.select = True
        self.selected_timeline = line
        line.update()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != self._value:
            self._value = value
            self.valueChanged.emit(value)

    def on_value_changed(self, new_value):
        # First, update the current annotation, if it exists. If the cursor
        # value goes beyond the allowed bounds, bring it back and do not update
        # the other widgets.
        if self.currentAnnotation:
            if (
                self.currentAnnotation.lower_bound
                and new_value < self.currentAnnotation.lower_bound
            ):
                new_value = self.currentAnnotation.lower_bound
            elif (
                self.currentAnnotation.upper_bound
                and new_value > self.currentAnnotation.upper_bound
            ):
                new_value = self.currentAnnotation.upper_bound
                if (
                    self.video.mediaplayer.playbackState()
                    == QMediaPlayer.PlaybackState.PlayingState
                ):
                    self.video.mediaplayer.pause()
            start_time = self.currentAnnotation.startTime
            end_time = self.currentAnnotation.endTime
            mfps = self.video.mfps
            if start_time < end_time:
                if new_value >= start_time:
                    self.currentAnnotation.update_end_time(
                        new_value + int(mfps / 2)
                    )
                else:
                    self.currentAnnotation.update_start_time(end_time)
                    self.currentAnnotation.update_end_time(start_time - mfps)
            else:
                if new_value <= start_time:
                    self.currentAnnotation.update_end_time(
                        new_value - int(mfps / 2)
                    )
                else:
                    self.currentAnnotation.update_start_time(end_time)
                    self.currentAnnotation.update_end_time(start_time + mfps)

        # Cope with selected annotation
        for i in self.scene.selectedItems():
            if isinstance(i, Annotation):
                new_value = i.get_time_from_bounding_interval(new_value)
                break

        # Update cursor position
        if self.time_pane_scale and self.time_pane_scale.cursor:
            self.time_pane_scale.cursor.setX(
                new_value * self.scene.width() / self.duration
            )

        if isinstance(self.scene.focusItem(), AnnotationHandle):
            annotation_handle: AnnotationHandle = self.scene.focusItem()
            annotation_handle.change_time(new_value)

        # Change appearance of annotation under the cursor
        # (Brute force approach; this ought to be improved)
        if not self.currentAnnotation:
            for t in self.timeline_lines:
                for a in t.annotations:
                    a.penWidth = Annotation.PEN_WIDTH_OFF_CURSOR
            if self.selected_timeline:
                for a in self.selected_timeline.annotations:
                    if a.startTime <= new_value and a.endTime >= new_value:
                        a.penWidth = Annotation.PEN_WIDTH_ON_CURSOR
                        break

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        if duration != self._duration:
            self._duration = duration
            self.durationChanged.emit(duration)

    def on_duration_changed(self, new_duration):
        # Update timeline Scale
        self.time_pane_scale = TimePaneScale(self)
        self.update()

    def load_common(self):
        # Recreate timeline
        self.time_pane_scale = TimePaneScale(self)

    def clear(self):
        # Clear timelineScene
        self.scene.clear()
        self.timeline_lines = []

    def handle_annotation(self):
        """Handles the annotation"""
        if not self.selected_timeline:
            QMessageBox.warning(self, "Warning", "No timeline selected")
            return
        else:
            if self.currentAnnotation is None:
                can_be_initiate, lower_bound, upper_bound, annotation = (
                    Annotation.annotationDrawCanBeInitiate(
                        self.selected_timeline.annotations, self.value
                    )
                )
                if can_be_initiate:
                    self.currentAnnotation = Annotation(
                        self,
                        self.selected_timeline,
                        None,
                        None,
                        lower_bound,
                        upper_bound,
                    )
                self.video.add_annotation_action.setText("Finish annotation")
                self.video.abort_current_annotation_action.setEnabled(True)
                if annotation:
                    annotation.setSelected(not annotation.isSelected())
                    annotation.calculateBounds()

            else:
                # End the current annotation
                agd = EventDialog(
                    self.currentAnnotation.timeline_line
                )
                agd.exec()

                if agd.result() == AnnotationDialogCode.Accepted:
                    if agd.state == "create":
                        # When creating a new event, create the event and add the
                        # current annotation to it
                        event = Event(
                            len(self.currentAnnotation.timeline_line.events)
                            + 1,
                            agd.event_name_text.text(),
                            agd.color,
                            self,
                        )
                        event.add_annotation(self.currentAnnotation)
                        self.currentAnnotation.timeline_line.add_event(event)
                    else:
                        # Otherwise, we are selecting an existing event, and will
                        # retrieve the event and add the annotation to it
                        event = agd.combo_box.currentData()
                        event.add_annotation(self.currentAnnotation)
                    self.currentAnnotation.ends_creation()
                    self.currentAnnotation = None
                    self.on_value_changed(self.value)
                elif agd.result() == AnnotationDialogCode.Aborted:
                    self.currentAnnotation.remove()
                    self.currentAnnotation = None
                self.video.add_annotation_action.setText("Start annotation")
                self.video.abort_current_annotation_action.setEnabled(False)
                self.update()

    def handle_timeline_line(self):
        dialog = TimelineDialog(self)
        dialog.exec()
        if dialog.result() == AnnotationDialogCode.Accepted:
            self.add_timeline_line(Timeline(dialog.get_text(), self))

    def resizeEvent(self, a0):
        if self.time_pane_scale:
            origin = self.view.mapToScene(0, 0).x()
            width_before = self.scene.width() / self.view.zoomFactor
            width_after = self.view.width()
            shift = origin * (1 - width_after / width_before)
            self.view.update_scale()
            previousAnchor = self.view.transformationAnchor()
            self.view.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.view.translate(shift, 0)
            self.view.setTransformationAnchor(previousAnchor)
        else:
            self.scene.setSceneRect(
                0,
                0,
                self.view.width(),
                TimePaneScale.FIXED_HEIGHT + Timeline.FIXED_HEIGHT,
            )

        self.update()

    def abort_current_annotation(self):
        if self.currentAnnotation is not None:
            confirm_box = AnnotationConfirmMessageBox(self)
            if (
                confirm_box.result()
                == AnnotationConfirmMessageBox.DialogCode.Accepted
            ):
                self.currentAnnotation.remove()
                self.currentAnnotation = None
                self.update()
                self.video.abort_current_annotation_action.setEnabled(False)

    def add_timeline_line(self, line):
        self.timeline_lines.append(line)
        line.addToScene()

        # Calculate the new height of the scene
        new_height = (
            TimePaneScale.FIXED_HEIGHT
            + len(self.timeline_lines) * Timeline.FIXED_HEIGHT
            + ZoomableGraphicsView.MARGIN_BOTTOM
        )
        scene_rect = self.scene.sceneRect()
        scene_rect.setHeight(new_height)
        self.scene.setSceneRect(scene_rect)

        # Set maximum height of the widget
        self.setMaximumHeight(int(new_height))

        # Select the new timeline
        for i in self.timeline_lines:
            i.select = False
        line.select = True

    def get_timeline_line_by_name(self, name):
        """Get the timeline by name"""
        return next((x for x in self.timeline_lines if x.name == name), None)

    def hasAnnotations(self) -> bool:
        return any(len(line.annotations) for line in self.timeline_lines)

    def delete_annotation(self):
        for i in self.scene.selectedItems():
            if isinstance(i, Annotation):
                i.on_remove()
                break


class Timeline(QGraphicsRectItem):
    FIXED_HEIGHT: float = 60.0

    def __init__(self, name: str, time_pane: TimePane = None):
        super().__init__()
        self.name = name
        self.time_pane = time_pane
        self.annotations: list[Annotation] = []
        self.events: list[Event] = []
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptHoverEvents(True)
        self.textItem = TimelineLabel(self.name, self)
        self._select = False

    @property
    def select(self):
        return self._select

    @select.setter
    def select(self, select):
        if select != self._select:
            self._select = select

    def addToScene(self):
        """Add the timeline to the scene"""
        # Set Y of the timeline based on the timescale height and the timeline
        # lines heights present on the scene
        self.setPos(
            0,
            self.time_pane.time_pane_scale.rect().height()
            + (len(self.time_pane.timeline_lines) - 1) * self.FIXED_HEIGHT,
        )

        # Set the right rect based on the scene width and the height constant
        self.setRect(
            0,
            0,
            self.time_pane.scene.width(),
            self.FIXED_HEIGHT,
        )

        # Add line to the scene
        self.time_pane.scene.addItem(self)

    def add_event(self, event):
        """Add an event to the timeline"""
        self.events.append(event)
        self.events.sort(key=lambda x: x.name)

    def remove_event(self, event):
        """Remove a event from the timeline"""
        self.events.remove(event)

    def get_event_by_name(self, name):
        return next((x for x in self.events if x.name == name), None)

    def add_annotation(self, annotation):
        """Add an annotation to the timeline"""
        self.annotations.append(annotation)
        self.annotations.sort(key=lambda x: x.startTime)
        self.time_pane.csv_needs_save = True

    def remove_annotation(self, annotation):
        """Remove an annotation from the timeline"""
        self.annotations.remove(annotation)

    def update_rect_width(self, new_width: float):
        """Update the width of the timeline"""
        rect = self.rect()
        rect.setWidth(new_width)
        rect_label = self.textItem.rect()
        rect_label.setWidth(new_width)
        self.textItem.setRect(rect_label)
        self.setRect(rect)

    def on_remove(self):
        if self.annotations:
            answer = QMessageBox.question(
                self.time_pane,
                "Confirmation",
                "There are annotations present. "
                "Do you want to remove this timeline?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if answer == QMessageBox.StandardButton.Yes:
                while self.annotations:
                    self.annotations[0].remove()
        # The following does not yet work, since there is no provision for
        # adjusting the positions of the timelines inside the time pane.
        # self.time_pane.scene.removeItem(self)
        # if self in self.time_pane.timeline_lines:
        #     self.time_pane.timeline_lines.remove(self)
        # del self

    def edit_label(self):
        dialog = QDialog()
        dialog.setWindowTitle("Timeline label")

        label = QLineEdit()
        label.setText(self.textItem.text)
        label.returnPressed.connect(dialog.accept)
        edit = QHBoxLayout()
        edit.addWidget(label)

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(dialog.reject)
        save = QPushButton("Save")
        save.clicked.connect(dialog.accept)
        buttons = QHBoxLayout()
        buttons.addWidget(cancel)
        buttons.addWidget(save)

        layout = QVBoxLayout()
        layout.addLayout(edit)
        layout.addLayout(buttons)
        dialog.setLayout(layout)

        dialog.exec()
        if dialog.result() == dialog.DialogCode.Accepted:
            self.textItem.set_text(label.text())

    def edit_events(self):
        while True:
            events_dialog = ChooseEvent(
                self.events, "Choose the event to be modified:"
            )
            events_dialog.exec()
            if events_dialog.result() == QMessageBox.DialogCode.Accepted:
                i = events_dialog.get_chosen()
                g = self.events[i]
                ChangeEvent(g, self).exec()
            if events_dialog.result() == QMessageBox.DialogCode.Rejected:
                break

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            menu = QMenu()
            menu.addAction("Add new timeline").triggered.connect(
                self.time_pane.handle_timeline_line
            )
            menu.addAction(
                "Delete timeline (not yet fully implemented)"
            ).triggered.connect(self.on_remove)
            menu.addAction("Edit timeline label").triggered.connect(
                self.edit_label
            )
            menu.addAction("Edit events").triggered.connect(self.edit_events)
            menu.exec(event.screenPos())
        else:
            super().mousePressEvent(event)
        return


class TimelineLabel(QGraphicsRectItem):
    FIXED_HEIGHT = 20

    def __init__(self, text: str, parent: Timeline = None):
        super().__init__(parent)
        self.text = text
        rect = self.parentItem().rect()
        rect.setHeight(self.FIXED_HEIGHT)
        self.setRect(rect)
        self.parent = parent

    def paint(self, painter, option, widget=...):
        # Draw the rectangle
        self._draw_rect(painter)

        # Draw the text
        self._draw_text(painter)

    def _draw_rect(self, painter):
        """Draw the timeline label rectangle"""
        # Set Pen and Brush for rectangle
        if self.parent.select:
            color = QColor(40, 40, 40)
        else:
            color = QColor(200, 200, 200)
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawRect(self.rect())

    def _draw_text(self, painter):
        """Draw the timeline label text"""
        if self.parent.select:
            color = QColor(200, 200, 200)
        else:
            color = QColor(150, 150, 150)
        painter.setPen(color)
        painter.setBrush(color)

        font = painter.font()
        fm = QFontMetrics(font)

        text_width = fm.boundingRect(self.text).width()
        text_height = fm.boundingRect(self.text).height()
        # Get timeline polygon based on the viewport
        timeline_line_in_viewport_pos = (
            self.parentItem().time_pane.view.mapToScene(
                self.rect().toRect()
            )
        )

        bounding_rect = timeline_line_in_viewport_pos.boundingRect()

        # Get the viewport rect
        viewport_rect = self.parentItem().time_pane.view.viewport().rect()

        # Calcul the x position for the text
        x_alignCenter = bounding_rect.x() + viewport_rect.width() / 2

        text_position = QPointF(x_alignCenter - text_width / 2, text_height - 3)

        painter.drawText(text_position, self.text)

    def set_text(self, text):
        self.text = text


class Cursor(QGraphicsItem):
    def __init__(self, parent):
        super().__init__(parent)
        if parent.time_pane:
            self.time_pane: TimePane = parent.time_pane
        self.pressed = False
        self.y = 15
        self.height = 10
        self.poly: QPolygonF = QPolygonF(
            [
                QPointF(-10, self.y),
                QPointF(10, self.y),
                QPointF(0, self.y + self.height),
            ]
        )
        self.line: QLine = QLine(0, self.y, 0, 10000)

        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setZValue(101)

    def paint(self, painter, option, widget=...):
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawLine(self.line)
        painter.drawPolygon(self.poly)

    def calculate_size(self):
        min_x: float = self.poly[0].x()
        max_x: float = self.poly[0].x()

        for i, point in enumerate(self.poly):
            if point.x() < min_x:
                min_x = point.x()
            if point.x() > max_x:
                max_x = point.x()

        return QSizeF(max_x - min_x, self.height)

    def boundingRect(self):
        size: QSizeF = self.calculate_size()
        return QRectF(-10, self.y, size.width(), size.height())

    def focusInEvent(self, event):
        self.pressed = True
        super().focusInEvent(event)
        self.update()

    def focusOutEvent(self, event):
        self.pressed = False
        super().focusOutEvent(event)
        self.update()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        pos: QPointF = event.scenePos()
        if self.pressed:
            time = int(
                pos.x()
                * self.time_pane.duration
                / self.parentItem().rect().width()
            )

            # During creation of a new annotation
            if self.time_pane and self.time_pane.currentAnnotation:
                annotation = self.time_pane.currentAnnotation
                if time != annotation.get_time_from_bounding_interval(time):
                    # Stop player at the lower or upper bound when they
                    # are passed over
                    self.setPos(self.x(), 0)
                    return

            self.time_pane.video.set_position(time)

            if pos.x() < 0:
                self.setPos(0, 0)
            elif pos.x() > self.parentItem().rect().width():
                self.setPos(self.parentItem().rect().width(), 0)
            else:
                self.setPos(pos.x(), 0)

        self.update()


class TimePaneScale(QGraphicsRectItem):

    FIXED_HEIGHT: float = 25.0

    def __init__(self, time_pane: TimePane):
        super().__init__()
        self.time_pane = time_pane
        self.time_pane.scene.addItem(self)
        self.cursor = Cursor(self)
        self.setRect(
            QRectF(0, 0, self.time_pane.scene.width(), self.FIXED_HEIGHT)
        )

    def paint(self, painter, option, widget=...):
        self._draw_rect(painter)

        if self.time_pane.duration != 0:
            self._draw_scale(painter)

    def update_rect(self):
        self.setRect(
            QRectF(0, 0, self.time_pane.scene.width(), self.FIXED_HEIGHT)
        )
        self.update()

    def _draw_rect(self, painter):
        """Draw the background rectangle of the timeline scale"""
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.lightGray)
        self.setRect(
            QRectF(0, 0, self.time_pane.scene.width(), self.FIXED_HEIGHT)
        )
        painter.drawRect(self.rect())

    def _draw_scale(self, painter):
        tl = TickLocator()
        min_gap = 0.05
        dur = self.time_pane.duration
        wid = self.time_pane.scene.width()
        font = painter.font()
        fm = QFontMetrics(font)
        loc = tl.find_locations(0, dur / 1000, wid, font, min_gap)
        # Calculate the height of the text
        font_height = painter.fontMetrics().height()
        line_height = 5
        y = self.rect().height()

        for p in loc:

            i = 1000 * (p[0] * wid / dur)

            # Calculate the position of the text
            text_width = fm.boundingRect(p[1]).width()
            text_position = QPointF(i - text_width / 2, font_height)

            # Draw the text
            painter.drawText(text_position, p[1])

            # Calculate the position of the line
            painter.drawLine(QPointF(i, y), QPointF(i, y - line_height))

    def mousePressEvent(self, event):
        return

    def mouseReleaseEvent(self, event):
        return


class Annotation(QGraphicsRectItem):
    DEFAULT_PEN_COLOR = QColor(0, 0, 0, 255)
    DEFAULT_BG_COLOR = QColor(255, 48, 48, 128)
    DEFAULT_FONT_COLOR = QColor(0, 0, 0, 255)
    PEN_WIDTH_ON_CURSOR = 3
    PEN_WIDTH_OFF_CURSOR = 1

    def __init__(
        self,
        time_pane: TimePane,
        timeline,
        startTime: int = None,
        endTime: int = None,
        lower_bound: int = None,
        upper_bound: int = None,
    ):
        """Initializes the Annotation widget"""
        super().__init__(timeline)
        self.brushColor = self.DEFAULT_BG_COLOR
        self.penColor = self.DEFAULT_PEN_COLOR
        self.penWidth = self.PEN_WIDTH_OFF_CURSOR
        self.fontColor = self.DEFAULT_FONT_COLOR
        self.event = None
        self.name = None
        self.time_pane = time_pane
        self.mfps = self.time_pane.video.mfps
        self.startTime = (
            startTime
            if startTime
            else time_pane.value - int(self.mfps / 2)
        )
        self.endTime = (
            endTime if endTime else time_pane.value + int(self.mfps / 2)
        )
        self.timeline_line: Timeline = timeline
        self.startXPosition = int(
            self.startTime
            * self.time_pane.scene.width()
            / self.time_pane.duration
        )
        self.endXPosition = int(
            self.endTime
            * self.time_pane.scene.width()
            / self.time_pane.duration
        )
        self.set_default_rect()
        self.selected = False
        self.startHandle: AnnotationHandle = None
        self.endHandle: AnnotationHandle = None

        self.setX(self.startXPosition)
        self.setY(TimelineLabel.FIXED_HEIGHT)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.comment: str = ""

    @staticmethod
    def annotationDrawCanBeInitiate(annotations, value):
        """Check if the annotation can be initiated"""
        lower_bound = upper_bound = None
        valid = True
        annotation_under_cursor = None

        # Loop through the annotations of the selected timeline
        for a in annotations:
            if a.startTime <= value <= a.endTime:
                valid = False
                annotation_under_cursor = a
                break
            if not lower_bound:
                if a.endTime < value:
                    lower_bound = a.endTime + int(a.mfps / 2)
            else:
                if a.endTime < value:
                    if lower_bound < a.endTime:
                        lower_bound = a.endTime + int(a.mfps / 2)
            if not upper_bound:
                if a.startTime > value:
                    upper_bound = a.startTime - int(a.mfps / 2)
            else:
                if a.startTime > value:
                    if upper_bound > a.startTime:
                        upper_bound = a.startTime - int(a.mfps / 2)
        return valid, lower_bound, upper_bound, annotation_under_cursor

    def set_default_rect(self):
        self.setRect(
            QRectF(
                0,
                0,
                self.endXPosition - self.startXPosition,
                Timeline.FIXED_HEIGHT - TimelineLabel.FIXED_HEIGHT,
            )
        )

    def mousePressEvent(self, event):
        return

    def mouseReleaseEvent(self, event):
        return

    def mouseDoubleClickEvent(self, event):
        if not self.time_pane.currentAnnotation:
            self.setSelected(True)
            self.calculateBounds()

    def focusOutEvent(self, event):
        self.setSelected(False)
        super().focusOutEvent(event)

    def contextMenuEvent(self, event):
        if not self.isSelected():
            super().contextMenuEvent(event)
            return
        can_merge_previous = False
        for annotation in self.timeline_line.annotations:
            if (
                annotation.endTime == self.startTime
                and self.name == annotation.name
            ):
                can_merge_previous = True
                break
        can_merge_next = False
        for annotation in self.timeline_line.annotations:
            if (
                self.endTime == annotation.startTime
                and self.name == annotation.name
            ):
                can_merge_next = True
                break
        menu = QMenu()
        menu.addAction("Delete annotation").triggered.connect(self.on_remove)
        menu.addAction("Change annotation label").triggered.connect(
            self.change_label
        )
        if can_merge_previous:
            menu.addAction("Merge with previous annotation").triggered.connect(
                self.merge_previous
            )
        if can_merge_next:
            menu.addAction("Merge with next annotation").triggered.connect(
                self.merge_next
            )
        menu.addAction("Comment annotation").triggered.connect(
            self.edit_comment
        )
        menu.exec(event.screenPos())

    def on_remove(self):
        answer = QMessageBox.question(
            self.time_pane,
            "Confirmation",
            "Do you want to remove the annotation?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.remove()

    def edit_comment(self):
        comment_dialog = AnnotationComment(self.comment)
        comment_dialog.exec()
        if comment_dialog.result() == QMessageBox.DialogCode.Accepted:
            self.comment = comment_dialog.get_text()

    def merge_previous(self):
        for annotation in self.timeline_line.annotations:
            if (
                self.startTime == annotation.endTime
                and self.name == annotation.name
            ):
                break
        self.startTime = annotation.startTime
        annotation.remove()
        self.update_rect()
        self.update()

    def merge_next(self):
        for annotation in self.timeline_line.annotations:
            if (
                self.endTime == annotation.startTime
                and self.name == annotation.name
            ):
                break
        self.endTime = annotation.endTime
        annotation.remove()
        self.update_rect()
        self.update()

    def change_label(self):
        events_dialog = ChooseEvent(
            self.timeline_line.events,
            "Select an event for the current annotation:",
        )
        events_dialog.exec()
        if events_dialog.result() == QMessageBox.DialogCode.Accepted:
            i = events_dialog.get_chosen()
            g = self.timeline_line.events[i]
            self.set_event(g)
            self.update()

    def remove(self):
        self.time_pane.scene.removeItem(self)
        if self in self.timeline_line.annotations:
            self.timeline_line.remove_annotation(self)
        if self.event:
            self.event.remove_annotation(self)
        del self

    def paint(self, painter, option, widget=...):
        # Draw the annotation rectangle
        self._draw_rect(painter)

        # Draw the name of the annotation in the annotation rectangle
        self._draw_name(painter)

        if self.isSelected():
            self.show_handles()
        else:
            self.hide_handles()

    def _draw_rect(self, painter):
        """Draw the annotation rectangle"""
        pen: QPen = QPen(self.penColor)
        pen.setWidth(self.penWidth)

        if self.isSelected():
            # Set border dotline if annotation is selected
            pen.setStyle(Qt.PenStyle.DotLine)
        painter.setPen(pen)
        painter.setBrush(self.brushColor)

        # Draw the rectangle
        painter.drawRect(self.rect())

    def _draw_name(self, painter):
        """Draws the name of the annotation"""
        if self.name:
            col = color_fg_from_bg(self.brushColor)
            painter.setPen(col)
            painter.setBrush(col)
            painter.drawText(
                self.rect(), Qt.AlignmentFlag.AlignCenter, self.name
            )

    def set_event(self, event=None):
        """Updates the event"""
        if event is None:
            self.event = None
            self.brushColor = self.DEFAULT_BG_COLOR
        else:
            self.event = event
            self.brushColor = event.color
            self.name = event.name
            self.setToolTip(self.name)
            if self.startHandle:
                self.startHandle.setBrush(event.color)
                self.endHandle.setBrush(event.color)

    def update_rect(self, new_rect: QRectF = None):
        new_rect = new_rect or self.time_pane.scene.sceneRect()
        # Calculate position to determine width
        self.startXPosition = (
            self.startTime * new_rect.width() / self.time_pane.duration
        )
        self.endXPosition = (
            self.endTime * new_rect.width() / self.time_pane.duration
        )
        self.setX(self.startXPosition)

        # Update the rectangle
        rect = self.rect()
        rect.setWidth(self.endXPosition - self.startXPosition)
        self.setRect(rect)

        if self.startHandle:
            self.startHandle.setX(self.rect().x())
            self.endHandle.setX(self.rect().width())

    def update_start_time(self, startTime: int):
        self.startTime = startTime
        self.update_rect()
        self.update()

    def update_end_time(self, endTime: int):
        """Updates the end time"""
        self.endTime = endTime
        self.update_rect()
        self.update()

    def update_selectable_flags(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.update()

    def create_handles(self):
        self.startHandle = AnnotationStartHandle(self)
        self.endHandle = AnnotationEndHandle(self)

    def ends_creation(self):
        """Ends the creation of the annotation"""
        self.update_selectable_flags()
        self.create_handles()

        # if startTime is greater than endTime then swap times
        if self.startTime > self.endTime:
            self.startTime, self.endTime = self.endTime, self.startTime
            self.update_rect()

        # Add this annotation to the annotation list of the timeline
        self.timeline_line.add_annotation(self)

        self.update()

    def show_handles(self):
        if self.startHandle:
            self.startHandle.setVisible(True)
        if self.endHandle:
            self.endHandle.setVisible(True)

    def hide_handles(self):
        if self.startHandle:
            self.startHandle.setVisible(False)
        if self.endHandle:
            self.endHandle.setVisible(False)

    def calculateBounds(self):
        _, lower_bound, upper_bound, annotation = (
            Annotation.annotationDrawCanBeInitiate(
                list(
                    filter(lambda x: x != self, self.timeline_line.annotations)
                ),
                self.startTime,
            )
        )
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_time_from_bounding_interval(self, time) -> int:
        if self.lower_bound and time < self.lower_bound:
            time = self.lower_bound
        elif self.upper_bound and time > self.upper_bound:
            time = self.upper_bound
            self.time_pane.video.mediaplayer.pause()
        return time


class AnnotationHandle(QGraphicsRectItem):
    PEN_WIDTH_ON = 3
    PEN_WIDTH_OFF = 1

    def __init__(self, annotation: Annotation, value: int, x: float):
        super().__init__(annotation)
        self.annotation = annotation
        self.value = value

        self.pen: QPen = QPen(self.annotation.penColor)
        self.pen.setWidth(self.PEN_WIDTH_OFF)
        self.setPen(self.pen)
        self.setBrush(self.annotation.brushColor)
        self.setVisible(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptDrops(True)

        width = 9
        self._height = annotation.rect().height() / 2
        self.setRect(QRectF(-4.5, 0, width, self._height))

        self.setX(x)
        self.setY(self._height / 2)

    @abstractmethod
    def change_time(self, new_time):
        self.value = new_time

    def focusInEvent(self, event):
        self.annotation.setSelected(True)
        self.annotation.time_pane.video.set_position(self.value)
        self.pen.setWidth(self.PEN_WIDTH_ON)
        self.setPen(self.pen)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.annotation.setSelected(False)
        self.pen.setWidth(self.PEN_WIDTH_OFF)
        self.setPen(self.pen)
        super().focusOutEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.setY(self._height / 2)

            # A la souris on déplace le X, il faut changer le temps
            time = int(
                event.scenePos().x()
                * self.annotation.time_pane.duration
                / self.annotation.time_pane.scene.width()
            )

            time = self.annotation.get_time_from_bounding_interval(time)

            self.annotation.time_pane.video.set_position(time)


class AnnotationStartHandle(AnnotationHandle):

    def __init__(self, annotation: Annotation):
        super().__init__(annotation, annotation.startTime, 0)

    def change_time(self, time):
        t = time - int(self.annotation.mfps / 2)
        super().change_time(t)
        self.annotation.update_start_time(t)


class AnnotationEndHandle(AnnotationHandle):
    def __init__(self, annotation: Annotation):
        super().__init__(
            annotation, annotation.endTime, annotation.rect().width()
        )

    def change_time(self, time):
        t = time + int(self.annotation.mfps / 2)
        super().change_time(t)
        self.annotation.update_end_time(t)


class Event:
    def __init__(
        self,
        id: int,
        name: str,
        color: QColor = None,
        timeline_line: Timeline = None,
    ):
        """Initializes the annotation event"""
        self.id = id
        self.name = name
        self.color = color
        self.timeline_line = timeline_line
        self.annotations = []

    def add_annotation(self, annotation: Annotation):
        annotation.name = self.name
        annotation.set_event(self)
        self.annotations.append(annotation)
        self.annotations.sort(key=lambda x: x.startTime)

    def remove_annotation(self, annotation: Annotation):
        annotation.name = None
        annotation.set_event(None)
        self.annotations.remove(annotation)


class EventDialog(QDialog):
    DEFAULT_COLOR = QColor(255, 255, 255)
    """Dialog to select or create a new annotation event"""

    def __init__(self, timeline_line: Timeline = None):
        super().__init__(timeline_line.time_pane)
        self.setWindowTitle("New annotation")

        self.color = self.DEFAULT_COLOR
        self.combo_box = QComboBox()
        self.labels = [x.name for x in timeline_line.events]
        for event in timeline_line.events:
            self.combo_box.addItem(event.name, event)
        self.combo_box.setEditable(True)

        self.label_2 = QLabel("New label")
        self.event_name_text = QLineEdit()

        self.button_color_2 = QPushButton("Color")
        self.button_color_2.clicked.connect(self.on_button_color_2_clicked)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        self.abort_button = QPushButton("Abort")
        self.abort_button.clicked.connect(self.abort)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)

        # Create layout for contents
        layout = QHBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.label_2)
        layout.addWidget(self.event_name_text)
        layout.addWidget(self.button_color_2)

        # Create layout for main buttons
        main_button_layout = QHBoxLayout()
        main_button_layout.addWidget(self.cancel_button)
        main_button_layout.addWidget(self.abort_button)
        main_button_layout.addWidget(self.save_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(main_button_layout)

        self.setLayout(main_layout)

        if timeline_line.events:
            self.state = "choose"
        else:
            self.state = "create"

        self.set_visibility()

    def accept(self):
        if self.state == "choose" and (
            self.combo_box.currentText() not in self.labels
        ):
            self.state = "create"
            self.event_name_text.setText(self.combo_box.currentText())
            self.set_visibility()
            self.event_name_text.setFocus()
        else:
            super().accept()

    def abort(self):
        confirm_box = AnnotationConfirmMessageBox(self)
        if confirm_box.result() == QMessageBox.DialogCode.Accepted:
            self.done(AnnotationDialogCode.Aborted)

    def on_button_color_2_clicked(self):
        dialog = QColorDialog(self.color, self)
        dialog.exec()
        if dialog.result() == dialog.DialogCode.Accepted:
            self.color = dialog.currentColor()

    def set_visibility(self):
        if self.state == "choose":
            self.combo_box.setVisible(True)
            self.label_2.setVisible(False)
            self.event_name_text.setVisible(False)
            self.button_color_2.setVisible(False)
        else:
            self.combo_box.setVisible(False)
            self.label_2.setVisible(True)
            self.event_name_text.setVisible(True)
            self.button_color_2.setVisible(True)
        self.save_button.setDefault(True)


class AnnotationConfirmMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(
            QMessageBox.Icon.Warning,
            "Warning",
            "Are you sure to abort the creation of this annotation ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            parent,
        )

        self.button(QMessageBox.StandardButton.Yes).clicked.connect(self.accept)
        self.button(QMessageBox.StandardButton.No).clicked.connect(self.reject)
        self.exec()


class AnnotationDialogCode(IntEnum):
    Accepted: int = QDialog.DialogCode.Accepted  # 0
    Canceled: int = QDialog.DialogCode.Rejected  # 1
    Aborted: int = 2
