import math
import random
from enum import Enum

from PyQt5.QtCore import QObject, Qt, QTimer, pyqtSlot, QDateTime
from PyQt5.QtGui import QColor

import easing
from gradient_window import GradientWindow


class States(Enum):
    IDLE = 0
    DELAY = 1
    NEXT_COLOR = 2
    REPEAT = 3


class GradientWindowController(QObject):
    def __init__(self, screens):
        super().__init__()
        self.windows = [GradientWindow(screen, self) for screen in screens]

        self.colors = []
        self.delay = self.repeat_interval = 0

        self.state = States.DELAY
        self.last_color = self.current_color = self.next_color = Qt.black
        self.repeat_count = self.repeated_count = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.run)

    def set_colors(self, colors):
        self.colors = colors

    def set_timers(self, delay, repeat_interval):
        self.delay = delay
        self.repeat_interval = repeat_interval

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

    def _another_color(self, color):
        another = random.choice(self.colors)
        while another == color:
            another = random.choice(self.colors)

        return another

    def get_current_color(self):
        return self.current_color

    @pyqtSlot()
    def run(self):
        if self.state == States.DELAY:
            self.last_color = self.current_color = self.next_color = random.choice(self.colors)
            for window in self.windows:
                window.showFullScreen()
                window.update()
            self.timer.start(1000 * self.delay)

            self.state = States.NEXT_COLOR
        elif self.state == States.NEXT_COLOR:
            self.timer.stop()

            self.last_color, self.next_color = self.next_color, self._another_color(self.next_color)
            self.current_color = self.last_color

            self.repeat_count = GradientWindowController.get_repeat_count(self.last_color, self.next_color)
            repaint_interval_msec = int(1000 * self.repeat_interval / self.repeat_count)
            self.timer.start(repaint_interval_msec)

            self.repeated_count = 0
            self.state = States.REPEAT
            print(QDateTime.currentMSecsSinceEpoch())
        elif self.state == States.REPEAT:
            if self.repeated_count <= self.repeat_count:
                self.current_color = GradientWindowController.mix_colors(self.last_color, self.next_color,
                                                                         self.repeated_count / self.repeat_count)
                for window in self.windows:
                    window.update()
                self.repeated_count += 1
            else:
                self.repeated_count = 0

                self.state = States.NEXT_COLOR

    def close_windows(self):
        self.timer.stop()
        self.state = States.DELAY
        self.repeated_count = 0

        for window in self.windows:
            window.close()
