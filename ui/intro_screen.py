from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QTextEdit, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QTextCursor, QPalette

from utils.config import GameConfig
from data.story_text import StoryText

class IntroScreen(QWidget):
    """Экран предыстории и главного меню"""

    start_game = pyqtSignal()

    def __init__(self, game_manager):
        super().__init__()
        self.game_manager = game_manager
        self.current_line = 0
        self.current_char = 0
        self.typewriter_timer = QTimer()
        self.typewriter_timer.timeout.connect(self.typewriter_effect)
        self.init_ui()
        self.setup_styling()
        self.intro_started = False


    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Заголовок
        title = QLabel("Пролог")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.TITLE_FONT_SIZE + 10, QFont.Bold))
        layout.addWidget(title)

        # Добавляем растягивающийся элемент
        layout.addItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Текстовая область для истории
        self.story_text = QTextEdit()
        self.story_text.setReadOnly(True)
        self.story_text.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.STORY_FONT_SIZE))
        self.story_text.setMinimumHeight(700)  # или даже больше, под размер окна
        self.story_text.setMaximumHeight(16777215)  # снять ограничение

        self.story_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.story_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.story_text)

        # Добавляем растягивающийся элемент
        layout.addItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.start_button = QPushButton("Начать игру")
        self.start_button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.start_button.setMinimumSize(150, 50)
        self.start_button.clicked.connect(self.on_start_clicked)
        self.start_button.setVisible(False)  # Скрываем до окончания анимации
        buttons_layout.addWidget(self.start_button)

        self.skip_button = QPushButton("Пропустить")
        self.skip_button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.skip_button.setMinimumSize(150, 50)
        self.skip_button.clicked.connect(self.skip_intro)
        buttons_layout.addWidget(self.skip_button)

        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def setup_styling(self):
        """Настройка стилей"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {GameConfig.BACKGROUND_COLOR};
                color: white;
            }}

            QLabel {{
                color: white;
                font-family: 'Segoe Script', cursive;
                font-size: 38px;
                font-weight: bold;
            }}

            QTextEdit {{
                background-color: transparent;
                border: none;
                color: {GameConfig.TEXT_COLOR};
                padding: 20px;
                line-height: 1.6;
                font-family: {GameConfig.MAIN_FONT};
                font-family: 'Segoe Script', cursive;
                font-size: 25px;

            }}

            QPushButton {{
                background-color: #444;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 500;
                font-family: 'Segoe UI', sans-serif;
            }}

            QPushButton:hover {{
                background-color: #666;
            }}

            QPushButton:pressed {{
                background-color: {GameConfig.ACCENT_COLOR};
            }}
        """)


    def start_typewriter(self):
        """Запуск эффекта печатной машинки"""
        self.current_line = 0
        self.current_char = 0
        self.story_text.clear()
        self.typewriter_timer.start(GameConfig.TYPEWRITER_SPEED)

    def typewriter_effect(self):
        """Эффект печатной машинки"""
        if self.current_line >= len(StoryText.INTRO_TEXT):
            self.typewriter_timer.stop()
            self.start_button.setVisible(True)
            self.skip_button.setVisible(False)  # 👈 скрываем кнопку "Пропустить"
            return


        current_text_line = StoryText.INTRO_TEXT[self.current_line]

        if self.current_char >= len(current_text_line):
            # Переходим к следующей строке
            self.current_line += 1
            self.current_char = 0

            # Добавляем новую строку
            cursor = self.story_text.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText("\n")
            return

        # Добавляем следующий символ
        char = current_text_line[self.current_char]
        cursor = self.story_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(char)

        self.current_char += 1

        # Прокручиваем вниз
        self.story_text.ensureCursorVisible()

    def skip_intro(self):
        """Пропустить интро"""
        self.typewriter_timer.stop()
        full_text = "\n".join(StoryText.INTRO_TEXT)
        self.story_text.setText(full_text)
        self.start_button.setVisible(True)
        self.skip_button.setVisible(False)  # 👈 скрываем кнопку "Пропустить"


    def on_start_clicked(self):
        """Обработка нажатия кнопки старта"""
        self.start_game.emit()

    def showEvent(self, event):
        super().showEvent(event)
        if not self.intro_started:
            self.intro_started = True
            QTimer.singleShot(500, self.start_typewriter)

