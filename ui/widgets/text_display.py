from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor, QTextBlockFormat, QTextCharFormat, QColor
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
        self.setReadOnly(True)
        self.setFont(QFont(GameConfig.MAIN_FONT, GameConfig.STORY_FONT_SIZE))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWordWrapMode(1)
        self.setAlignment(Qt.AlignCenter)

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

        if use_typewriter:
            self.typewriter_timer.start(GameConfig.TYPEWRITER_SPEED)
        else:
            self.insert_all_text()

    def typewriter_tick(self):
        if self.current_line_index >= len(self.current_text_lines):
            self.typewriter_timer.stop()
            self.text_finished.emit()
            return

        current_line = self.current_text_lines[self.current_line_index]

        if not current_line.strip():
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText("\n")
            self.current_line_index += 1
            self.current_char_index = 0
            return

        if self.current_char_index == 0:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            if self.current_line_index > 0:
                cursor.insertText("\n")

            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignCenter)
            block_format.setLineHeight(130, QTextBlockFormat.ProportionalHeight)
            cursor.setBlockFormat(block_format)

            char_format = QTextCharFormat()
            if self._is_quote(current_line):
                char_format.setFontItalic(True)
            cursor.setCharFormat(char_format)

        char = current_line[self.current_char_index]
        self.textCursor().insertText(char)
        self.current_char_index += 1

        if self.current_char_index >= len(current_line):
            self.current_line_index += 1
            self.current_char_index = 0

        self.ensureCursorVisible()

    def insert_all_text(self):
        self.clear()
        cursor = self.textCursor()

        for i, line in enumerate(self.current_text_lines):
            if i > 0:
                cursor.insertText("\n")

            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignCenter)
            block_format.setLineHeight(130, QTextBlockFormat.ProportionalHeight)
            cursor.setBlockFormat(block_format)

            char_format = QTextCharFormat()
            char_format.setFontItalic(self._is_quote(line))
            char_format.setForeground(self.palette().color(self.foregroundRole()))
            cursor.setCharFormat(char_format)
            cursor.insertText(line)

        self.setTextCursor(cursor)
        self.text_finished.emit()

    def skip_typewriter(self):
        if self.typewriter_timer.isActive():
            self.typewriter_timer.stop()
            self.insert_all_text()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.typewriter_timer.isActive():
            self.skip_typewriter()
        else:
            super().mousePressEvent(event)

    def _is_quote(self, line):
        line = line.strip()
        return (
            (line.startswith("'") and line.endswith("'")) or
            (line.startswith('"') and line.endswith('"')) or
            (line.startswith("«") and line.endswith("»")) or
            (line.startswith("“") and line.endswith("”")) or
            ("'Хранилище знаний" in line) or
            ("The number is the answer" in line) or
            ("Solve:" in line)
        )
