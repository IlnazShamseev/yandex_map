import sys

import requests
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QFont, QPixmap
)
from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QLabel
)


def font(style="Consolas", size=14):
    """
    :param style: вид стиля
    :param size: размер текста
    :return: Стиль
    """
    return QFont(style, size)


alignmentCenter = QtCore.Qt.AlignmentFlag.AlignCenter
alignmentLeft = QtCore.Qt.AlignmentFlag.AlignLeft


class MainWindow(QWidget):
    """
    Класс для отображения карты
    """

    def __init__(self):
        ## Проводим инициализацию
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Метод для создания интерфейса
        """

        self.setWindowTitle("Maps")
        self.setFixedSize(500, 500)

        ## Добавляем стиля
        self.setStyleSheet(""" background:rgb(208,208,208); border-radius: 50px; """)

        ## Основные данные для работы с картой
        self.x = 52.318529
        self.y = 54.885912
        self.zoom = 19

        ## Сама карта
        self.map = QLabel(self)
        self.map.move(25, 25)
        self.map.resize(450, 450)
        self.map.setVisible(True)

        self.update_map()

    def create_map(self):
        """
        Создает карту
        Ничего не возвращает
        """

        # https://yandex.ru/maps-api/docs/static-api/request.html
        # документация тут

        server_address = "https://static-maps.yandex.ru/v1"

        params = {
            # Ключ. Его не надо трогать
            "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",

            # Долгота и широта центра карты в градусах
            "ll": f"{self.x},{self.y}",

            # Уровень масштабирования карты (0-21)
            "z": self.zoom,

            # Размеры. Его не надо трогать
            "size": "450,450",

            # Тип карты
            "maptype": "map",
        }

        response = requests.get(
            server_address,
            params=params
        )

        ## Проверка на соединения с сервером
        if not response:
            print("Ошибка выполнения запроса:")
            print(server_address, params)
            print(f"Http статус: {response.status_code} ( {response.reason} )")
            sys.exit(1)

        ## Запишем полученное изображение в файл.
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

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
        self.create_map()
        self.display_map()



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
