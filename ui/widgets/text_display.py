from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor, QPalette, QTextBlockFormat, QTextOption

from utils.config import GameConfig

class TextDisplay(QTextEdit):
    """Виджет для отображения текста истории с эффектом печатной машинки"""

    text_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.current_text_lines = []
        self.current_line_index = 0
        self.current_char_index = 0
        self.line_buffer = ""
        self.typewriter_timer = QTimer()
        self.typewriter_timer.timeout.connect(self.typewriter_tick)
        self.setup_widget()

    def setup_widget(self):
        self.setReadOnly(True)
        self.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.STORY_FONT_SIZE))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWordWrapMode(1)  # QTextOption.WordWrap

        # Установка выравнивания по центру
        self.setAlignment(Qt.AlignCenter)

        # Настройка межстрочного интервала через стили документа
        document = self.document()
        document.setDefaultStyleSheet("""
            p {
                line-height: 0.8;
                margin-top: 0px;
                margin-bottom: 0px;
                text-align: center;
            }
        """)

        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: transparent;
                border: none;
                color: {GameConfig.TEXT_COLOR};
                padding: 20px;
                selection-background-color: {GameConfig.ACCENT_COLOR};
            }}
        """)

    def show_text(self, text_lines, use_typewriter=True):
        self.clear()
        self.current_text_lines = text_lines if isinstance(text_lines, list) else [text_lines]
        self.current_line_index = 0
        self.current_char_index = 0
        self.line_buffer = ""

        if use_typewriter:
            self.typewriter_timer.start(GameConfig.TYPEWRITER_SPEED)
        else:
            self.insert_all_text()

    def typewriter_tick(self):
        """Один тик эффекта печатной машинки"""
        if self.current_line_index >= len(self.current_text_lines):
            self.typewriter_timer.stop()
            self.text_finished.emit()
            return

        current_line = self.current_text_lines[self.current_line_index]

        # Если текущая строка пустая, переходим к следующей
        if not current_line.strip():
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText("\n")
            self.current_line_index += 1
            self.current_char_index = 0
            return

        # Если дошли до конца строки
        if self.current_char_index >= len(current_line):
            self.current_line_index += 1
            self.current_char_index = 0

            # Добавляем новую строку только если это не последняя строка
            if self.current_line_index < len(self.current_text_lines):
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.End)
                cursor.insertText("\n")
            return

        cursor = self.textCursor()

        # При начале новой строки устанавливаем центрирование и проверяем на цитату
        if self.current_char_index == 0:
            cursor.movePosition(QTextCursor.End)
            if self.current_line_index > 0:
                cursor.insertText("\n")
            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignCenter)
            block_format.setLineHeight(80, QTextBlockFormat.ProportionalHeight)  # Уменьшаем межстрочный интервал
            cursor.setBlockFormat(block_format)

            # Проверяем, является ли строка цитатой
            if self._is_quote(current_line):
                from PyQt5.QtGui import QTextCharFormat
                char_format = QTextCharFormat()
                char_format.setFontItalic(True)
                cursor.setCharFormat(char_format)

        # Добавляем следующий символ
        cursor.movePosition(QTextCursor.End)
        char = current_line[self.current_char_index]
        cursor.insertText(char)
        self.current_char_index += 1

        # Прокручиваем к концу
        self.ensureCursorVisible()

    def _update_last_line(self, text):
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)
        cursor.select(cursor.BlockUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText(text)
        self.ensureCursorVisible()

    def skip_typewriter(self):
        if self.typewriter_timer.isActive():
            self.typewriter_timer.stop()
            self.insert_all_text()
            self.text_finished.emit()

    def append_text(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText("\n" + text)
        # Применяем центрирование к новому блоку
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignCenter)
        cursor.setBlockFormat(block_format)
        self.ensureCursorVisible()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.typewriter_timer.isActive():
            self.skip_typewriter()
        else:
            super().mousePressEvent(event)

    def _is_quote(self, line):
        """Определяет, является ли строка цитатой"""
        line = line.strip()
        return (
            (line.startswith("'") and line.endswith("'")) or
            (line.startswith('"') and line.endswith('"')) or
            (line.startswith("«") and line.endswith("»")) or
            (line.startswith(""") and line.endswith(""")) or
            ("'Хранилище знаний" in line) or  # Для конкретной цитаты из игры
            ("The number is the answer" in line) or
            ("Solve:" in line)
        )

    def insert_all_text(self):
        self.clear()
        cursor = self.textCursor()

        for i, line in enumerate(self.current_text_lines):
            if i > 0:
                cursor.insertBlock()

            # Применяем центрирование и уменьшенный межстрочный интервал к каждому блоку
            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignCenter)
            block_format.setLineHeight(80, QTextBlockFormat.ProportionalHeight)  # 80% от обычной высоты
            cursor.setBlockFormat(block_format)

            # Проверяем на цитату и применяем курсив
            if self._is_quote(line):
                from PyQt5.QtGui import QTextCharFormat
                char_format = QTextCharFormat()
                char_format.setFontItalic(True)
                cursor.setCharFormat(char_format)
            else:
                from PyQt5.QtGui import QTextCharFormat
                char_format = QTextCharFormat()
                char_format.setFontItalic(False)
                cursor.setCharFormat(char_format)

            cursor.insertText(line)

        self.setTextCursor(cursor)
