from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from utils.config import GameConfig

class SplashScreen(QWidget):
    start_game = pyqtSignal()
    exit_game = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_styling()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        layout.addItem(QSpacerItem(20, 250, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Отступ сверху

        title = QLabel("Увидимся в 6:05")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.TITLE_FONT_SIZE + 30, QFont.Bold))
        layout.addWidget(title)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
                    # ... кнопки как было ...
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        buttons_layout = QHBoxLayout()
        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.start_button = QPushButton("Начать игру")
        self.start_button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.start_button.setMinimumSize(180, 60)
        self.start_button.clicked.connect(self.start_game.emit)
        buttons_layout.addWidget(self.start_button)

        self.exit_button = QPushButton("Выйти")
        self.exit_button.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.BUTTON_FONT_SIZE))
        self.exit_button.setMinimumSize(180, 60)
        self.exit_button.clicked.connect(self.exit_game.emit)
        buttons_layout.addWidget(self.exit_button)

        buttons_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(buttons_layout)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def setup_styling(self):
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {GameConfig.BACKGROUND_COLOR};
            color: white;
        }}

        QLabel {{
                color: white;
                font-family: 'Segoe Script', cursive;
                font-size: 60px;
                font-weight: bold;
            }}

        QPushButton {{
                background-color: #444;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 15px 30px;
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
