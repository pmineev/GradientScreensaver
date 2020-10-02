import json

from PyQt5.QtCore import pyqtSlot, QTime
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QColorDialog, QTableWidgetItem, QApplication, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTableWidget, QVBoxLayout, QWidget, QFileDialog, QTableWidgetSelectionRange, QTimeEdit, QTabWidget

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

        self._load_settings()

        # self._test_table()

    def _create_color_tab(self):
        self.colorWidget = QWidget()
        self.colorWidget.setAutoFillBackground(True)

        self.colorsLayout = QHBoxLayout()

        self.colorTable = QTableWidget()
        self.colorTable.setRowCount(0)
        self.colorTable.setColumnCount(1)
        self.colorTable.verticalHeader().hide()
        self.colorTable.horizontalHeader().hide()
        self.colorTable.setMaximumWidth(40)
        self.colorTable.setColumnWidth(20, 30)

        self.colorButtonsLayout = QVBoxLayout()
        self.addButton = QPushButton('Добавить')
        self.upButton = QPushButton('Вверх')
        self.downButton = QPushButton('Вниз')
        self.deleteButton = QPushButton('Удалить')
        self.colorButtonsLayout.addWidget(self.addButton)
        self.colorButtonsLayout.addWidget(self.upButton)
        self.colorButtonsLayout.addWidget(self.downButton)
        self.colorButtonsLayout.addWidget(self.deleteButton)
        self.colorButtonsLayout.addStretch()

        self.colorsLayout.addWidget(self.colorTable)
        self.colorsLayout.addStretch()
        self.colorsLayout.addLayout(self.colorButtonsLayout)
        self.colorWidget.setLayout(self.colorsLayout)

        return self.colorWidget

    def _create_intervals_tab(self):
        self.intervalsWidget = QWidget()        
        self.intervalsWidget.setAutoFillBackground(True)

        self.intervalsLayout = QVBoxLayout()
        self.delayInput = QTimeEdit()
        self.delayInput.setDisplayFormat('hh:mm:ss')
        self.delayInput.setMinimumTime(QTime(0, 0, 1))
        self.repeatInput = QTimeEdit()
        self.repeatInput.setDisplayFormat('hh:mm:ss')
        self.repeatInput.setMinimumTime(QTime(0, 0, 1))
        self.intervalsLayout.addWidget(QLabel('Первый цвет'))
        self.intervalsLayout.addWidget(self.delayInput)
        self.intervalsLayout.addWidget(QLabel('Интервал'))
        self.intervalsLayout.addWidget(self.repeatInput)
        self.intervalsLayout.addStretch()

        self.intervalsWidget.setLayout(self.intervalsLayout)

        return self.intervalsWidget

    def _init_ui(self):
        self.central = QWidget()

        self.centralLayout = QVBoxLayout()

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self._create_color_tab(), 'Цвета')
        self.tabWidget.addTab(self._create_intervals_tab(), 'Интервалы')

        self.centralLayout.addWidget(self.tabWidget)

        self.errorLabel = QLabel()

        self.centralLayout.addWidget(self.errorLabel)

        self.settingsButtonsLayout = QHBoxLayout()
        self.saveButton = QPushButton('Сохранить')
        self.loadButton = QPushButton('Загрузить')
        self.startButton = QPushButton('Запустить')
        self.settingsButtonsLayout.addWidget(self.saveButton)
        self.settingsButtonsLayout.addWidget(self.loadButton)
        self.settingsButtonsLayout.addWidget(self.startButton)

        self.centralLayout.addLayout(self.settingsButtonsLayout)

        self.central.setLayout(self.centralLayout)

        self.setCentralWidget(self.central)

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

        settings = dict()

        items = [table.item(row, 0) for row in range(table.rowCount())]
        colors = [item.background().color() for item in items]
        rgb_colors = [color.getRgb() for color in colors]
        
        settings['colors'] = rgb_colors
        settings['delay'] = QTime(0, 0).secsTo(self.delayInput.time())
        settings['repeat_interval'] = QTime(0, 0).secsTo(self.repeatInput.time()) 

        filename = QFileDialog.getSaveFileName(directory='settings.json')[0]
        if filename:
            with open(filename, 'w') as f:
                json.dump(settings, f)

            self.errorLabel.setText(f'настройки сохранены в {filename}')

    def _load_settings(self, filename='settings.json'):
        try:
            with open(filename) as f:
                settings = json.load(f)

                table: QTableWidget = self.colorTable
                table.setRowCount(0)

                for rgb_color in settings['colors']:
                    color = QColor.fromRgb(*rgb_color)

                    item = QTableWidgetItem()
                    item.setBackground(color)

                    table.insertRow(table.rowCount())
                    table.setItem(table.rowCount() - 1, 0, item)

                self.delayInput.setTime(QTime().addSecs(settings['delay']))
                self.repeatInput.setTime(QTime().addSecs(settings['repeat_interval']))
            self.errorLabel.setText(f'настройки загружены из {filename}')

        except FileNotFoundError:
            pass
        except json.JSONDecodeError or KeyError or TypeError:
            self.errorLabel.setText(f'в {filename} ошибка')

    @pyqtSlot()
    def on_load(self):
        filename = QFileDialog.getOpenFileName()[0]
        if filename:
            self._load_settings(filename)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = SettingsWindow()
    w.show()
    sys.exit(app.exec_())
