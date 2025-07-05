from PyQt5.QtCore import QObject, pyqtSignal
from datetime import datetime

class GameState(QObject):
    """Класс для хранения состояния игры"""

    # Сигналы
    stats_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        """Сброс состояния игры"""
        self.current_location = None
        self.visited_locations = set()
        self.solved_puzzles = set()
        self.game_flags = {}
        self.items = set()  # 👈 добавили
        self.start_time = datetime.now()
        self.stats = {
            'puzzles_solved': 0,
            'wrong_answers': 0,
            'locations_visited': 0,
            'items_collected': 0
        }

    def add_item(self, item_name):
        if item_name not in self.items:
            self.items.add(item_name)
            self.stats['items_collected'] += 1
            self.stats_changed.emit(self.stats)

    def has_item(self, item_name):
        return item_name in self.items


    def visit_location(self, location_name):
        """Отметить локацию как посещенную"""
        if location_name not in self.visited_locations:
            self.visited_locations.add(location_name)
            self.stats['locations_visited'] += 1
            self.stats_changed.emit(self.stats)

    def solve_puzzle(self, puzzle_name):
        """Отметить головоломку как решенную"""
        if puzzle_name not in self.solved_puzzles:
            self.solved_puzzles.add(puzzle_name)
            self.stats['puzzles_solved'] += 1
            self.stats_changed.emit(self.stats)

    def set_flag(self, flag_name, value):
        """Установить флаг игры"""
        self.game_flags[flag_name] = value

    def get_flag(self, flag_name, default=False):
        """Получить значение флага"""
        return self.game_flags.get(flag_name, default)

    def increment_wrong_answers(self):
        """Увеличить счетчик неправильных ответов"""
        self.stats['wrong_answers'] += 1
        self.stats_changed.emit(self.stats)

    def get_play_time(self):
        """Получить время игры"""
        return datetime.now() - self.start_time

    def to_dict(self):
        """Преобразовать в словарь для сохранения"""
        return {
            'current_location': self.current_location,
            'visited_locations': list(self.visited_locations),
            'solved_puzzles': list(self.solved_puzzles),
            'game_flags': self.game_flags,
            'stats': self.stats,
            'start_time': self.start_time.isoformat()
        }

    def from_dict(self, data):
        """Загрузить из словаря"""
        self.current_location = data.get('current_location')
        self.visited_locations = set(data.get('visited_locations', []))
        self.solved_puzzles = set(data.get('solved_puzzles', []))
        self.game_flags = data.get('game_flags', {})
        self.stats = data.get('stats', {})
        self.start_time = datetime.fromisoformat(data.get('start_time', datetime.now().isoformat()))
