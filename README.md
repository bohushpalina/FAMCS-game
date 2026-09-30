# See You at 6:05 (Увидимся в 6:05)

An interactive narrative text quest and puzzle desktop game inspired by university life at FAMCS BSU.

---

## About the Game

**"See You at 6:05"** is a story-driven quest game built with Python and PyQt5. The player navigates through iconic university locations (Entrance Hall, Library, Lecture Halls), solves mathematical and logic puzzles, and unfolds a mysterious storyline set within the faculty wall.

### Key Features
* **Interactive Narrative Engine:** Custom choice-driven story flow with state management and event signals.
* **Logic & Math Puzzles:** Embedded mathematical sequence solvers and riddle-based doors/locks.
* **Dynamic Visual UI:** Clean, dark-themed GUI built using PyQt5 widgets with custom background rendering, typewriter text animations, and smooth transitions.
* **Audio System:** Integrated sound manager supporting looped background music, ambient track switching, typewriter audio cues, and action sound effects (`QMediaPlayer`).

---

## Game Architecture & Logic

* `main.py` — Application entry point; initializes PyQt5 application and applies global configurations.
* `ui/` — User Interface layer:
  * `main_window.py` — Window stack container (`QStackedWidget`) managing transitions between screens.
  * `splash_screen.py` & `intro_screen.py` — Title screen, prologue presentation, and typewriter story introduction.
  * `game_screen.py` — Main game viewport managing scene rendering, dynamic backgrounds, choices, and puzzle input forms.
* `game/` — Core Game Logic:
  * `game_manager.py` — Handles location switching, puzzle triggers, game progression, and event signaling.
  * `game_state.py` — Tracks session progress, visited rooms, inventory items, and solved puzzles.
* `utils/` — Audio management (`sound_manager.py`) and UI styling configuration (`config.py`).

---

## Tech Stack

* **Language:** Python 3.x
* **GUI Framework:** PyQt5
* **Multimedia:** PyQt5 QtMultimedia

---

## Authors
**Palina Bohush** and **Yarmolik Anastasiya**