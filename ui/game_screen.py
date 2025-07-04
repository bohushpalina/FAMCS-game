from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QLabel, QPushButton, QLineEdit, QFrame, QScrollArea,
                             QGridLayout, QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QTextCursor, QPalette

from utils.config import GameConfig
from ui.widgets.text_display import TextDisplay
from ui.widgets.choice_buttons import ChoiceButtons

class GameScreen(QWidget):
    """Основной игровой экран"""

    return_to_menu = pyqtSignal()

    def __init__(self, game_manager):
        super().__init__()
        self.game_manager = game_manager
        self.current_puzzle = None
        self.init_ui()
        self.setup_styling()
        self.connect_signals()

    def init_ui(self):
        """Инициализация интерфейса"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Верхняя панель с информацией
        top_panel = QFrame()
        top_panel.setFrameStyle(QFrame.StyledPanel)
        top_panel.setMaximumHeight(80)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 15, 20, 15)

        # Заголовок текущей локации
        self.location_label = QLabel("University Quest")
        self.location_label.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.TITLE_FONT_SIZE, QFont.Bold))
        self.location_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.location_label)

        # Кнопка меню
        self.menu_button = QPushButton("☰ Меню")
        self.menu_button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.menu_button.setMaximumWidth(100)
        self.menu_button.clicked.connect(self.show_menu_dialog)
        top_layout.addWidget(self.menu_button)

        top_panel.setLayout(top_layout)
        main_layout.addWidget(top_panel)

        # Основная область контента
        content_frame = QFrame()
        content_frame.setFrameStyle(QFrame.StyledPanel)
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Область для текста истории
        self.text_display = TextDisplay()
        content_layout.addWidget(self.text_display, 3)

        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        content_layout.addWidget(separator)

        # Область для выборов
        self.choice_buttons = ChoiceButtons()
        self.choice_buttons.choice_made.connect(self.on_choice_made)
        content_layout.addWidget(self.choice_buttons, 1)

        # Область для ввода ответов на головоломки
        self.puzzle_frame = QFrame()
        self.puzzle_frame.setFrameStyle(QFrame.StyledPanel)
        puzzle_layout = QVBoxLayout()
        puzzle_layout.setContentsMargins(20, 15, 20, 15)

        # Заголовок головоломки
        puzzle_title = QLabel("🧩 Головоломка")
        puzzle_title.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE + 2, QFont.Bold))
        puzzle_title.setAlignment(Qt.AlignCenter)
        puzzle_layout.addWidget(puzzle_title)

        # Текст головоломки
        self.puzzle_label = QLabel()
        self.puzzle_label.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.STORY_FONT_SIZE))
        self.puzzle_label.setWordWrap(True)
        self.puzzle_label.setAlignment(Qt.AlignCenter)
        puzzle_layout.addWidget(self.puzzle_label)

        # Поле ввода и кнопка
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.puzzle_input = QLineEdit()
        self.puzzle_input.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.puzzle_input.setPlaceholderText("Введите ответ...")
        self.puzzle_input.returnPressed.connect(self.submit_puzzle_answer)
        input_layout.addWidget(self.puzzle_input)

        self.submit_button = QPushButton("✓ Ответить")
        self.submit_button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.submit_button.setMaximumWidth(120)
        self.submit_button.clicked.connect(self.submit_puzzle_answer)
        input_layout.addWidget(self.submit_button)

        puzzle_layout.addLayout(input_layout)

        # Подсказка
        self.hint_label = QLabel()
        self.hint_label.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE - 2))
        self.hint_label.setWordWrap(True)
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setStyleSheet("color: #888888; font-style: italic;")
        puzzle_layout.addWidget(self.hint_label)

        self.puzzle_frame.setLayout(puzzle_layout)
        self.puzzle_frame.setVisible(False)

        content_layout.addWidget(self.puzzle_frame)

        content_frame.setLayout(content_layout)
        main_layout.addWidget(content_frame)

        self.setLayout(main_layout)

    def setup_styling(self):
        """Настройка стилей"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {GameConfig.BACKGROUND_COLOR};
                color: {GameConfig.TEXT_COLOR};
                font-family: {GameConfig.MAIN_FONT};
            }}

            QFrame {{
                background-color: {GameConfig.BUTTON_COLOR};
                border: 2px solid {GameConfig.ACCENT_COLOR};
                border-radius: 12px;
            }}

            QLabel {{
                color: {GameConfig.TEXT_COLOR};
                background-color: transparent;
                border: none;
            }}

            QPushButton {{
                background-color: {GameConfig.BUTTON_COLOR};
                color: {GameConfig.TEXT_COLOR};
                border: 2px solid {GameConfig.ACCENT_COLOR};
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                min-height: 20px;
            }}

            QPushButton:hover {{
                background-color: {GameConfig.BUTTON_HOVER_COLOR};
                border-color: {GameConfig.TEXT_COLOR};
            }}

            QPushButton:pressed {{
                background-color: {GameConfig.ACCENT_COLOR};
                color: {GameConfig.BACKGROUND_COLOR};
            }}

            QLineEdit {{
                background-color: {GameConfig.BACKGROUND_COLOR};
                color: {GameConfig.TEXT_COLOR};
                border: 2px solid {GameConfig.ACCENT_COLOR};
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }}

            QLineEdit:focus {{
                border-color: {GameConfig.TEXT_COLOR};
                background-color: {GameConfig.BUTTON_COLOR};
            }}

            QFrame[frameShape="4"] {{
                color: {GameConfig.ACCENT_COLOR};
                background-color: {GameConfig.ACCENT_COLOR};
                border: none;
                max-height: 2px;
            }}
        """)

    def connect_signals(self):
        """Подключение сигналов"""
        self.game_manager.location_changed.connect(self.on_location_changed)
        self.game_manager.story_updated.connect(self.on_story_updated)
        self.game_manager.choices_updated.connect(self.on_choices_updated)
        self.game_manager.puzzle_started.connect(self.on_puzzle_started)
        self.game_manager.game_ended.connect(self.on_game_ended)

    def start_new_game(self):
        """Начать новую игру"""
        self.game_manager.start_new_game()

    def on_location_changed(self, location_name):
        """Обработка изменения локации"""
        location_names = {
            "entrance_hall": "🏛️ Холл первого этажа",
            "library": "📚 Библиотека",
            "room_521": "🚪 Аудитория 521",
            "room_605": "🎓 Аудитория 605"
        }

        display_name = location_names.get(location_name, f"📍 {location_name}")
        self.location_label.setText(display_name)

    def on_story_updated(self, story_lines):
        """Обновление текста истории"""
        self.text_display.show_text(story_lines)

    def on_choices_updated(self, choices):
        """Обновление выборов"""
        self.choice_buttons.set_choices(choices)
        self.puzzle_frame.setVisible(False)

    def on_puzzle_started(self, puzzle_data):
        """Начало головоломки"""
        self.current_puzzle = puzzle_data
        self.puzzle_label.setText(puzzle_data["question"])

        # Показываем подсказку если есть
        if "hint" in puzzle_data:
            self.hint_label.setText(f"💡 {puzzle_data['hint']}")
        else:
            self.hint_label.setText("")

        self.puzzle_input.clear()
        self.puzzle_input.setFocus()
        self.puzzle_frame.setVisible(True)
        self.choice_buttons.hide_choices()

    def on_choice_made(self, choice_index):
        """Обработка выбора"""
        if choice_index == 0 and self.game_manager.current_location == "room_521":
            # Переход в 605 аудиторию
            self.game_manager.change_location("room_605")
        elif choice_index == 0 and self.game_manager.current_location == "library":
            # Переход в 521 аудиторию
            self.game_manager.change_location("room_521")
        else:
            self.game_manager.make_choice(choice_index)

    def submit_puzzle_answer(self):
        """Отправка ответа на головоломку"""
        if not self.current_puzzle:
            return

        answer = self.puzzle_input.text().strip()
        if not answer:
            self.show_message("Пожалуйста, введите ответ!")
            return

        if self.game_manager.solve_puzzle(answer):
            self.puzzle_frame.setVisible(False)
            self.current_puzzle = None
            self.show_message("✅ Правильно!", success=True)
        else:
            self.puzzle_input.clear()
            self.puzzle_input.setFocus()
            self.show_message("❌ Неправильно. Попробуйте еще раз!")

    def show_message(self, message, success=False):
        """Показать временное сообщение"""
        color = "#4CAF50" if success else "#F44336"

        # Создаем временную метку
        temp_label = QLabel(message)
        temp_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
        """)
        temp_label.setAlignment(Qt.AlignCenter)


        layout = self.layout()
        layout.insertWidget(1, temp_label)


        QTimer.singleShot(2000, lambda: temp_label.deleteLater())

    def on_game_ended(self, victory):
        """Обработка окончания игры"""
        if victory:
            msg = QMessageBox(self)
            msg.setWindowTitle("🎉 Поздравляем!")
            msg.setText("Вы успешно прошли University Quest!\n\nБыло ли это сном или реальностью?")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        # Небольшая задержка перед возвратом в меню
        QTimer.singleShot(1000, self.return_to_menu.emit)

    def show_menu_dialog(self):
        """Показать диалог меню"""
        msg = QMessageBox(self)
        msg.setWindowTitle("📋 Меню игры")
        msg.setText("Что вы хотите сделать?")
        msg.setIcon(QMessageBox.Question)

        menu_button = msg.addButton("🏠 Главное меню", QMessageBox.ActionRole)
        restart_button = msg.addButton("🔄 Перезапустить", QMessageBox.ActionRole)
        cancel_button = msg.addButton("❌ Отмена", QMessageBox.RejectRole)

        msg.exec_()

        if msg.clickedButton() == menu_button:
            self.return_to_menu.emit()
        elif msg.clickedButton() == restart_button:
            self.start_new_game()

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.puzzle_frame.isVisible():
                self.submit_puzzle_answer()
        elif event.key() == Qt.Key_Escape:
            self.show_menu_dialog()
        else:
            super().keyPressEvent(event)
