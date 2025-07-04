from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor, QPalette

from utils.config import GameConfig

class TextDisplay(QTextEdit):
    """Виджет для отображения текста истории с эффектом печатной машинки"""

    text_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.current_text_lines = []
        self.current_line_index = 0
        self.current_char_index = 0
        self.typewriter_timer = QTimer()
        self.typewriter_timer.timeout.connect(self.typewriter_tick)
        self.setup_widget()

    def setup_widget(self):
        """Настройка виджета"""
        self.setReadOnly(True)
        self.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.STORY_FONT_SIZE))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWordWrapMode(1)  # QTextOption.WordWrap

        # Стили
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: transparent;
                border: none;
                color: {GameConfig.TEXT_COLOR};
                padding: 20px;
                line-height: 1.8;
                selection-background-color: {GameConfig.ACCENT_COLOR};
            }}
        """)

    def show_text(self, text_lines, use_typewriter=True):
        """Показать текст с эффектом печатной машинки"""
        self.current_text_lines = text_lines if isinstance(text_lines, list) else [text_lines]

        if use_typewriter:
            self.clear()
            self.current_line_index = 0
            self.current_char_index = 0
            self.typewriter_timer.start(GameConfig.TYPEWRITER_SPEED)
        else:
            self.clear()
            self.setText("\\n".join(self.current_text_lines))
            self.text_finished.emit()

    def typewriter_tick(self):
        """Один тик эффекта печатной машинки"""
        if self.current_line_index >= len(self.current_text_lines):
            self.typewriter_timer.stop()
            self.text_finished.emit()
            return

        current_line = self.current_text_lines[self.current_line_index]

        # Если текущая строка пустая, переходим к следующей
        if not current_line.strip():
            self.append("")
            self.current_line_index += 1
            self.current_char_index = 0
            return

        # Если дошли до конца строки
        if self.current_char_index >= len(current_line):
            self.current_line_index += 1
            self.current_char_index = 0

            # Добавляем новую строку только если это не последняя строка
            if self.current_line_index < len(self.current_text_lines):
                self.append("")
            return

        # Добавляем следующий символ
        char = current_line[self.current_char_index]
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)

        # Если это первый символ в строке, создаем новую строку
        if self.current_char_index == 0 and self.current_line_index > 0:
            cursor.insertText("\\n")
            cursor.movePosition(QTextCursor.End)

        cursor.insertText(char)
        self.current_char_index += 1

        # Прокручиваем к концу
        self.ensureCursorVisible()

    def skip_typewriter(self):
        """Пропустить эффект печатной машинки"""
        if self.typewriter_timer.isActive():
            self.typewriter_timer.stop()
            self.clear()
            self.setText("\\n".join(self.current_text_lines))
            self.text_finished.emit()

    def append_text(self, text):
        """Добавить текст в конец"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText("\\n\\n" + text)
        self.ensureCursorVisible()

    def mousePressEvent(self, event):
        """Обработка клика мыши - пропуск анимации"""
        if event.button() == Qt.LeftButton and self.typewriter_timer.isActive():
            self.skip_typewriter()
        else:
            super().mousePressEvent(event)
