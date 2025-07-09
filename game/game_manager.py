from PyQt5.QtCore import QObject, pyqtSignal
from game.game_state import GameState
from data.story_text import StoryText
from PyQt5.QtCore import QTimer
from utils.config import GameConfig
from utils.sound_manager import SoundManager


class GameManager(QObject):
    """Основной менеджер игры"""

    # Сигналы
    location_changed = pyqtSignal(str)  # Изменение локации
    story_updated = pyqtSignal(object)  # Было list — стало object
    choices_updated = pyqtSignal(object)  # Обновление выборов
    puzzle_started = pyqtSignal(dict)   # Начало головоломки
    game_ended = pyqtSignal(bool)       # Окончание игры (True = победа)


    def __init__(self):
        super().__init__()
        self.game_state = GameState()
        self.sound_manager = SoundManager()
        self.sound_manager.load_sounds()
        self.current_location = None
        self.room_605_click_count = 0
        self.room_605_new_action_shown = False
        self.room_605_wake_up_ready = False
        self.game_over = False
        self.room_605_final_action_shown = False  # <--- Добавь сюда


    def start_new_game(self):
        """Начать новую игру"""
        self.game_over = False
        self.game_state.reset()
        self.reset_room_605_state()
        self.sound_manager.play_background_music()
        self.change_location("entrance_hall")

    def change_location(self, location_name):
        """Изменить локацию"""
        if self.game_over:
            print(f"Попытка сменить локацию на {location_name} после завершения игры — игнорируем")
            return  # Не меняем локацию после окончания игры
        self.current_location = location_name
        self.game_state.current_location = location_name
        self.location_changed.emit(location_name)

        # Загружаем контент локации
        self.load_location_content(location_name)

    def load_location_content(self, location_name):
        """Загрузить контент локации"""
        from data.story_text import StoryText

        if self.game_over:
            print(f"Игра завершена, не загружаем локацию {location_name}")  # debug
            return  # Не загружаем больше никакие сцены после финала

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
            self.choices_updated.emit({
                    "items": [StoryText.ROOM_605_FIRST_ACTION],
                    "numbered": False
                })





    def make_choice(self, choice_index):
        """Обработка выбора игрока"""
        location = self.current_location

        """Обработка выбора игрока"""
        if self.game_over:
            return  # Блокируем действия после завершения игры

            # Обработка выбора в холле
        if location == "entrance_hall":
            if 0 <= choice_index < len(StoryText.ENTRANCE_HALL_CHOICES):
                response = StoryText.ENTRANCE_HALL_CHOICE_RESPONSES.get(choice_index, "Это не то место... Попробуй ещё раз.")
                if choice_index == 0:  # Библиотека
                    self.story_updated.emit([response])
                    self.change_location("library")
                else:
                    self.story_updated.emit([response])
                    self.game_screen.show_message("Неправильно. Попробуйте ещё раз!")
                    def reset_entrance_hall():
                        self.story_updated.emit((StoryText.ENTRANCE_HALL_DESCRIPTION, True))
                        self.choices_updated.emit(StoryText.ENTRANCE_HALL_CHOICES)

                    QTimer.singleShot(7000, reset_entrance_hall)

        elif location == "library":
            if 0 <= choice_index < len(StoryText.LIBRARY_BOOKS):
                response = StoryText.LIBRARY_BOOK_RESPONSES.get(choice_index, "Ничего особенного...")

                if choice_index == 5:  # Лексикология — правильный выбор
                    self.story_updated.emit([response] + StoryText.LIBRARY_BOOK_PAGE)
                    self.game_state.add_item("library_key")
                    self.start_math_puzzle()
                else:
                    self.game_screen.show_message("Неправильно. Попробуйте ещё раз!")
                    self.story_updated.emit([response])
                    self.choices_updated.emit(StoryText.LIBRARY_BOOKS)

        elif location == "library_after_puzzle":
            if 0 <= choice_index < len(StoryText.AFTER_LIBRARY_CHOICES):
                choice = StoryText.AFTER_LIBRARY_CHOICES[choice_index]


                if choice == "Аудитория 521":
                    self.sound_manager.play_sound_effect("door_opening")
                    self.story_updated.emit([StoryText.AFTER_LIBRARY_RESPONSES[choice]])
                    self.change_location("room_521")
                    self.story_updated.emit(StoryText.ROOM_521_DESCRIPTION)
                    self.start_pi_puzzle()
                else:
                    # Показываем реакцию на неправильный выбор
                    self.story_updated.emit([StoryText.AFTER_LIBRARY_RESPONSES[choice]])
                    self.game_screen.show_message("Неправильно. Попробуйте ещё раз!")


                    # Через 7 секунд возвращаем выбор и исходный текст
                    def reset_after_library():
                        # Вернуть вопрос "Куда отправиться?" + выборы
                        self.story_updated.emit((StoryText.LIBRARY_KEY_FOUND, True))
                        self.choices_updated.emit(StoryText.AFTER_LIBRARY_CHOICES)

                    QTimer.singleShot(8000, reset_after_library)

        elif location == "room_521":
            if 0 <= choice_index < len(StoryText.ROOM_521_CHOICES):
                choice = StoryText.ROOM_521_CHOICES[choice_index]
                response = StoryText.ROOM_521_CHOICES_RESPONSES.get(choice, "Это не тот путь. Стоит попробовать ещё раз.")
                self.story_updated.emit([response])
            if choice == "Аудитория 605":
                self.change_location("room_605")
            else:
                self.game_screen.show_message("Неправильно. Попробуйте ещё раз!")

                def reset_room_521():
                    self.story_updated.emit((StoryText.ROOM_521_CLUE, True))
                    self.choices_updated.emit(StoryText.ROOM_521_CHOICES)

                QTimer.singleShot(7000, reset_room_521)

        elif location == "room_605":
            if self.room_605_final_action_shown:
                current_actions = [StoryText.ROOM_605_FINAL_ACTION]
            elif self.room_605_wake_up_ready:
                    current_actions = [StoryText.ROOM_605_WAKE_UP]
            elif self.room_605_new_action_shown:
                current_actions = [StoryText.ROOM_605_SECOND_ACTION]
            else:
                current_actions = [StoryText.ROOM_605_FIRST_ACTION]

            if 0 <= choice_index < len(current_actions):
                choice = current_actions[choice_index]
            else:
                return  # Неверный индекс — выходим

            # Кнопка 1 — Взглянуть в окно
            if choice == StoryText.ROOM_605_FIRST_ACTION:
                self.room_605_new_action_shown = True
                self.choices_updated.emit({
                    "items": [StoryText.ROOM_605_SECOND_ACTION],
                    "numbered": False
                })
                self.story_updated.emit(StoryText.ROOM_605_WINDOW_DESCRIPTION)

            # Кнопка 2 — Осмотреть аудиторию
            elif choice == StoryText.ROOM_605_SECOND_ACTION and not self.room_605_wake_up_ready:
                self.room_605_wake_up_ready = True
                self.choices_updated.emit({
                    "items": [StoryText.ROOM_605_WAKE_UP],
                    "numbered": False
                })
                self.story_updated.emit(StoryText.ROOM_605_INSPECT_TEXT)

            # Кнопка 3 — Проснуться
            elif choice == StoryText.ROOM_605_WAKE_UP:
                self.room_605_final_action_shown = True
                self.choices_updated.emit({
                    "items": [StoryText.ROOM_605_FINAL_ACTION],
                    "numbered": False
                })
                self.sound_manager.play_sound_effect("alarm_clock")
                QTimer.singleShot(1400, lambda: self.sound_manager.play_sound_effect("alarm_clock"))

                self.location_changed.emit("На часах — 6:05")
                self.story_updated.emit(StoryText.ROOM_605_WAKE_UP_TEXT)

            # Кнопка 4 — Завершить
            elif choice == StoryText.ROOM_605_FINAL_ACTION:
                self.choices_updated.emit([])
                self.sound_manager.play_credits_music()  # Запускаем музыку для титров
                # Передаем флаг is_credits=True в третьем параметре
                self.story_updated.emit((StoryText.CREDITS, False, True))
                self.game_over = True
                self.game_ended.emit(True)

    def reset_room_605_state(self):
        self.room_605_click_count = 0
        self.room_605_new_action_shown = False
        self.room_605_wake_up_ready = False
        self.room_605_final_action_shown = False





    def start_math_puzzle(self):
        """Запустить математическую головоломку"""
        puzzle_data = {
            "type": "math",
            "question": "Solve: (10+1)×(5+2)+444=?",
            "answer": "521",
        }
        self.puzzle_started.emit(puzzle_data)

    def start_pi_puzzle(self):
        """Запустить головоломку с числом пи"""
        puzzle_data = {
            "type": "sequence",
            "question": "Числовой ряд: 3, 1, 4, 1, 5, ...",
            "answer": "9",
        }
        self.puzzle_started.emit(puzzle_data)

    def solve_puzzle(self, answer):
        """Решить головоломку"""
        location = self.current_location

        if location == "library":
            if answer == "521":
                self.game_state.add_item("room_521_key")
                self.sound_manager.play_sound_effect("key_splash")
                self.story_updated.emit(StoryText.LIBRARY_KEY_FOUND + ["Куда отправиться?"])
                # Показываем варианты выбора аудиторий
                self.choices_updated.emit(StoryText.AFTER_LIBRARY_CHOICES)
                # Меняем локацию, чтобы обработка выбора после библиотеки была корректной
                self.current_location = "library_after_puzzle"
                return True


        elif location == "room_521":
            if answer == "9":
                self.story_updated.emit(StoryText.ROOM_521_CLUE)
                self.choices_updated.emit(StoryText.ROOM_521_CHOICES)  # Показать выборы
                return True

    def set_game_screen(self, screen):
        self.game_screen = screen



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
