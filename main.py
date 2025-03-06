import os
import sys

import requests
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QFont, QPixmap, QIcon
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QLabel, QPushButton, QLineEdit
)

apikeys = {
    "geocoder": "8013b162-6b42-4997-9691-77b7074026e0",
    "static-map": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
    "search-maps": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
}


def way(files):
    """
    Возвращает полный путь до файла
    :param files: путь до файла через итерируемые объекты
    :return: путь до файла с настройкой под ОС
    """
    fullname = os.path.join("data", *files)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    return fullname


def font(style="Consolas", size=14):
    """
    :param style: вид стиля
    :param size: размер текста
    :return: Стиль
    """
    return QFont(style, size)


alignmentCenter = QtCore.Qt.AlignmentFlag.AlignCenter
alignmentLeft = QtCore.Qt.AlignmentFlag.AlignLeft
alignmentRight = QtCore.Qt.AlignmentFlag.AlignRight

stiles = {
    "MainWidget": {
        "Light": """ QWidget { background:rgb(240,240,240); border-radius: 10px; } """,
        "Dark": """QWidget { background:rgb(100,100,100); border-radius: 10px; }""",
    },
    "Widget": {
        "Light": """ QWidget { background:rgb(220,220,220); border-radius: 10px; } """,
        "Dark": """QWidget { background:rgb(70,70,70); border-radius: 10px; color: white}""",
    },
}


class MainWindow(QMainWindow):
    """
    Класс для отображения карты
    """

    def __init__(self):
        ## Проводим инициализацию
        super().__init__()

        ## Основные данные для работы с картой
        self.x = 52.318529
        self.y = 54.885912
        self.zoom = 19

        self.initUI()

    def initUI(self):
        """
        Метод для создания интерфейса
        """

        self.setWindowTitle(" ")
        self.setWindowIcon(QIcon(way(("icon.png",))))
        self.setFixedSize(800, 520)

        ## Добавляем стиля
        self.setStyleSheet(stiles["MainWidget"]["Light"])

        ## Строка для ввода
        self.search_edit = QLineEdit(self)
        self.search_edit.move(25, 25)
        self.search_edit.resize(200, 50)
        self.search_edit.setPlaceholderText("Search")
        self.search_edit.setFont(font(size=14))
        self.search_edit.setStyleSheet(stiles["Widget"]["Light"])
        self.search_edit.clearFocus()

        ## Кнопка для поиска
        self.search_btn = QPushButton(self)
        self.search_btn.move(250, 25)
        self.search_btn.resize(50, 50)
        self.search_btn.setFont(font(size=14))
        self.search_btn.setStyleSheet(stiles["Widget"]["Light"])
        self.search_btn.clicked.connect(self.search)
        self.search_btn.clearFocus()

        ## Переключатель темы
        self.theme = QPushButton(self)
        self.theme.move(25, 425)
        self.theme.resize(275, 50)
        self.theme.setText("Light")
        self.theme.setFont(font(size=18))
        self.theme.setStyleSheet(stiles["Widget"]["Light"])
        self.theme.clicked.connect(self.changing_theme)
        self.theme.clearFocus()

        ## Сама карта
        self.map = QLabel(self)
        self.map.move(325, 25)
        self.map.resize(450, 450)
        self.map.setStyleSheet(stiles["Widget"]["Light"])

        ## Статус бар для показа ошибки
        self.statusBar().resize(50, 50)
        self.statusBar()
        self.statusBar().setFont(font(size=10))
        self.statusBar().setStyleSheet(stiles["Widget"]["Light"])
        self.statusBar().clearFocus()

        self.update_map()

    def create_map(self, *arg):
        """
        Создает карту
        Ничего не возвращает
        """
        server_address = "https://static-maps.yandex.ru/v1"

        params = {
            # Ключ. Его не надо трогать
            "apikey": apikeys["static-map"],
            # Долгота и широта центра карты в градусах
            "ll": f"{self.x},{self.y}",
            # Уровень масштабирования карты (0-21)
            "z": self.zoom,
            # Размеры. Его не надо трогать
            "size": "450,450",
            # Тема запрашиваемого изображения карты. Поддерживаются светлая "light" и тёмная "dark" темы.
            "theme": self.theme.text().lower(),
            # Тип карты
            "maptype": "map",
        }

        response = None
        try:
            response = requests.get(
                server_address,
                params=params
            )
            self.statusBar().showMessage(" ")
        except:
            self.statusBar().showMessage("Ошибка")
            return

        ## Проверка на соединения с сервером
        if not response:
            print("Ошибка выполнения запроса:")
            print(server_address, params)
            print(f"Http статус: {response.status_code} ( {response.reason} )")

        ## Запишем полученное изображение в файл.
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

    def search(self):
        """
        Поиск места по адресу или организации
        """
        if not self.search_edit.text():
            return

        server_address = "https://search-maps.yandex.ru/v1"

        params = {
            # Ключ. Его не надо трогать
            "apikey": apikeys["search-maps"],
            # Текст поискового запроса.
            # Например, название географического объекта, адрес, координаты, название организации, телефон.
            "text": self.search_edit.text(),
            # Количество возвращаемых объектов
            "results": 1,
            # Предпочитаемый язык ответа
            "lang": "ru_RU"
        }

        response = None
        try:
            response = requests.get(
                # f"https://search-maps.yandex.ru/v1/?text=Bank Alfalah&type=biz&lang=en_US&apikey={apikeys["search-maps"]}"
                server_address,
                params=params
            )
            self.statusBar().showMessage(" ")
        except:
            print(1)
            self.statusBar().showMessage("Ошибка")
            return

        ## Проверка на соединения с сервером
        if not response:
            print("Ошибка выполнения запроса:")
            print(server_address, params)
            print(f"Http статус: {response.status_code} ( {response.reason} )")

        data = response.json()
        x, y = data["features"][0]["geometry"]["coordinates"]
        self.x = x
        self.y = y

        self.update_map()

    def display_map(self):
        """
        Отображает карту
        """
        ## Изображение
        pixmap = QPixmap('map.png')
        ## Его запись в карту
        self.map.setPixmap(pixmap)

    def update_map(self):
        """
        Обновляет состояние карты
        """

        self.search_edit.clearFocus()
        self.search_btn.clearFocus()
        self.theme.clearFocus()

        self.create_map()
        self.display_map()

    def keyPressEvent(self, event):
        is_update = False

        ## Проверка на запрос изменения масштаба
        if event.key() == Qt.Key.Key_PageUp:
            self.zoom = min(self.zoom + 1, 21)
            is_update = True
        elif event.key() == Qt.Key.Key_PageDown:
            self.zoom = max(self.zoom - 1, 0)
            is_update = True

        ## Проверка на запрос перемещения карты
        if event.key() == Qt.Key.Key_Up:
            self.change_coord(0, 1)
            is_update = True
        elif event.key() == Qt.Key.Key_Down:
            self.change_coord(0, -1)
            is_update = True
        elif event.key() == Qt.Key.Key_Right:
            self.change_coord(1, 0)
            is_update = True
        elif event.key() == Qt.Key.Key_Left:
            self.change_coord(-1, 0)
            is_update = True

        if is_update:
            self.update_map()

    def change_coord(self, x_delta: int, y_delta: int):
        """
        Обновляет центр карты
        :param x_delta: число из [-1:1] для оси y
        :param y_delta: число из [-1:1] для оси x
        """
        coefficients = {
            "x": lambda zoom: 0.000075 * 2 ** (21 - zoom),
            "y": lambda zoom: 0.000045 * 2 ** (21 - zoom)
        }

        ## Обновляем координаты
        self.x = max(min(self.x + coefficients["x"](self.zoom) * x_delta, 179), 0)
        self.y = max(min(self.y + coefficients["y"](self.zoom) * y_delta, 89), 0)

        self.update_map()

    def get_theme(self, reverse=False):
        """
        Возвращает цвет темы. Если reverse==True, возвращает обратный цвет темы
        :param reverse: bool
        :return: str
        """

        text = "Light"
        if reverse:
            if self.theme.text() == "Light":
                text = "Dark"
        else:
            if self.theme.text() != "Light":
                text = "Dark"
        return text

    def changing_theme(self):
        """
        Изменяем тему
        """

        theme = self.get_theme(reverse=True)
        self.theme.setText(theme)
        self.setStyleSheet(stiles["MainWidget"][theme])
        self.search_edit.setStyleSheet(stiles["Widget"][theme])
        self.search_btn.setStyleSheet(stiles["Widget"][theme])
        self.theme.setStyleSheet(stiles["Widget"][theme])
        self.statusBar().setStyleSheet(stiles["Widget"][theme])

        self.update_map()


def except_hook(cls, exception, traceback):
    """
    Это функция для проверки ошибок
    """
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.setVisible(True)
    sys.excepthook = except_hook
    sys.exit(app.exec())

"""
## - Это важно
#  - просто комментарий
"""
