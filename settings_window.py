import json

from PyQt5.QtCore import pyqtSlot, QTime
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QColorDialog, QTableWidgetItem, QApplication, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTableWidget, QVBoxLayout, QWidget, QFileDialog, QTableWidgetSelectionRange, QTimeEdit

from gradient_window import GradientWindow


class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._init_ui()

        # uic.loadUi("settings_window.ui", self)

        self.addButton.clicked.connect(self.on_add)
        self.deleteButton.clicked.connect(self.on_delete)
        self.upButton.clicked.connect(self.on_up)
        self.downButton.clicked.connect(self.on_down)
        self.startButton.clicked.connect(self.on_start)
        self.saveButton.clicked.connect(self.on_save)
        self.loadButton.clicked.connect(self.on_load)

        self.gradientWindow = GradientWindow()

        self._load_palette()

        # self._test_table()

    def _init_ui(self):
        self.topLayout = QHBoxLayout()

        self.colorTable = QTableWidget()
        self.colorTable.setRowCount(0)
        self.colorTable.setColumnCount(1)
        self.colorTable.verticalHeader().hide()
        self.colorTable.horizontalHeader().hide()
        self.colorTable.setMaximumWidth(40)
        self.colorTable.setColumnWidth(20, 30)

        self.buttonsLayout = QVBoxLayout()
        self.addButton = QPushButton('Добавить')
        self.upButton = QPushButton('Вверх')
        self.downButton = QPushButton('Вниз')
        self.deleteButton = QPushButton('Удалить')
        self.saveButton = QPushButton('Сохранить')
        self.loadButton = QPushButton('Загрузить')
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.upButton)
        self.buttonsLayout.addWidget(self.downButton)
        self.buttonsLayout.addWidget(self.deleteButton)
        self.buttonsLayout.addWidget(self.saveButton)
        self.buttonsLayout.addWidget(self.loadButton)
        self.buttonsLayout.addStretch()

        self.intervalsLayout = QVBoxLayout()
        self.delayInput = QTimeEdit()
        self.delayInput.setDisplayFormat('hh:mm:ss')
        self.delayInput.setMinimumTime(QTime(0, 0, 1))
        self.repeatInput = QTimeEdit()
        self.repeatInput.setDisplayFormat('hh:mm:ss')
        self.repeatInput.setMinimumTime(QTime(0, 0, 1))
        self.errorLabel = QLabel()
        self.startButton = QPushButton('Запустить')
        self.intervalsLayout.addWidget(QLabel('Первый цвет'))
        self.intervalsLayout.addWidget(self.delayInput)
        self.intervalsLayout.addWidget(QLabel('Интервал'))
        self.intervalsLayout.addWidget(self.repeatInput)
        self.intervalsLayout.addWidget(self.errorLabel)
        self.intervalsLayout.addWidget(self.startButton)

        self.topLayout.addWidget(self.colorTable)
        self.topLayout.addLayout(self.buttonsLayout)
        self.topLayout.addLayout(self.intervalsLayout)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.topLayout)
        self.setCentralWidget(self.centralWidget)

    def _test_table(self):
        table: QTableWidget = self.colorTable
        table.setRowCount(3)

        item = QTableWidgetItem()
        item.setBackground(QColor(254, 1, 2))
        table.setItem(0, 0, item)

        item = QTableWidgetItem()
        item.setBackground(QColor(3, 253, 4))
        table.setItem(1, 0, item)

        item = QTableWidgetItem()
        item.setBackground(QColor(5, 6, 252))
        table.setItem(2, 0, item)

        self.delayInput.setText('1000')
        self.repeatInput.setText('2000')

    @pyqtSlot()
    def on_add(self):
        color = QColorDialog.getColor()
        item = QTableWidgetItem()
        item.setBackground(color)

        table: QTableWidget = self.colorTable
        table.insertRow(table.rowCount())
        table.setItem(table.rowCount() - 1, 0, item)

    @pyqtSlot()
    def on_delete(self):
        table: QTableWidget = self.colorTable
        selected = table.selectedIndexes()
        rows = [index.row() for index in selected]
        for row in rows:
            table.removeRow(row)

    @staticmethod
    def _swap_items(table: QTableWidget, row1, col1, row2, col2):
        item1 = table.takeItem(row1, col1)
        item2 = table.takeItem(row2, col2)
        table.setItem(row1, col1, item2)
        table.setItem(row2, col2, item1)

    @pyqtSlot()
    def on_up(self):
        table: QTableWidget = self.colorTable

        selected = table.selectedIndexes()
        if selected:
            rows = [index.row() for index in selected]

            prev_row = 0
            for row in sorted(rows):
                if row > prev_row:
                    SettingsWindow._swap_items(table, row, 0, row - 1, 0)
                else:
                    prev_row += 1

            table.clearSelection()
            table.setRangeSelected(QTableWidgetSelectionRange(min(rows)-1, 0, max(rows)-1, 0), True)

    @pyqtSlot()
    def on_down(self):
        table: QTableWidget = self.colorTable

        selected = table.selectedIndexes()
        if selected:
            rows = [index.row() for index in selected]

            next_row = table.rowCount() - 1
            for row in sorted(rows, reverse=True):
                if row < next_row:
                    SettingsWindow._swap_items(table, row, 0, row + 1, 0)
                else:
                    next_row -= 1

            table.clearSelection()
            table.setRangeSelected(QTableWidgetSelectionRange(min(rows)+1, 0, max(rows)+1, 0), True)

    @pyqtSlot()
    def on_start(self):
        table: QTableWidget = self.colorTable

        items = [table.item(row, 0) for row in range(table.rowCount())]
        colors = [item.background().color() for item in items]

        if not colors:
            self.errorLabel.setText('цвета добавь')
            return

        if len(colors) < 2:
            self.errorLabel.setText('давай побольше цветов')
            return

        # delay_text = self.delayInput.text()
        # repeat_text = self.repeatInput.text()
        # if not (delay_text and repeat_text):
        #     self.errorLabel.setText('интервалы напиши')
        #     return

        # if not (delay_text and delay_text.isdigit() and repeat_text and repeat_text.isdigit()):
        #     self.errorLabel.setText('нормально интервалы напиши')
        #     return

        if self.errorLabel.text():
            self.errorLabel.setText('молодец')

        delay = QTime(0, 0).secsTo(self.delayInput.time())
        repeat_interval = QTime(0, 0).secsTo(self.repeatInput.time()) 

        self.gradientWindow.set_colors(colors)
        self.gradientWindow.set_timers(delay, repeat_interval)

        self.gradientWindow.showFullScreen()
        self.gradientWindow.run()

    @pyqtSlot()
    def on_save(self):
        table: QTableWidget = self.colorTable

        items = [table.item(row, 0) for row in range(table.rowCount())]
        colors = [item.background().color() for item in items]
        rgb_colors = [color.getRgb() for color in colors]

        filename = QFileDialog.getSaveFileName(directory='palette.json')[0]
        if filename:
            with open(filename, 'w') as f:
                json.dump(rgb_colors, f)

            self.errorLabel.setText(f'палитра сохранена в {filename}')

    def _load_palette(self, filename='palette.json'):
        try:
            with open(filename) as f:
                rgb_colors = json.load(f)

                table: QTableWidget = self.colorTable
                table.setRowCount(0)

                for rgb_color in rgb_colors:
                    color = QColor.fromRgb(*rgb_color)

                    item = QTableWidgetItem()
                    item.setBackground(color)

                    table.insertRow(table.rowCount())
                    table.setItem(table.rowCount() - 1, 0, item)
            self.errorLabel.setText(f'палитра загружена из {filename}')

        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            self.errorLabel.setText(f'в {filename} ошибка')

    @pyqtSlot()
    def on_load(self):
        filename = QFileDialog.getOpenFileName()[0]
        if filename:
            self._load_palette(filename)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = SettingsWindow()
    w.show()
    sys.exit(app.exec_())
