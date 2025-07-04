from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont

from utils.config import GameConfig

class ChoiceButtons(QWidget):
    """Виджет для отображения кнопок выбора"""

    choice_made = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.buttons = []
        self.setup_widget()

    def setup_widget(self):
        """Настройка виджета"""
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 10, 0, 10)
        self.layout.setSpacing(10)

        # Заголовок
        self.title_label = QLabel("Выберите действие:")
        self.title_label.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.setLayout(self.layout)

        # Стили
        self.setStyleSheet(f"""
            QLabel {{
                color: {GameConfig.ACCENT_COLOR};
                margin: 10px 0;
            }}

            QPushButton {{
                background-color: {GameConfig.BUTTON_COLOR};
                color: {GameConfig.TEXT_COLOR};
                border: 2px solid {GameConfig.ACCENT_COLOR};
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
                text-align: left;
                min-height: 40px;
            }}

            QPushButton:hover {{
                background-color: {GameConfig.BUTTON_HOVER_COLOR};
                border-color: {GameConfig.TEXT_COLOR};
                transform: translateY(-2px);
            }}

            QPushButton:pressed {{
                background-color: {GameConfig.ACCENT_COLOR};
            }}

            QPushButton:disabled {{
                background-color: #1a1a1a;
                color: #666666;
                border-color: #444444;
            }}
        """)

    def set_choices(self, choices):
        """Установить варианты выбора"""
        # Очищаем предыдущие кнопки
        self.clear_buttons()

        if not choices:
            self.hide()
            return

        self.show()

        # Создаем новые кнопки
        for i, choice in enumerate(choices):
            button = QPushButton(f"{i+1}. {choice}")
            button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
            button.clicked.connect(lambda checked, idx=i: self.on_button_clicked(idx))

            # Анимация появления
            button.setStyleSheet(button.styleSheet() + " opacity: 0;")
            self.layout.addWidget(button)
            self.buttons.append(button)

            # Запускаем анимацию с задержкой
            self.animate_button_appearance(button, i * 100)

    def clear_buttons(self):
        """Очистить все кнопки"""
        for button in self.buttons:
            button.deleteLater()
        self.buttons.clear()

    def hide_choices(self):
        """Скрыть кнопки выбора"""
        self.hide()

    def on_button_clicked(self, index):
        """Обработка нажатия кнопки"""
        # Отключаем все кнопки
        for button in self.buttons:
            button.setEnabled(False)

        # Подсвечиваем выбранную кнопку
        if index < len(self.buttons):
            selected_button = self.buttons[index]
            selected_button.setStyleSheet(
                selected_button.styleSheet() +
                f"background-color: {GameConfig.ACCENT_COLOR}; border-color: {GameConfig.TEXT_COLOR};"
            )

        # Отправляем сигнал
        self.choice_made.emit(index)

    def animate_button_appearance(self, button, delay):
        """Анимация появления кнопки"""
        # Создаем анимацию через QTimer для простоты
        from PyQt5.QtCore import QTimer

        def show_button():
            button.setStyleSheet(button.styleSheet().replace("opacity: 0;", "opacity: 1;"))

        QTimer.singleShot(delay, show_button)

    def set_enabled(self, enabled):
        """Включить/выключить все кнопки"""
        for button in self.buttons:
            button.setEnabled(enabled)

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        key = event.key()

        # Обработка цифровых клавиш
        if Qt.Key_1 <= key <= Qt.Key_9:
            choice_index = key - Qt.Key_1
            if choice_index < len(self.buttons) and self.buttons[choice_index].isEnabled():
                self.on_button_clicked(choice_index)
                return

        super().keyPressEvent(event)
