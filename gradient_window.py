from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QWidget


class GradientWindow(QWidget):
    def __init__(self, screen, controller):
        super().__init__()

        self.controller = controller

        self.setAttribute(Qt.WA_NativeWindow)
        self.screen = screen
        self.windowHandle().setScreen(screen)
        self.setGeometry(screen.geometry())

    def paintEvent(self, event):
        color = self.controller.get_current_color()
        painter = QPainter(self)
        painter.setBrush(QBrush(color, Qt.SolidPattern))
        painter.setPen(QPen(color))
        painter.drawRect(0, 0, self.width(), self.height())

    def keyPressEvent(self, event):
        self.controller.close_windows()

    def mousePressEvent(self, event):
        self.controller.close_windows()
