import random
import json
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle


# =========================================================
# WINDOW
# =========================================================

Window.clearcolor = (0.035, 0.055, 0.10, 1)


# =========================================================
# COLORS
# =========================================================

BG = (0.035, 0.055, 0.10, 1)
CARD = (0.075, 0.105, 0.17, 1)
CARD2 = (0.12, 0.16, 0.23, 1)

WHITE = (0.95, 0.97, 1, 1)
GRAY = (0.58, 0.65, 0.75, 1)

BLUE = (0.22, 0.74, 0.95, 1)
GREEN = (0.13, 0.78, 0.38, 1)
RED = (0.95, 0.25, 0.30, 1)
YELLOW = (1.0, 0.78, 0.15, 1)
PURPLE = (0.60, 0.35, 0.95, 1)


# =========================================================
# ROUNDED BACKGROUND WIDGET
# =========================================================

class Card(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*CARD)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(18)]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# =========================================================
# BUTTON STYLE
# =========================================================

class GameButton(Button):

    def __init__(
        self,
        bg_color=BLUE,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = bg_color

        self.color = WHITE
        self.font_size = dp(18)
        self.bold = True

        self.size_hint_y = None
        self.height = dp(58)


# =========================================================
# HOME SCREEN
# =========================================================

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=[dp(30), dp(45)],
            spacing=dp(18)
        )

        title = Label(
            text="MATH\nCHALLENGE",
            font_size=dp(38),
            bold=True,
            color=BLUE,
            halign="center"
        )

        title.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        subtitle = Label(
            text="Test your speed. Master the math.",
            font_size=dp(17),
            color=GRAY,
            size_hint_y=None,
            height=dp(40)
        )

        layout.add_widget(title)
        layout.add_widget(subtitle)

        spacer = Widget()
        layout.add_widget(spacer)

        best_card = Card(
            orientation="vertical",
            padding=dp(15),
            size_hint_y=None,
            height=dp(90)
        )

        best_title = Label(
            text="🏆  BEST SCORE",
            font_size=dp(14),
            color=GRAY
        )

        self.best_label = Label(
            text="0",
            font_size=dp(28),
            bold=True,
            color=YELLOW
        )

        best_card.add_widget(best_title)
        best_card.add_widget(self.best_label)

        layout.add_widget(best_card)

        spacer2 = Widget()
        layout.add_widget(spacer2)

        start_button = GameButton(
            text="🎮  START GAME",
            bg_color=BLUE
        )

        start_button.bind(
            on_press=self.start_game
        )

        layout.add_widget(start_button)

        quit_button = GameButton(
            text="EXIT",
            bg_color=CARD2
        )

        quit_button.bind(
            on_press=lambda x: App.get_running_app().stop()
        )

        layout.add_widget(quit_button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.best_label.text = str(app.best_score)

    def start_game(self, instance):
        self.manager.current = "difficulty"


# =========================================================
# DIFFICULTY SCREEN
# =========================================================

class DifficultyScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=[dp(30), dp(40)],
            spacing=dp(15)
        )

        title = Label(
            text="SELECT DIFFICULTY",
            font_size=dp(30),
            bold=True,
            color=WHITE,
            size_hint_y=None,
            height=dp(60)
        )

        layout.add_widget(title)

        description = Label(
            text="Choose your challenge",
            font_size=dp(16),
            color=GRAY,
            size_hint_y=None,
            height=dp(35)
        )

        layout.add_widget(description)

        layout.add_widget(Widget())

        easy = GameButton(
            text="🟢  EASY",
            bg_color=GREEN
        )

        easy.bind(
            on_press=lambda x:
            self.start_game("Easy")
        )

        layout.add_widget(easy)

        medium = GameButton(
            text="🟡  MEDIUM",
            bg_color=YELLOW
        )

        medium.bind(
            on_press=lambda x:
            self.start_game("Medium")
        )

        layout.add_widget(medium)

        hard = GameButton(
            text="🔴  HARD",
            bg_color=RED
        )

        hard.bind(
            on_press=lambda x:
            self.start_game("Hard")
        )

        layout.add_widget(hard)

        layout.add_widget(Widget())

        back = GameButton(
            text="← BACK",
            bg_color=CARD2
        )

        back.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "home")
        )

        layout.add_widget(back)

        self.add_widget(layout)

    def start_game(self, difficulty):

        app = App.get_running_app()

        app.start_new_game(difficulty)

        self.manager.current = "game"


# =========================================================
# GAME SCREEN
# =========================================================

class GameScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.time_left = 60
        self.max_time = 60

        layout = BoxLayout(
            orientation="vertical",
            padding=[dp(18), dp(20)],
            spacing=dp(12)
        )

        # -------------------------------------------------
        # TOP BAR
        # -------------------------------------------------

        top = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(55),
            spacing=dp(8)
        )

        self.score_label = Label(
            text="⭐ 0",
            font_size=dp(18),
            bold=True,
            color=YELLOW
        )

        self.combo_label = Label(
            text="🔥 x0",
            font_size=dp(18),
            bold=True,
            color=PURPLE
        )

        self.lives_label = Label(
            text="❤️❤️❤️",
            font_size=dp(18),
            bold=True,
            color=RED
        )

        top.add_widget(self.score_label)
        top.add_widget(self.combo_label)
        top.add_widget(self.lives_label)

        layout.add_widget(top)

        # -------------------------------------------------
        # TIMER
        # -------------------------------------------------

        timer_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(65),
            spacing=dp(5)
        )

        self.timer_label = Label(
            text="⏱ 60",
            font_size=dp(18),
            bold=True,
            color=BLUE,
            size_hint_y=None,
            height=dp(30)
        )

        self.progress = ProgressBar(
            max=60,
            value=60,
            size_hint_y=None,
            height=dp(12)
        )

        timer_box.add_widget(self.timer_label)
        timer_box.add_widget(self.progress)

        layout.add_widget(timer_box)

        # -------------------------------------------------
        # DIFFICULTY
        # -------------------------------------------------

        self.level_label = Label(
            text="EASY",
            font_size=dp(14),
            bold=True,
            color=BLUE,
            size_hint_y=None,
            height=dp(30)
        )

        layout.add_widget(self.level_label)

        # -------------------------------------------------
        # QUESTION CARD
        # -------------------------------------------------

        question_card = Card(
            orientation="vertical",
            padding=dp(20),
            size_hint_y=None,
            height=dp(190)
        )

        self.question_label = Label(
            text="",
            font_size=dp(34),
            bold=True,
            color=WHITE,
            halign="center"
        )

        self.question_label.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        question_card.add_widget(
            self.question_label
        )

        layout.add_widget(question_card)

        # -------------------------------------------------
        # ANSWER INPUT
        # -------------------------------------------------

        self.answer_input = TextInput(
            hint_text="Enter your answer",
            multiline=False,
            input_filter="int",
            font_size=dp(24),
            halign="center",
            size_hint_y=None,
            height=dp(60),
            background_color=WHITE,
            foreground_color=BG,
            padding=[dp(10), dp(12)]
        )

        self.answer_input.bind(
            on_text_validate=self.submit_answer
        )

        layout.add_widget(
            self.answer_input
        )

        # -------------------------------------------------
        # MESSAGE
        # -------------------------------------------------

        self.message_label = Label(
            text="",
            font_size=dp(17),
            bold=True,
            color=WHITE,
            size_hint_y=None,
            height=dp(35)
        )

        layout.add_widget(
            self.message_label
        )

        # -------------------------------------------------
        # SUBMIT
        # -------------------------------------------------

        self.submit_button = GameButton(
            text="✓  SUBMIT ANSWER",
            bg_color=BLUE
        )

        self.submit_button.bind(
            on_press=self.submit_answer
        )

        layout.add_widget(
            self.submit_button
        )

        # -------------------------------------------------
        # QUIT
        # -------------------------------------------------

        quit_button = GameButton(
            text="QUIT GAME",
            bg_color=CARD2
        )

        quit_button.height = dp(45)
        quit_button.font_size = dp(14)

        quit_button.bind(
            on_press=self.quit_game
        )

        layout.add_widget(
            quit_button
        )

        self.add_widget(layout)

    # =====================================================
    # START GAME
    # =====================================================

    def start_game(self):

        app = App.get_running_app()

        self.time_left = 60
        self.max_time = 60

        self.level_label.text = app.difficulty.upper()

        self.update_screen()

        self.generate_question()

        self.message_label.text = ""

        if app.timer_event is not None:
            app.timer_event.cancel()

        app.timer_event = Clock.schedule_interval(
            self.update_timer,
            1
        )

    # =====================================================
    # TIMER
    # =====================================================

    def update_timer(self, dt):

        self.time_left -= 1

        self.progress.value = self.time_left

        self.timer_label.text = (
            f"⏱ {self.time_left}"
        )

        if self.time_left <= 10:
            self.timer_label.color = RED

        elif self.time_left <= 20:
            self.timer_label.color = YELLOW

        else:
            self.timer_label.color = BLUE

        if self.time_left <= 0:

            app = App.get_running_app()

            if app.timer_event:
                app.timer_event.cancel()

            self.submit_button.disabled = True
            self.answer_input.disabled = True

            self.message_label.text = "⏰ TIME'S UP!"

            Clock.schedule_once(
                lambda dt: self.end_game(),
                1
            )

    # =====================================================
    # GENERATE QUESTION
    # =====================================================

    def generate_question(self):

        app = App.get_running_app()

        difficulty = app.difficulty

        if difficulty == "Easy":

            a = random.randint(2, 8)
            x = random.randint(1, 10)
            b = random.randint(-10, 10)

            c = a * x + b

            app.correct_answer = x

            if b >= 0:
                equation = f"{a}x + {b} = {c}"
            else:
                equation = f"{a}x - {abs(b)} = {c}"

        elif difficulty == "Medium":

            a = random.randint(2, 8)
            d = random.randint(1, 7)

            while a == d:
                d = random.randint(1, 7)

            x = random.randint(-8, 10)
            b = random.randint(-10, 10)

            e = (a - d) * x + b

            app.correct_answer = x

            if b >= 0:
                left = f"{a}x + {b}"
            else:
                left = f"{a}x - {abs(b)}"

            if e >= 0:
                right = f"{d}x + {e}"
            else:
                right = f"{d}x - {abs(e)}"

            equation = f"{left} = {right}"

        else:

            a = random.randint(2, 6)
            d = random.randint(1, 5)

            while a == d:
                d = random.randint(1, 5)

            x = random.randint(-6, 8)
            b = random.randint(-8, 8)

            e = a * (x + b) - d * x

            app.correct_answer = x

            if b >= 0:
                left = f"{a}(x + {b})"
            else:
                left = f"{a}(x - {abs(b)})"

            if e >= 0:
                right = f"{d}x + {e}"
            else:
                right = f"{d}x - {abs(e)}"

            equation = f"{left} = {right}"

        self.question_label.text = equation

        self.answer_input.text = ""
        self.answer_input.disabled = False
        self.submit_button.disabled = False

        self.answer_input.focus = True

    # =====================================================
    # SUBMIT ANSWER
    # =====================================================

    def submit_answer(self, instance):

        app = App.get_running_app()

        if self.time_left <= 0:
            return

        if self.submit_button.disabled:
            return

        try:

            user_answer = int(
                self.answer_input.text
            )

        except ValueError:

            self.message_label.text = (
                "⚠ Enter a number!"
            )

            self.message_label.color = YELLOW

            return

        if user_answer == app.correct_answer:

            app.combo += 1

            bonus = 10

            if app.combo >= 3:
                bonus += 5

            if app.combo >= 5:
                bonus += 5

            app.score += bonus

            self.message_label.text = (
                f"✓ CORRECT!  +{bonus}"
            )

            self.message_label.color = GREEN

        else:

            app.lives -= 1

            app.combo = 0

            self.message_label.text = (
                "✕ WRONG ANSWER!"
            )

            self.message_label.color = RED

            if app.lives <= 0:

                self.update_screen()

                Clock.schedule_once(
                    lambda dt: self.end_game(),
                    0.7
                )

                return

        self.update_screen()

        Clock.schedule_once(
            lambda dt: self.generate_question(),
            0.35
        )

    # =====================================================
    # UPDATE SCREEN
    # =====================================================

    def update_screen(self):

        app = App.get_running_app()

        self.score_label.text = (
            f"⭐ {app.score}"
        )

        self.combo_label.text = (
            f"🔥 x{app.combo}"
        )

        if app.lives == 3:
            hearts = "❤️❤️❤️"

        elif app.lives == 2:
            hearts = "❤️❤️♡"

        elif app.lives == 1:
            hearts = "❤️♡♡"

        else:
            hearts = "♡♡♡"

        self.lives_label.text = hearts

    # =====================================================
    # END GAME
    # =====================================================

    def end_game(self):

        app = App.get_running_app()

        if app.timer_event:
            app.timer_event.cancel()
            app.timer_event = None

        self.submit_button.disabled = True
        self.answer_input.disabled = True

        app.save_best_score()

        game_over = self.manager.get_screen(
            "gameover"
        )

        game_over.update_result()

        self.manager.current = "gameover"

    # =====================================================
    # QUIT GAME
    # =====================================================

    def quit_game(self, instance):

        app = App.get_running_app()

        if app.timer_event:
            app.timer_event.cancel()
            app.timer_event = None

        self.manager.current = "home"


# =========================================================
# GAME OVER SCREEN
# =========================================================

class GameOverScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=[dp(30), dp(50)],
            spacing=dp(15)
        )

        title = Label(
            text="GAME OVER",
            font_size=dp(38),
            bold=True,
            color=RED,
            size_hint_y=None,
            height=dp(70)
        )

        layout.add_widget(title)

        self.result_label = Label(
            text="",
            font_size=dp(21),
            color=WHITE,
            halign="center"
        )

        self.result_label.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        layout.add_widget(
            self.result_label
        )

        layout.add_widget(
            Widget()
        )

        again = GameButton(
            text="🔄  PLAY AGAIN",
            bg_color=GREEN
        )

        again.bind(
            on_press=self.play_again
        )

        layout.add_widget(again)

        menu = GameButton(
            text="🏠  MAIN MENU",
            bg_color=BLUE
        )

        menu.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "home")
        )

        layout.add_widget(menu)

        exit_button = GameButton(
            text="EXIT",
            bg_color=CARD2
        )

        exit_button.bind(
            on_press=lambda x:
            App.get_running_app().stop()
        )

        layout.add_widget(exit_button)

        self.add_widget(layout)

    def update_result(self):

        app = App.get_running_app()

        self.result_label.text = (
            f"⭐ SCORE\n"
            f"{app.score}\n\n"
            f"🏆 BEST SCORE\n"
            f"{app.best_score}"
        )

    def play_again(self, instance):

        self.manager.current = "difficulty"


# =========================================================
# MAIN APPLICATION
# =========================================================

class MathChallengeApp(App):

    difficulty = "Easy"

    score = 0
    best_score = 0
    lives = 3
    combo = 0

    correct_answer = 0

    timer_event = None

    # -----------------------------------------------------
    # BEST SCORE FILE
    # -----------------------------------------------------

    def get_save_file(self):

        return os.path.join(
            self.user_data_dir,
            "math_challenge.json"
        )

    def load_best_score(self):

        try:

            path = self.get_save_file()

            if os.path.exists(path):

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                    self.best_score = int(
                        data.get("best_score", 0)
                    )

        except Exception:

            self.best_score = 0

    def save_best_score(self):

        if self.score > self.best_score:

            self.best_score = self.score

        try:

            os.makedirs(
                self.user_data_dir,
                exist_ok=True
            )

            path = self.get_save_file()

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    {
                        "best_score":
                        self.best_score
                    },
                    file
                )

        except Exception:
            pass

    # -----------------------------------------------------
    # START NEW GAME
    # -----------------------------------------------------

    def start_new_game(self, difficulty):

        self.difficulty = difficulty

        self.score = 0
        self.lives = 3
        self.combo = 0

        game_screen = self.root.get_screen(
            "game"
        )

        game_screen.start_game()

    # -----------------------------------------------------
    # BUILD
    # -----------------------------------------------------

    def build(self):

        self.title = "Math Challenge"

        self.load_best_score()

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen(
                name="home"
            )
        )

        manager.add_widget(
            DifficultyScreen(
                name="difficulty"
            )
        )

        manager.add_widget(
            GameScreen(
                name="game"
            )
        )

        manager.add_widget(
            GameOverScreen(
                name="gameover"
            )
        )

        return manager

    # -----------------------------------------------------
    # STOP
    # -----------------------------------------------------

    def on_stop(self):

        if self.timer_event:

            self.timer_event.cancel()

            self.timer_event = None

        self.save_best_score()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    MathChallengeApp().run()