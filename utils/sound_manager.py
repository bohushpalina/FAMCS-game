from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl, QObject, pyqtSignal
import os

class SoundManager(QObject):
    """Менеджер звуков и музыки для игры"""

    def __init__(self):
        super().__init__()

        # Основной плеер для фоновой музыки
        self.background_player = QMediaPlayer()
        self.background_playlist = QMediaPlaylist()
        self.background_player.setPlaylist(self.background_playlist)

        # Плеер для титров
        self.credits_player = QMediaPlayer()

        # Плеер для звуковых эффектов
        self.sfx_player = QMediaPlayer()

        # Плеер для эффекта печатной машинки (отдельный для зацикливания)
        self.typewriter_player = QMediaPlayer()

        # Настройка громкости
        self.background_player.setVolume(30)  # Фоновая музыка тише
        self.credits_player.setVolume(50)
        self.sfx_player.setVolume(70)
        self.typewriter_player.setVolume(40)

        # Пути к звуковым файлам
        self.sounds_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils", "music")

    def load_sounds(self):
        """Загрузка звуковых файлов"""
        # Фоновая музыка для игры (зацикленная)
        background_music = os.path.join(self.sounds_dir, "title_theme.mp3")
        if os.path.exists(background_music):
            self.background_playlist.addMedia(QMediaContent(QUrl.fromLocalFile(background_music)))
            self.background_playlist.setPlaybackMode(QMediaPlaylist.Loop)

        # Музыка для титров
        credits_music = os.path.join(self.sounds_dir, "credits.mp3")
        if os.path.exists(credits_music):
            self.credits_player.setMedia(QMediaContent(QUrl.fromLocalFile(credits_music)))

        # Звук печатной машинки для пролога
        typewriter_sound = os.path.join(self.sounds_dir, "typewriter_effect.mp3")
        if os.path.exists(typewriter_sound):
            self.typewriter_player.setMedia(QMediaContent(QUrl.fromLocalFile(typewriter_sound)))

    def play_background_music(self):
        self.credits_player.stop()
        """Запустить фоновую музыку"""
        if self.background_player.state() != QMediaPlayer.PlayingState:
            self.background_player.play()

    def stop_background_music(self):
        """Остановить фоновую музыку"""
        self.background_player.stop()

    def play_credits_music(self):
        """Запустить музыку для титров"""
        self.stop_background_music()  # Останавливаем фоновую музыку
        self.credits_player.play()

    def play_sound_effect(self, effect_name):
        """Воспроизвести звуковой эффект"""
        # Пробуем сначала .mp3, потом .wav
        for extension in ['.mp3', '.wav']:
            effect_path = os.path.join(self.sounds_dir, f"{effect_name}{extension}")
            if os.path.exists(effect_path):
                self.sfx_player.setMedia(QMediaContent(QUrl.fromLocalFile(effect_path)))
                self.sfx_player.play()
                break

    def play_typewriter_sound(self):
        self.credits_player.stop()
        """Воспроизвести звук печатной машинки"""
        if self.typewriter_player.state() != QMediaPlayer.PlayingState:
            self.typewriter_player.play()

    def stop_typewriter_sound(self):
        """Остановить звук печатной машинки"""
        self.typewriter_player.stop()
        self.credits_player.stop()


    def stop_all(self):
        """Остановить всю музыку и звуки"""
        self.background_player.stop()
        self.credits_player.stop()
        self.sfx_player.stop()
        self.typewriter_player.stop()

    def set_background_volume(self, volume):
        """Установить громкость фоновой музыки (0-100)"""
        self.background_player.setVolume(volume)

    def set_credits_volume(self, volume):
        """Установить громкость музыки титров (0-100)"""
        self.credits_player.setVolume(volume)

    def pause_all(self):
        """Поставить всю музыку на паузу"""
        self.background_player.pause()
        self.credits_player.pause()
        self.typewriter_player.pause()

    def resume_all(self):
        """Возобновить воспроизведение"""
        if self.credits_player.state() == QMediaPlayer.PausedState:
            self.credits_player.play()
        elif self.background_player.state() == QMediaPlayer.PausedState:
            self.background_player.play()
