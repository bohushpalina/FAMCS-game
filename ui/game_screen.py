from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont

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
        self.processing_answer = False
        self.game_over = False


    def init_ui(self):
        """Инициализация интерфейса"""

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Верхняя панель с названием локации и кнопкой меню
        top_panel = QFrame()
        top_panel.setFrameStyle(QFrame.StyledPanel)
        top_panel.setMaximumHeight(80)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 15, 20, 15)

        self.location_label = QLabel("Увидимся в 6:05")
        self.location_label.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.TITLE_FONT_SIZE, QFont.Bold))
        self.location_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.location_label, 1)

        self.menu_button = QPushButton("Меню")
        self.menu_button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.menu_button.setMaximumWidth(100)
        self.menu_button.clicked.connect(self.show_menu_dialog)
        top_layout.addWidget(self.menu_button)

        top_panel.setLayout(top_layout)
        main_layout.addWidget(top_panel)

        # Основной контент: текст истории, выборы и головоломки
        content_frame = QFrame()
        content_frame.setFrameStyle(QFrame.StyledPanel)
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Текст истории
        self.text_display = TextDisplay()
        content_layout.addWidget(self.text_display, 3)

        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        content_layout.addWidget(separator)

        # Выборы игрока
        self.choice_buttons = ChoiceButtons()
        self.choice_buttons.choice_made.connect(self.on_choice_made)
        content_layout.addWidget(self.choice_buttons, 1)

        # Головоломка — поле ввода с вопросом и кнопка подтверждения
        self.puzzle_frame = QFrame()
        self.puzzle_frame.setFrameStyle(QFrame.StyledPanel)
        puzzle_layout = QVBoxLayout()
        puzzle_layout.setContentsMargins(20, 15, 20, 15)


        self.puzzle_label = QLabel()
        self.puzzle_label.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.STORY_FONT_SIZE))
        self.puzzle_label.setWordWrap(True)
        self.puzzle_label.setAlignment(Qt.AlignCenter)
        puzzle_layout.addWidget(self.puzzle_label)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.puzzle_input = QLineEdit()
        self.puzzle_input.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.puzzle_input.setPlaceholderText("Введите ответ...")
        input_layout.addWidget(self.puzzle_input)

        self.submit_button = QPushButton("Ответить")
        self.submit_button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.submit_button.setMaximumWidth(120)
        self.submit_button.clicked.connect(self.submit_puzzle_answer)
        input_layout.addWidget(self.submit_button)

        puzzle_layout.addLayout(input_layout)

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
        """Применение стилей"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {GameConfig.BACKGROUND_COLOR};
                color: white;
                font-family: 'Segoe Script', cursive;
            }}
            QFrame {{
                background-color: {GameConfig.BUTTON_COLOR};
                border-radius: 15px;
                border: none;
            }}
            QLabel {{
                color: white;
                background-color: transparent;
                font-family: 'Segoe Script', cursive;
                font-weight: bold;
            }}
            QPushButton {{
                background-color: #444;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 12px 25px;
                font-size: 16px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: 600;
                transition: background-color 0.3s ease;
            }}
            QPushButton:hover {{
                background-color: #666;
                cursor: pointer;
            }}
            QPushButton:pressed {{
                background-color: {GameConfig.ACCENT_COLOR};
                color: {GameConfig.BACKGROUND_COLOR};
            }}
            QLineEdit {{
                background-color: {GameConfig.BACKGROUND_COLOR};
                color: white;
                border: 2px solid transparent;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 16px;
                font-family: 'Segoe UI', sans-serif;
                transition: border-color 0.3s ease;
            }}
            QLineEdit:focus {{
                border-color: {GameConfig.ACCENT_COLOR};
                background-color: {GameConfig.BUTTON_COLOR};
            }}
        """)

    def connect_signals(self):
        """Подключаем сигналы от game_manager к методам экрана"""
        self.game_manager.location_changed.connect(self.on_location_changed)
        self.game_manager.story_updated.connect(self.on_story_updated)
        self.game_manager.choices_updated.connect(self.on_choices_updated)
        self.game_manager.puzzle_started.connect(self.on_puzzle_started)
        self.game_manager.game_ended.connect(self.on_game_ended)

    def start_new_game(self):
        self.game_manager.start_new_game()

    # Обновление названия локации в заголовке
    def on_location_changed(self, location_name):
        location_names = {
            "entrance_hall": "Холл первого этажа",
            "library": "Библиотека",
            "room_521": "Аудитория 521",
            "room_605": "Аудитория 605",
            "---": "— — —"  # Заголовок при взгляде в окно
        }
        self.location_label.setText(location_names.get(location_name, location_name))

    # Обновление текста истории
    def on_story_updated(self, story_data):
        # Позволяет передавать флаг "без анимации"
        if isinstance(story_data, tuple):
            story_lines, instant = story_data
        else:
            story_lines = story_data
            instant = False

        self.text_display.show_text(story_lines, use_typewriter=not instant)


    # Обновление кнопок выбора
    def on_choices_updated(self, choices):
        if not choices:
            self.choice_buttons.hide()
            # Если есть надпись "Выберите действие", её тоже скрыть
            # например:
            # self.choose_label.hide()
        else:
            self.choice_buttons.show()
            self.choice_buttons.set_choices(choices)
            self.puzzle_frame.setVisible(False)



    # Начало головоломки: показываем вопрос и поле ввода
    def on_puzzle_started(self, puzzle_data):
        self.current_puzzle = puzzle_data
        self.puzzle_label.setText(puzzle_data.get("question", ""))
        self.puzzle_input.clear()
        self.puzzle_input.setFocus()
        self.puzzle_frame.setVisible(True)
        self.choice_buttons.hide_choices()
        self.puzzle_frame.setVisible(True)


        if puzzle_data.get("type") == "sequence":
            self.puzzle_input.setPlaceholderText("Введите следующий элемент последовательности...")
        else:
            self.puzzle_input.setPlaceholderText("Введите ответ...")

    # Обработка выбора игрока (кнопка)
    def on_choice_made(self, choice_index):
        # Передаем выбор в менеджер игры
        self.game_manager.make_choice(choice_index)

    # Отправка ответа на головоломку
    def submit_puzzle_answer(self):

        if self.processing_answer:
            return
        self.processing_answer = True

        if not self.current_puzzle:
            self.processing_answer = False
            return

        answer = self.puzzle_input.text().strip()
        if self.game_manager.solve_puzzle(answer):
            self.puzzle_frame.setVisible(False)
            self.current_puzzle = None
            self.show_message("Правильно!", success=True)
        else:
            self.puzzle_input.clear()
            self.puzzle_input.setFocus()
            self.show_message("Неправильно. Попробуйте еще раз!")

        self.processing_answer = False

    def show_message(self, message, success=False):
        color = "#4CAF50" if success else "#F44336"
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

        QTimer.singleShot(2000, temp_label.deleteLater)

    # Обработка окончания игры
    def on_game_ended(self, victory):
        self.game_over = True
        if victory:
            # Убираем всплывающее окно с поздравлением
            # Просто оставляем игру в состоянии конца, без перехода

            # Если нужно, можно дополнительно заблокировать выборы
            self.choice_buttons.set_choices([])  # Убрать кнопки
            self.puzzle_frame.setVisible(False)
            # Можно показать какое-то финальное сообщение или оставить титры,
            # это уже делает GameManager через story_updated.emit(StoryText.CREDITS)


    # Меню игры
    def show_menu_dialog(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Меню игры")
        msg.setText("Что вы хотите сделать?")
        msg.setIcon(QMessageBox.Question)

        menu_button = msg.addButton("Главное меню", QMessageBox.ActionRole)
        restart_button = msg.addButton("Перезапустить", QMessageBox.ActionRole)
        cancel_button = msg.addButton("Отмена", QMessageBox.RejectRole)

        msg.exec_()

        if msg.clickedButton() == menu_button:
            self.return_to_menu.emit()
        elif msg.clickedButton() == restart_button:
            self.start_new_game()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.puzzle_frame.isVisible():
                self.submit_puzzle_answer()
        elif event.key() == Qt.Key_Escape:
            self.show_menu_dialog()
        else:
            super().keyPressEvent(event)
