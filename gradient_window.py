import math
import random
from enum import Enum

from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QMainWindow

import easing


class States(Enum):
    IDLE = 0
    DELAY = 1
    NEXT_COLOR = 2
    REPEAT = 3


class GradientWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.state = States.DELAY
        self.last_color = QColor(255, 255, 255)
        self.current_color = QColor(255, 255, 255)
        self.next_color = QColor(0, 0, 0)

        self.delta_color = Qt.gray
        self.repeat_count = 0
        self.repeated_count = 0

        self.timer = QTimer(self)

        self.colors = []
        self.delay = 0
        self.repeat_interval = 0

        self.timer.timeout.connect(self.run)

    def set_colors(self, colors):
        self.colors = colors

    def set_timers(self, delay, repeat_interval):
        self.delay = delay
        self.repeat_interval = repeat_interval

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.current_color, Qt.SolidPattern))
        painter.setPen(QPen(self.current_color))
        painter.drawRect(0, 0, self.width(), self.height())

    @staticmethod
    def get_repeat_count(c1: QColor, c2: QColor):
        delta = [c1.red() - c2.red(),
                 c1.green() - c2.green(),
                 c1.blue() - c2.blue()]
        count = int(math.sqrt(delta[0] ** 2 + delta[1] ** 2 + delta[2] ** 2))
        return count

    @staticmethod
    def mix_colors(c1: QColor, c2: QColor, k: float):
        f = easing.sine
        red = f(c1.redF(), c2.redF(), k)
        green = f(c1.greenF(), c2.greenF(), k)
        blue = f(c1.blueF(), c2.blueF(), k)
        mixed = QColor(int(red * 255),
                       int(green * 255),
                       int(blue * 255))
        return mixed

    @pyqtSlot()
    def run(self):
        if self.state == States.DELAY:
            self.current_color = random.choice(self.colors)
            self.last_color = self.current_color
            self.next_color = self.current_color
            self.repaint()
            self.timer.start(self.delay)

            self.state = States.NEXT_COLOR
        elif self.state == States.NEXT_COLOR:
            self.timer.stop()

            color = random.choice(self.colors)
            while color == self.next_color:
                color = random.choice(self.colors)

            self.current_color = self.next_color
            self.last_color = self.next_color
            self.next_color = color

            self.repeat_count = GradientWindow.get_repeat_count(self.last_color, self.next_color)
            self.timer.start(int(self.repeat_interval / self.repeat_count))

            self.state = States.REPEAT
        elif self.state == States.REPEAT:
            if self.repeated_count <= self.repeat_count:
                self.current_color = GradientWindow.mix_colors(self.last_color, self.next_color,
                                                               self.repeated_count / self.repeat_count)
                self.repaint()
                self.repeated_count += 1
            else:
                self.repeated_count = 0

                self.state = States.NEXT_COLOR

    def closeEvent(self, event):
        self.timer.stop()
        self.state = States.DELAY
        self.repeated_count = 0
        event.accept()

    def keyPressEvent(self, event):
        self.close()

    def mousePressEvent(self, event):
        self.close()
