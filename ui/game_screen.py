from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QPixmap, QBrush, QColor
import os

from utils.config import GameConfig
from ui.widgets.text_display import TextDisplay
from ui.widgets.choice_buttons import ChoiceButtons

class GameScreen(QWidget):
    """Основной игровой экран"""

    return_to_menu = pyqtSignal()
    return_to_splash = pyqtSignal()

    def __init__(self, game_manager):
        super().__init__()
        self.game_manager = game_manager
        self.game_manager.set_game_screen(self)
        self.current_puzzle = None
        self.current_background = None
        self.background_pixmap = None
        self.init_ui()
        self.setup_styling()
        self.connect_signals()
        self.processing_answer = False
        self.game_over = False
        self.showing_credits = False  # Флаг для отслеживания титров

    def paintEvent(self, event):
        """Отрисовка фонового изображения"""
        painter = QPainter(self)

        # Сначала рисуем черный фон
        painter.fillRect(self.rect(), QBrush(QColor(26, 26, 26)))

        # Рисуем фоновое изображение, если оно загружено и мы не показываем титры
        if self.background_pixmap and not self.background_pixmap.isNull() and not self.showing_credits:
            try:
                # Масштабируем изображение под размер окна, сохраняя пропорции
                scaled_pixmap = self.background_pixmap.scaled(
                    self.size(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )

                # Центрируем изображение
                x = (self.width() - scaled_pixmap.width()) // 2
                y = (self.height() - scaled_pixmap.height()) // 2

                # Рисуем изображение более четко (увеличили прозрачность)
                painter.setOpacity(0.7)
                painter.drawPixmap(x, y, scaled_pixmap)
                painter.setOpacity(1.0)
            except Exception as e:
                print(f"Ошибка при отрисовке фона: {e}")

    def init_ui(self):
        """Инициализация интерфейса"""

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Верхняя панель с названием локации и кнопкой меню
        top_panel = QFrame()
        top_panel.setFrameStyle(QFrame.StyledPanel)
        top_panel.setMaximumHeight(80)
        top_panel.setObjectName("topPanel")
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
        content_frame.setObjectName("contentFrame")
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
        self.puzzle_frame.setObjectName("puzzleFrame")
        puzzle_layout = QVBoxLayout()
        puzzle_layout.setContentsMargins(20, 15, 20, 15)

        self.puzzle_label = QLabel()
        self.puzzle_label.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.STORY_FONT_SIZE))
        self.puzzle_label.setWordWrap(True)
        self.puzzle_label.setAlignment(Qt.AlignCenter)
        puzzle_layout.addWidget(self.puzzle_label)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(15)
        input_layout.addStretch(1)

        self.puzzle_input = QLineEdit()
        self.puzzle_input.setContextMenuPolicy(Qt.NoContextMenu)
        self.puzzle_input.setStyleSheet("color: white; weight: bold; font-size: 40px;")

        self.puzzle_input.setPlaceholderText("Введите ответ...")
        self.puzzle_input.setMaximumWidth(350)
        self.puzzle_input.setMinimumWidth(300)
        self.puzzle_input.setMinimumHeight(50)
        self.puzzle_input.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(self.puzzle_input)

        self.submit_button = QPushButton("Ответить")
        self.submit_button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.submit_button.setMaximumWidth(120)
        self.submit_button.setMinimumHeight(50)
        self.submit_button.clicked.connect(self.submit_puzzle_answer)
        input_layout.addWidget(self.submit_button)

        input_layout.addStretch(1)
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
            GameScreen {{
                background: transparent;
            }}
            QWidget {{
                color: white;
                font-family: 'Segoe Script', cursive;
            }}
            QFrame#topPanel {{
               background-color: rgba(42, 42, 42, 180);
               border-radius: 15px;
               border: none;
            }}
            QFrame#contentFrame {{
                background-color: rgba(42, 42, 42, 150);
                border-radius: 15px;
                border: none;
            }}
            QFrame#puzzleFrame {{
                background-color: rgba(42, 42, 42, 150);
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
                background-color: rgba(68, 68, 68, 180);
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
                background-color: rgba(102, 102, 102, 200);
                cursor: pointer;
            }}
            QPushButton:pressed {{
                background-color: {GameConfig.ACCENT_COLOR};
                color: {GameConfig.BACKGROUND_COLOR};
            }}
            QLineEdit {{
                background-color: rgba(26, 26, 26, 220);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 15px 20px;
                font-size: 20px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                text-align: center;
                max-width: 400px;
                min-height: 50px;
            }}
            QLineEdit:focus {{
                border-color: {GameConfig.ACCENT_COLOR};
                background-color: rgba(42, 42, 42, 250);
                border-width: 3px;
            }}
            QTextEdit {{
                background-color: transparent;
                color: white;
            }}

            /* Исправление для QMessageBox (белое меню) */
            QMessageBox {{
                background-color: #2a2a2a;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }}
            QMessageBox QLabel {{
                color: white;
                background-color: transparent;
                font-size: 14px;
            }}
            QMessageBox QPushButton {{
                background-color: #444;
                color: white;
                min-width: 100px;
                padding: 8px 20px;
                font-size: 14px;
                border-radius: 8px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: #555;
            }}
            QMessageBox QPushButton:pressed {{
                background-color: #666;
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
        self.showing_credits = False  # Сбрасываем флаг титров при новой игре
        self.game_manager.start_new_game()

    def load_background_image(self, location_name):
        """Безопасная загрузка фонового изображения"""
        try:

            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Возможные пути к папке с изображениями
            possible_paths = [
                os.path.join(script_dir, "utils", "picture"),
                os.path.join(script_dir, "..", "utils", "picture"),
                os.path.join(script_dir, "..", "..", "utils", "picture"),
                os.path.join(script_dir, "..", "..", "..", "utils", "picture"),
                os.path.join(os.path.dirname(script_dir), "utils", "picture"),
                os.path.join("utils", "picture"),
                os.path.join("picture"),
                os.path.join("assets", "images"),
                os.path.join("images")
            ]

            # Соответствие локаций и файлов
            background_files = {
                "entrance_hall": ["hall.png", "hall.jpg", "hall.jpeg"],
                "library": ["biblio.png", "biblio.jpg", "biblio.jpeg"],
                "room_521": ["521.png", "521.jpg", "521.jpeg"],
                "room_605": ["605.png", "605.jpg", "605.jpeg"],
                "dormitory": ["dormitory.png", "dormitory.jpg", "dormitory.jpeg"],
                "final_scene": ["dormitory.png", "dormitory.jpg", "dormitory.jpeg"]  # Для финальной сцены используем общежитие
            }

            if location_name not in background_files:
                print(f"Локация '{location_name}' не найдена в списке фонов")
                return False

            # Пробуем найти файл изображения
            for base_path in possible_paths:
                if not os.path.exists(base_path):
                    continue

                for filename in background_files[location_name]:
                    image_path = os.path.join(base_path, filename)
                    print(f"Проверяем путь: {image_path}")

                    if os.path.exists(image_path):
                        print(f"Найден файл: {image_path}")
                        pixmap = QPixmap(image_path)

                        if not pixmap.isNull():
                            self.background_pixmap = pixmap
                            self.current_background = location_name
                            print(f"Фон загружен успешно: {pixmap.width()}x{pixmap.height()}")
                            self.update()  # Перерисовать виджет
                            return True
                        else:
                            print(f"Не удалось загрузить изображение: {image_path}")

            print(f"Фоновое изображение для '{location_name}' не найдено")
            return False

        except Exception as e:
            print(f"Ошибка при загрузке фона: {e}")
            return False

    def set_background(self, location_name):
        """Установить фоновое изображение для локации"""
        if location_name == self.current_background:
            return  # Фон уже установлен

        success = self.load_background_image(location_name)
        if not success:
            # Если не удалось загрузить фон, используем градиент по умолчанию
            self.background_pixmap = None
            self.current_background = None
            self.update()

    # Обновление названия локации в заголовке
    def on_location_changed(self, location_name):
        location_names = {
            "entrance_hall": "Холл первого этажа",
            "library": "Библиотека",
            "room_521": "Аудитория 521",
            "room_605": "Аудитория 605",
            "dormitory": "Общежитие",
            "На часах — 6:05": "На часах — 6:05"
        }
        self.location_label.setText(location_names.get(location_name, location_name))

        # Устанавливаем фоновое изображение
        if location_name == "На часах — 6:05":
            # Для финальной сцены используем фон общежития
            self.set_background("final_scene")
        else:
            self.set_background(location_name)

    # Обновление текста истории
    def on_story_updated(self, story_data):
        if isinstance(story_data, tuple):
            if len(story_data) == 3:
                story_lines, instant, is_credits = story_data
                # Для титров устанавливаем флаг и убираем фон
                if is_credits:
                    self.showing_credits = True
                    self.background_pixmap = None  # Очищаем фоновое изображение
                    self.current_background = None
                    self.update()  # Перерисовать без фона
                else:
                    self.showing_credits = False
                self.text_display.show_text(story_lines, use_typewriter=not instant)
            else:
                story_lines, instant = story_data
                self.text_display.show_text(story_lines, use_typewriter=not instant)
        else:
            story_lines = story_data
            self.text_display.show_text(story_lines, use_typewriter=True)

    # Обновление кнопок выбора
    def on_choices_updated(self, choices):
        if not choices:
            self.choice_buttons.hide()
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
        self.choice_buttons.set_choices([])
        self.puzzle_frame.setVisible(False)

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
            self.return_to_splash.emit()
        elif msg.clickedButton() == restart_button:
            self.return_to_menu.emit()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.puzzle_frame.isVisible():
                self.submit_puzzle_answer()
        elif event.key() == Qt.Key_Escape:
            self.show_menu_dialog()
        else:
            super().keyPressEvent(event)
