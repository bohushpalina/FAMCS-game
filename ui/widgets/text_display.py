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
            self.append("")
            self.current_line_index += 1
            self.current_char_index = 0
            return  # Важно: выходим, чтобы не вставлять символ дальше

        # Если дошли до конца строки
        if self.current_char_index >= len(current_line):
            self.current_line_index += 1
            self.current_char_index = 0

            # Добавляем новую строку только если это не последняя строка
            if self.current_line_index < len(self.current_text_lines):
                self.append("")
            return  # Важно: выходим, чтобы не вставлять символ дальше

        # Добавляем следующий символ
        char = current_line[self.current_char_index]
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)

        # Если это первый символ в строке, создаем новую строку
        if self.current_char_index == 0 and self.current_line_index > 0:
            cursor.insertText("\n")
            cursor.movePosition(QTextCursor.End)

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
        self.append("")
        self.append(text)
        self.ensureCursorVisible()



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.typewriter_timer.isActive():
            self.skip_typewriter()
        else:
            super().mousePressEvent(event)

    def insert_all_text(self):
        self.clear()
        cursor = self.textCursor()
        for i, line in enumerate(self.current_text_lines):
            if i > 0:
                cursor.insertBlock()  # создаёт новый блок, но без лишнего форматирования
            cursor.insertText(line)
        self.setTextCursor(cursor)

