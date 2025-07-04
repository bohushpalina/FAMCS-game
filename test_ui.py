import sys
import os

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🧪 Тестирование UI компонентов...")

# Проверка импортов
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    print("✅ PyQt5 импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта PyQt5: {e}")
    sys.exit(1)

# Проверка конфигурации
try:
    from utils.config import GameConfig
    print("✅ Конфигурация загружена")
    print(f"  Размер окна: {GameConfig.WINDOW_WIDTH}x{GameConfig.WINDOW_HEIGHT}")
    print(f"  Цвет фона: {GameConfig.BACKGROUND_COLOR}")
except ImportError as e:
    print(f"❌ Ошибка импорта конфигурации: {e}")
    sys.exit(1)

# Проверка виджетов
try:
    from ui.widgets.text_display import TextDisplay
    from ui.widgets.choice_buttons import ChoiceButtons
    print("✅ Виджеты импортированы успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта виджетов: {e}")
    sys.exit(1)

# Проверка экранов
try:
    from ui.intro_screen import IntroScreen
    from ui.game_screen import GameScreen
    from ui.main_window import MainWindow
    print("✅ Экраны импортированы успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта экранов: {e}")
    sys.exit(1)

# Проверка игрового менеджера
try:
    from game.game_manager import GameManager
    from game.game_state import GameState
    print("✅ Игровая логика импортирована успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта игровой логики: {e}")
    sys.exit(1)

# Проверка данных
try:
    from data.story_text import StoryText
    print("✅ Данные истории импортированы успешно")
    print(f"  Количество строк в intro: {len(StoryText.INTRO_TEXT)}")
except ImportError as e:
    print(f"❌ Ошибка импорта данных: {e}")
    sys.exit(1)

# Тест создания компонентов
def test_ui_components():
    """Тест создания UI компонентов"""
    print("\n🧪 Тестирование создания компонентов...")

    app = QApplication(sys.argv)

    try:
        # Тест виджетов
        print("  📝 Создание TextDisplay...")
        text_display = TextDisplay()
        print("  ✅ TextDisplay создан")

        print("  🔘 Создание ChoiceButtons...")
        choice_buttons = ChoiceButtons()
        print("  ✅ ChoiceButtons создан")

        # Тест менеджера игры
        print("  🎮 Создание GameManager...")
        game_manager = GameManager()
        print("  ✅ GameManager создан")

        # Тест экранов
        print("  🖥️ Создание IntroScreen...")
        intro_screen = IntroScreen(game_manager)
        print("  ✅ IntroScreen создан")

        print("  🎯 Создание GameScreen...")
        game_screen = GameScreen(game_manager)
        print("  ✅ GameScreen создан")

        print("  🏠 Создание MainWindow...")
        main_window = MainWindow()
        print("  ✅ MainWindow создан")

        print("\n🎉 Все компоненты созданы успешно!")

        # Показываем главное окно для визуальной проверки
        print("  📺 Показываем главное окно...")
        main_window.show()

        print("\n✅ UI блок полностью работоспособен!")
        print("   Закройте окно для завершения теста.")

        return app.exec_()

    except Exception as e:
        print(f"❌ Ошибка создания компонентов: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 ТЕСТИРОВАНИЕ UI БЛОКА UNIVERSITY QUEST")
    print("=" * 50)

    try:
        result = test_ui_components()
        print(f"\n🏁 Тест завершен с кодом: {result}")
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
