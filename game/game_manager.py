from PyQt5.QtCore import QObject, pyqtSignal
from game.game_state import GameState

class GameManager(QObject):
    """Основной менеджер игры"""

    # Сигналы
    location_changed = pyqtSignal(str)  # Изменение локации
    story_updated = pyqtSignal(list)    # Обновление текста истории
    choices_updated = pyqtSignal(list)  # Обновление выборов
    puzzle_started = pyqtSignal(dict)   # Начало головоломки
    game_ended = pyqtSignal(bool)       # Окончание игры (True = победа)

    def __init__(self):
        super().__init__()
        self.game_state = GameState()
        self.current_location = None

    def start_new_game(self):
        """Начать новую игру"""
        self.game_state.reset()
        self.change_location("entrance_hall")

    def change_location(self, location_name):
        """Изменить локацию"""
        self.current_location = location_name
        self.game_state.current_location = location_name
        self.location_changed.emit(location_name)

        # Загружаем контент локации
        self.load_location_content(location_name)

    def load_location_content(self, location_name):
        """Загрузить контент локации"""
        from data.story_text import StoryText

        if location_name == "entrance_hall":
            self.story_updated.emit(StoryText.ENTRANCE_HALL_DESCRIPTION)
            self.choices_updated.emit(StoryText.ENTRANCE_HALL_CHOICES)

        elif location_name == "library":
            self.story_updated.emit(StoryText.LIBRARY_DESCRIPTION)
            self.choices_updated.emit(StoryText.LIBRARY_BOOKS)

        elif location_name == "room_521":
            self.story_updated.emit(StoryText.ROOM_521_DESCRIPTION)
            # Запускаем головоломку с числовой последовательностью
            self.start_pi_puzzle()

        elif location_name == "room_605":
            self.story_updated.emit(StoryText.ROOM_605_DESCRIPTION)
            # Запускаем финальную сцену
            self.start_final_scene()

    def make_choice(self, choice_index):
        """Сделать выбор"""
        location = self.current_location

        if location == "entrance_hall":
            if choice_index == 0:  # Библиотека
                self.change_location("library")
            else:
                # Неправильный выбор
                self.story_updated.emit(["Это не то место... Попробуй еще раз."])

        elif location == "library":
            if choice_index == 5:  # Лексикология - правильный выбор
                self.game_state.add_item("library_key")
                self.story_updated.emit(StoryText.LIBRARY_BOOK_PAGE)
                self.start_math_puzzle()
            else:
                self.story_updated.emit(["Эта книга не выделяется... Попробуй другую."])

    def start_math_puzzle(self):
        """Запустить математическую головоломку"""
        puzzle_data = {
            "type": "math",
            "question": "Solve: (10+1)×(5+2)+444=?",
            "answer": "521",
            "hint": "But something is wrong there. Distortion of space and numbers."
        }
        self.puzzle_started.emit(puzzle_data)

    def start_pi_puzzle(self):
        """Запустить головоломку с числом пи"""
        puzzle_data = {
            "type": "sequence",
            "question": "Числовой ряд: 3, 1, 4, 1, 5, ...",
            "answer": "9",
            "hint": "Это знаменитая математическая константа..."
        }
        self.puzzle_started.emit(puzzle_data)

    def solve_puzzle(self, answer):
        """Решить головоломку"""
        location = self.current_location

        if location == "library":
            if answer == "521":
                self.game_state.add_item("room_521_key")
                self.story_updated.emit([
                    "Правильно! Ключ от аудитории 521 теперь у тебя.",
                    "Можешь идти в аудиторию 521."
                ])
                self.choices_updated.emit(["Идти в аудиторию 521"])
                return True

        elif location == "room_521":
            if answer == "9":
                self.story_updated.emit(StoryText.ROOM_521_CLUE)
                self.choices_updated.emit(["Идти в аудиторию 605"])
                return True

        # Неправильный ответ
        self.story_updated.emit(["Неправильно... Попробуй еще раз."])
        return False

    def start_final_scene(self):
        """Запустить финальную сцену"""
        from data.story_text import StoryText
        import threading
        import time

        def final_animation():
            time.sleep(3)
            self.story_updated.emit(StoryText.FINAL_TEXT)
            time.sleep(5)
            self.game_ended.emit(True)

        # Запускаем финальную анимацию в отдельном потоке
        thread = threading.Thread(target=final_animation)
        thread.daemon = True
        thread.start()

    def get_inventory(self):
        """Получить инвентарь"""
        return self.game_state.inventory

    def save_game(self):
        """Сохранить игру"""
        # TODO: Реализовать сохранение
        pass

    def load_game(self):
        """Загрузить игру"""
        # TODO: Реализовать загрузку
        pass
