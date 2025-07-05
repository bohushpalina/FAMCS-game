import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from utils.config import GameConfig

def main():
    """Главная функция запуска игры"""
    app = QApplication(sys.argv)

    # Настройка приложения
    app.setApplicationName("Увидимся в 6:05")
    app.setApplicationVersion("1.0")

    # Загрузка шрифтов
    setup_fonts()

    # Создание главного окна
    main_window = MainWindow()
    main_window.setWindowTitle("Увидимся в 6:05")
    main_window.showMaximized()




    # Запуск приложения
    sys.exit(app.exec_())

def setup_fonts():
    """Настройка шрифтов для игры"""
    # Здесь можно добавить кастомные шрифты
    pass

if __name__ == "__main__":
    main()
