"""
Конфигурационный файл для игры
"""

class GameConfig:
    """Основные настройки игры"""

    # Размеры окна
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    MIN_WINDOW_WIDTH = 900
    MIN_WINDOW_HEIGHT = 600

    # Цвета
    BACKGROUND_COLOR = "#0a0a0a"  # Почти черный
    TEXT_COLOR = "#e0e0e0"        # Светло-серый
    ACCENT_COLOR = "#ff6b6b"      # Красный акцент
    BUTTON_COLOR = "#2a2a2a"      # Темно-серый
    BUTTON_HOVER_COLOR = "#3a3a3a"

    # Шрифты
    MAIN_FONT = "Segoe UI"
    TITLE_FONT = "Segoe Script"  # если хочешь разделить
    STORY_FONT_SIZE = 16
    TITLE_FONT_SIZE = 30
    BUTTON_FONT_SIZE = 14

    # Анимации
    TYPEWRITER_SPEED = 50  # мс между символами
    FADE_DURATION = 1000   # мс для fade in/out

    # Звуки
    ENABLE_SOUND = True
    SOUND_VOLUME = 0.7

    # Геймплей
    AUTO_SAVE = True
    SAVE_INTERVAL = 30  # секунд
