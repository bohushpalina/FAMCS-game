from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPainter
from utils.config import GameConfig
from utils.sound_manager import SoundManager
import os

class SplashScreen(QWidget):
    start_game = pyqtSignal()
    exit_game = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.background_pixmap = None
        self.sound_manager = SoundManager()
        self.sound_manager.load_sounds()
        self.load_background_image()
        self.init_ui()
        self.setup_styling()

    def showEvent(self, event):
        """Вызывается при показе виджета"""
        super().showEvent(event)
        # Запускаем музыку заставки при показе экрана
        self.sound_manager.play_splash_music()

    def load_background_image(self):
        """Загрузка фонового изображения"""
        image_path = os.path.join("utils", "picture", "splash_screen.png")
        if os.path.exists(image_path):
            self.background_pixmap = QPixmap(image_path)

    def paintEvent(self, event):
        """Отрисовка фонового изображения"""
        if self.background_pixmap:
            painter = QPainter(self)
            # Масштабируем изображение под размер окна
            scaled_pixmap = self.background_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            # Вычисляем позицию для центрирования
            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        # Большой отступ сверху
        layout.addItem(QSpacerItem(20, 250, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Заголовок
        title = QLabel("Увидимся в 6:05")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.TITLE_FONT_SIZE + 30, QFont.Bold))
        # Добавляем тень для лучшей читаемости на фоне
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-family: 'Segoe Script', cursive;
                font-size: 60px;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
            }
        """)
        layout.addWidget(title)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.start_button = QPushButton("Начать игру")
        self.start_button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.start_button.setMinimumSize(180, 60)
        self.start_button.clicked.connect(self.on_start_game)
        buttons_layout.addWidget(self.start_button)

        self.exit_button = QPushButton("Выйти")
        self.exit_button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.exit_button.setMinimumSize(180, 60)
        self.exit_button.clicked.connect(self.on_exit_game)
        buttons_layout.addWidget(self.exit_button)

        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(buttons_layout)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def on_start_game(self):
        """Обработка нажатия кнопки 'Начать игру'"""
        # Останавливаем музыку заставки
        self.sound_manager.stop_splash_music()
        # Испускаем сигнал начала игры
        self.start_game.emit()

    def on_exit_game(self):
        """Обработка нажатия кнопки 'Выйти'"""
        # Останавливаем музыку заставки
        self.sound_manager.stop_splash_music()
        # Испускаем сигнал выхода
        self.exit_game.emit()

    def setup_styling(self):
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {GameConfig.BACKGROUND_COLOR};
            color: white;
        }}

        QPushButton {{
            background-color: rgba(68, 68, 68, 200);
            color: white;
            border: none;
            border-radius: 15px;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: 500;
            font-family: 'Segoe UI', sans-serif;
        }}

        QPushButton:hover {{
            background-color: rgba(102, 102, 102, 200);
        }}

        QPushButton:pressed {{
            background-color: {GameConfig.ACCENT_COLOR};
        }}
        """)
