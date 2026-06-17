import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import math
from datetime import datetime

try:
    import winsound
    def beep(kind='ok'):
        freq = 1000 if kind == 'ok' else 500
        dur = 120 if kind == 'ok' else 180
        winsound.Beep(freq, dur)
except Exception:
    def beep(kind='ok'):
        pass

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
LEADERBOARD_FILE = os.path.join(DATA_DIR, 'leaderboard.json')
SAVE_FILE = os.path.join(DATA_DIR, 'savegame.json')

WORDS = {
    'Technology': [
        {'word': 'python', 'hint1': 'Programming language', 'hint2': 'Popular for AI and web development'},
        {'word': 'database', 'hint1': 'Data storage system', 'hint2': 'Used to organize records'},
        {'word': 'algorithm', 'hint1': 'Step-by-step solution', 'hint2': 'Important in computer science'},
        {'word': 'network', 'hint1': 'Connected computers', 'hint2': 'Lets devices communicate'},
        {'word': 'compiler', 'hint1': 'Translates code', 'hint2': 'Turns source code into machine code'}
    ],
    'Animals': [
        {'word': 'elephant', 'hint1': 'Largest land animal', 'hint2': 'Has a trunk'},
        {'word': 'tiger', 'hint1': 'Striped big cat', 'hint2': 'Lives in forests'},
        {'word': 'penguin', 'hint1': 'Bird that cannot fly', 'hint2': 'Lives in cold places'},
        {'word': 'giraffe', 'hint1': 'Very tall animal', 'hint2': 'Has a long neck'},
        {'word': 'dolphin', 'hint1': 'Smart sea animal', 'hint2': 'Uses clicks to communicate'}
    ],
    'Sports': [
        {'word': 'cricket', 'hint1': 'Popular bat-and-ball game', 'hint2': 'Very popular in India'},
        {'word': 'football', 'hint1': 'Played with a round ball', 'hint2': 'Known as soccer in some countries'},
        {'word': 'tennis', 'hint1': 'Racket sport', 'hint2': 'Played on a court'},
        {'word': 'hockey', 'hint1': 'Played with a stick', 'hint2': 'Can be on ice or field'},
        {'word': 'basketball', 'hint1': 'Ball into a hoop', 'hint2': 'Usually 5 players per team'}
    ],
    'Countries': [
        {'word': 'india', 'hint1': 'South Asian country', 'hint2': 'Capital is New Delhi'},
        {'word': 'japan', 'hint1': 'Island nation', 'hint2': 'Capital is Tokyo'},
        {'word': 'brazil', 'hint1': 'Largest country in South America', 'hint2': 'Famous for Rio and the Amazon'},
        {'word': 'canada', 'hint1': 'North American country', 'hint2': 'Known for cold weather and maple leaf'},
        {'word': 'egypt', 'hint1': 'Home of ancient pyramids', 'hint2': 'Located in North Africa'}
    ]
}

DEFAULT_SETTINGS = {'theme': 'dark', 'sound': True, 'timer_enabled': True, 'timer_seconds': 60}
DEFAULT_ACH = {'first_win': False, 'streak_3': False, 'perfect_game': False, 'no_hint_win': False, 'fast_30': False}

ACH_LABELS = {
    'first_win': ('🏆', 'First Win'),
    'streak_3': ('🔥', '3-Win Streak'),
    'perfect_game': ('💎', 'Flawless Round'),
    'no_hint_win': ('🧠', 'No-Hint Win'),
    'fast_30': ('⚡', 'Speed Win'),
}

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

# THEME TOKENS ---------------------------------------------------------
THEMES = {
    'dark': {
        'bg': '#15171c',
        'panel': '#1c1f26',
        'panel_alt': '#22262e',
        'border': '#2c313a',
        'text': '#f1ede4',
        'muted': '#7d8590',
        'accent': '#e8b04b',
        'accent_dark': '#c4902f',
        'good': '#5ce0a0',
        'bad': '#ff5c6c',
        'warn': '#e8b04b',
        'info': '#6fb3e0',
        'tile_idle': '#262a32',
        'tile_idle_text': '#4b505c',
        'rope': '#8a6a3a',
        'post': '#9aa0ab',
    },
    'light': {
        'bg': '#f3efe6',
        'panel': '#ffffff',
        'panel_alt': '#f6f2ea',
        'border': '#e0d9c8',
        'text': '#1f2229',
        'muted': '#7a7468',
        'accent': '#b6792a',
        'accent_dark': '#8f5e1f',
        'good': '#1f9d6c',
        'bad': '#d4434f',
        'warn': '#b6792a',
        'info': '#2f7fb0',
        'tile_idle': '#ece5d6',
        'tile_idle_text': '#a39c8c',
        'rope': '#8a6a3a',
        'post': '#5b554a',
    }
}

DISPLAY_FONT = 'Georgia'
BODY_FONT = 'Helvetica'
MONO_FONT = 'Consolas'


class DataStore:
    def __init__(self):
        self.leaderboard = self.load_json(LEADERBOARD_FILE, [])
        self.settings = self.load_json(os.path.join(DATA_DIR, 'settings.json'), DEFAULT_SETTINGS.copy())
        self.achievements = self.load_json(os.path.join(DATA_DIR, 'achievements.json'), DEFAULT_ACH.copy())
        self.stats = self.load_json(
            os.path.join(DATA_DIR, 'stats.json'),
            {'games_played': 0, 'wins': 0, 'losses': 0, 'current_streak': 0, 'best_score': 0, 'total_score': 0}
        )

    def load_json(self, path, default):
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return default

    def save_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def save_all(self):
        self.save_json(os.path.join(DATA_DIR, 'settings.json'), self.settings)
        self.save_json(os.path.join(DATA_DIR, 'achievements.json'), self.achievements)
        self.save_json(os.path.join(DATA_DIR, 'stats.json'), self.stats)
        self.save_json(LEADERBOARD_FILE, self.leaderboard)


class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Hangman Deluxe')
        self.root.geometry('980x760')
        self.root.minsize(920, 700)
        self.data = DataStore()
        self.apply_theme()

        self.player_name = ''
        self.selected_category = tk.StringVar(value='Technology')
        self.selected_difficulty = tk.StringVar(value='Medium')
        self.timer_value = self.data.settings.get('timer_seconds', 60)
        self.time_left = self.timer_value
        self.timer_job = None

        self.word_info = None
        self.word = ''
        self.guessed = []
        self.wrong = 0
        self.score = 0
        self.hints_used = 0
        self.round_start = None
        self.letter_buttons = {}

        self.build_start_screen()
        self.check_autoload_save()

    # ---------------------------------------------------------------- THEME
    def apply_theme(self):
        s = self.data.settings
        theme_name = s.get('theme', 'dark')
        self.colors = THEMES.get(theme_name, THEMES['dark'])
        self.root.configure(bg=self.colors['bg'])

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ---------------------------------------------------------------- WIDGET HELPERS
    def card(self, parent, alt=False, pad_border=True):
        return tk.Frame(
            parent,
            bg=self.colors['panel_alt'] if alt else self.colors['panel'],
            bd=0,
            highlightthickness=1 if pad_border else 0,
            highlightbackground=self.colors['border']
        )

    def button(self, parent, text, cmd, kind='accent', small=False):
        palette = {
            'accent': (self.colors['accent'], '#1c1306' if self.colors['bg'] == '#15171c' else '#ffffff'),
            'danger': (self.colors['bad'], '#ffffff'),
            'ghost': (self.colors['panel_alt'], self.colors['text']),
        }
        bg, fg = palette.get(kind, palette['accent'])
        b = tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            relief='flat',
            bd=0,
            cursor='hand2',
            padx=14 if small else 18,
            pady=6 if small else 10,
            font=(BODY_FONT, 10 if small else 11, 'bold')
        )
        if kind == 'ghost':
            b.config(highlightthickness=1, highlightbackground=self.colors['border'])
        return b

    def section_label(self, parent, text, bg=None):
        return tk.Label(
            parent,
            text=text.upper(),
            font=(BODY_FONT, 9, 'bold'),
            bg=bg or self.colors['panel'],
            fg=self.colors['muted'],
        )

    # ---------------------------------------------------------------- START SCREEN
    def build_start_screen(self):
        self.clear()
        self.apply_theme()

        outer = tk.Frame(self.root, bg=self.colors['bg'])
        outer.pack(fill='both', expand=True, padx=28, pady=26)

        # Header with mini gallows mark
        header = tk.Frame(outer, bg=self.colors['bg'])
        header.pack(fill='x', pady=(0, 4))

        mark = tk.Canvas(header, width=46, height=46, bg=self.colors['bg'], highlightthickness=0)
        mark.pack(side='left', padx=(0, 14))
        self.draw_mini_gallows(mark)

        title_box = tk.Frame(header, bg=self.colors['bg'])
        title_box.pack(side='left')
        tk.Label(
            title_box, text='HANGMAN', font=(DISPLAY_FONT, 30, 'bold'),
            bg=self.colors['bg'], fg=self.colors['text']
        ).pack(anchor='w')
        tk.Label(
            title_box, text='D E L U X E', font=(BODY_FONT, 11, 'bold'),
            bg=self.colors['bg'], fg=self.colors['accent']
        ).pack(anchor='w')

        tk.Label(
            outer,
            text='Guess the word, one letter at a time, before the rope runs out.',
            font=(BODY_FONT, 11),
            bg=self.colors['bg'],
            fg=self.colors['muted']
        ).pack(anchor='w', pady=(10, 20))

        body = tk.Frame(outer, bg=self.colors['bg'])
        body.pack(fill='both', expand=True)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        # Left: setup card
        setup = self.card(body)
        setup.grid(row=0, column=0, sticky='nsew', padx=(0, 16))

        inner = tk.Frame(setup, bg=self.colors['panel'])
        inner.pack(fill='both', expand=True, padx=28, pady=26)

        self.section_label(inner, 'New Game').pack(anchor='w', pady=(0, 14))

        self.name_var = tk.StringVar(value='')
        self.timer_var = tk.IntVar(value=self.data.settings.get('timer_seconds', 60))
        self.sound_var = tk.BooleanVar(value=self.data.settings.get('sound', True))
        self.theme_var = tk.StringVar(value=self.data.settings.get('theme', 'dark'))

        self.labeled_entry(inner, 'Player name', self.name_var)
        self.labeled_optionmenu(inner, 'Category', self.selected_category, list(WORDS.keys()))
        self.labeled_optionmenu(inner, 'Difficulty', self.selected_difficulty, ['Easy', 'Medium', 'Hard'])
        self.labeled_scale(inner, 'Timer (seconds)', self.timer_var)
        self.labeled_optionmenu(inner, 'Theme', self.theme_var, ['dark', 'light'])

        chk_row = tk.Frame(inner, bg=self.colors['panel'])
        chk_row.pack(fill='x', pady=(6, 18))
        tk.Checkbutton(
            chk_row, text='Sound effects', variable=self.sound_var,
            bg=self.colors['panel'], fg=self.colors['text'],
            selectcolor=self.colors['panel_alt'], activebackground=self.colors['panel'],
            font=(BODY_FONT, 10)
        ).pack(anchor='w')

        btns = tk.Frame(inner, bg=self.colors['panel'])
        btns.pack(fill='x', pady=(4, 0))
        self.button(btns, 'Play', self.start_game).pack(side='left', padx=(0, 8))
        self.button(btns, 'Resume', self.resume_game, kind='ghost').pack(side='left', padx=(0, 8))
        self.button(btns, 'Leaderboard', self.show_leaderboard, kind='ghost').pack(side='left')

        self.status = tk.Label(
            inner, text='', bg=self.colors['panel'], fg=self.colors['muted'],
            font=(BODY_FONT, 9), wraplength=380, justify='left'
        )
        self.status.pack(anchor='w', pady=(16, 0))

        # Right: stats + achievements summary
        right = tk.Frame(body, bg=self.colors['bg'])
        right.grid(row=0, column=1, sticky='nsew')

        stats_card = self.card(right)
        stats_card.pack(fill='x', pady=(0, 16))
        sc_inner = tk.Frame(stats_card, bg=self.colors['panel'])
        sc_inner.pack(fill='both', expand=True, padx=24, pady=22)
        self.section_label(sc_inner, 'Your Record').pack(anchor='w', pady=(0, 12))

        st = self.data.stats
        stat_rows = [
            ('Games played', st['games_played']),
            ('Wins', st['wins']),
            ('Losses', st['losses']),
            ('Win rate', f"{self.win_rate():.1f}%"),
            ('Best score', st.get('best_score', 0)),
            ('Current streak', st.get('current_streak', 0)),
        ]
        for label, val in stat_rows:
            row = tk.Frame(sc_inner, bg=self.colors['panel'])
            row.pack(fill='x', pady=3)
            tk.Label(row, text=label, bg=self.colors['panel'], fg=self.colors['muted'], font=(BODY_FONT, 10)).pack(side='left')
            tk.Label(row, text=str(val), bg=self.colors['panel'], fg=self.colors['text'], font=(BODY_FONT, 10, 'bold')).pack(side='right')

        ach_card = self.card(right)
        ach_card.pack(fill='both', expand=True)
        ac_inner = tk.Frame(ach_card, bg=self.colors['panel'])
        ac_inner.pack(fill='both', expand=True, padx=24, pady=22)
        self.section_label(ac_inner, 'Achievements').pack(anchor='w', pady=(0, 12))

        unlocked_any = False
        for key, (icon, label) in ACH_LABELS.items():
            unlocked = self.data.achievements.get(key, False)
            unlocked_any = unlocked_any or unlocked
            row = tk.Frame(ac_inner, bg=self.colors['panel'])
            row.pack(fill='x', pady=3)
            tk.Label(
                row, text=icon if unlocked else '○', bg=self.colors['panel'],
                fg=self.colors['accent'] if unlocked else self.colors['muted'],
                font=(BODY_FONT, 12)
            ).pack(side='left', padx=(0, 8))
            tk.Label(
                row, text=label, bg=self.colors['panel'],
                fg=self.colors['text'] if unlocked else self.colors['muted'],
                font=(BODY_FONT, 10, 'bold' if unlocked else 'normal')
            ).pack(side='left')
        if not unlocked_any:
            tk.Label(ac_inner, text='Win a round to unlock your first badge.', bg=self.colors['panel'], fg=self.colors['muted'], font=(BODY_FONT, 9, 'italic'), wraplength=260, justify='left').pack(anchor='w', pady=(8, 0))

    def labeled_entry(self, parent, label, var):
        tk.Label(parent, text=label, bg=self.colors['panel'], fg=self.colors['muted'], font=(BODY_FONT, 9, 'bold')).pack(anchor='w', pady=(8, 4))
        e = tk.Entry(
            parent, textvariable=var, font=(BODY_FONT, 12),
            bg=self.colors['panel_alt'], fg=self.colors['text'],
            insertbackground=self.colors['text'], relief='flat',
            highlightthickness=1, highlightbackground=self.colors['border'],
            highlightcolor=self.colors['accent']
        )
        e.pack(fill='x', ipady=6)
        return e

    def labeled_optionmenu(self, parent, label, var, options):
        tk.Label(parent, text=label, bg=self.colors['panel'], fg=self.colors['muted'], font=(BODY_FONT, 9, 'bold')).pack(anchor='w', pady=(12, 4))
        m = tk.OptionMenu(parent, var, *options)
        m.config(
            bg=self.colors['panel_alt'], fg=self.colors['text'], activebackground=self.colors['accent'],
            activeforeground='#1c1306', relief='flat', highlightthickness=1,
            highlightbackground=self.colors['border'], font=(BODY_FONT, 10), anchor='w', padx=10, pady=6
        )
        m['menu'].config(bg=self.colors['panel_alt'], fg=self.colors['text'], activebackground=self.colors['accent'])
        m.pack(fill='x')
        return m

    def labeled_scale(self, parent, label, var):
        tk.Label(parent, text=label, bg=self.colors['panel'], fg=self.colors['muted'], font=(BODY_FONT, 9, 'bold')).pack(anchor='w', pady=(12, 4))
        s = tk.Scale(
            parent, from_=30, to=120, orient='horizontal', variable=var,
            bg=self.colors['panel'], fg=self.colors['text'], troughcolor=self.colors['panel_alt'],
            highlightthickness=0, relief='flat', bd=0, activebackground=self.colors['accent'],
            font=(BODY_FONT, 9)
        )
        s.pack(fill='x')
        return s

    def draw_mini_gallows(self, canvas):
        c = self.colors
        canvas.create_line(6, 42, 40, 42, fill=c['post'], width=3)
        canvas.create_line(14, 42, 14, 6, fill=c['post'], width=3)
        canvas.create_line(14, 6, 34, 6, fill=c['post'], width=3)
        canvas.create_line(34, 6, 34, 14, fill=c['rope'], width=2)
        canvas.create_oval(28, 14, 40, 26, outline=c['accent'], width=2)

    def check_autoload_save(self):
        if os.path.exists(SAVE_FILE):
            self.status.config(text='A saved game is waiting. Tap Resume to pick up where you left off.')

    # ---------------------------------------------------------------- GAME SETUP
    def load_selected_word(self):
        self.word_info = random.choice(WORDS[self.selected_category.get()])
        self.word = self.word_info['word']

    def start_game(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning('Name required', 'Please enter a player name.')
            return

        self.player_name = name
        self.data.settings['theme'] = self.theme_var.get()
        self.data.settings['sound'] = bool(self.sound_var.get())
        self.data.settings['timer_enabled'] = True
        self.data.settings['timer_seconds'] = int(self.timer_var.get())
        self.data.save_all()

        self.apply_theme()
        self.max_attempts = {'Easy': 8, 'Medium': 6, 'Hard': 4}[self.selected_difficulty.get()]
        self.timer_value = int(self.timer_var.get())
        self.new_round(from_resume=False)
        self.build_game_screen()

    def new_round(self, from_resume=False):
        if not from_resume:
            self.load_selected_word()
            self.guessed = []
            self.wrong = 0
            self.score = 0
            self.hints_used = 0
            self.time_left = self.timer_value if self.data.settings.get('timer_enabled', True) else 0
        self.round_start = datetime.now()

    # ---------------------------------------------------------------- GAME SCREEN
    def build_game_screen(self):
        self.clear()
        self.apply_theme()

        root_frame = tk.Frame(self.root, bg=self.colors['bg'])
        root_frame.pack(fill='both', expand=True, padx=24, pady=20)

        # Top bar
        top = tk.Frame(root_frame, bg=self.colors['bg'])
        top.pack(fill='x', pady=(0, 14))

        left_top = tk.Frame(top, bg=self.colors['bg'])
        left_top.pack(side='left')
        tk.Label(left_top, text=self.player_name, font=(DISPLAY_FONT, 16, 'bold'), bg=self.colors['bg'], fg=self.colors['text']).pack(side='left')
        tk.Label(
            left_top, text=f"  ·  {self.selected_category.get()}  ·  {self.selected_difficulty.get()}",
            font=(BODY_FONT, 10), bg=self.colors['bg'], fg=self.colors['muted']
        ).pack(side='left')

        timer_box = self.card(top, alt=True)
        timer_box.pack(side='right')
        self.timer_label = tk.Label(
            timer_box, text=f'⏱ {self.time_left}s', font=(BODY_FONT, 13, 'bold'),
            bg=self.colors['panel_alt'], fg=self.colors['warn'], padx=14, pady=6
        )
        self.timer_label.pack()

        # Main two-column area
        main = tk.Frame(root_frame, bg=self.colors['bg'])
        main.pack(fill='both', expand=True)
        main.grid_columnconfigure(0, weight=3)
        main.grid_columnconfigure(1, weight=2)
        main.grid_rowconfigure(0, weight=1)

        # ----- Left: gallows + word
        left = self.card(main)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 16))
        left_inner = tk.Frame(left, bg=self.colors['panel'])
        left_inner.pack(fill='both', expand=True, padx=20, pady=20)

        self.gallows_canvas = tk.Canvas(left_inner, width=260, height=240, bg=self.colors['panel'], highlightthickness=0)
        self.gallows_canvas.pack(pady=(4, 10))

        self.word_tiles_frame = tk.Frame(left_inner, bg=self.colors['panel'])
        self.word_tiles_frame.pack(pady=(6, 14))

        self.hint_label = tk.Label(
            left_inner, text='', bg=self.colors['panel'], fg=self.colors['info'],
            font=(BODY_FONT, 11, 'italic'), wraplength=420, justify='center'
        )
        self.hint_label.pack(pady=(0, 10))

        self.progress = tk.Canvas(left_inner, width=420, height=10, bg=self.colors['tile_idle'], highlightthickness=0)
        self.progress.pack(pady=(0, 16))

        entry_row = tk.Frame(left_inner, bg=self.colors['panel'])
        entry_row.pack(pady=(0, 10))
        self.entry = tk.Entry(
            entry_row, font=(BODY_FONT, 16), justify='center', width=4,
            bg=self.colors['panel_alt'], fg=self.colors['text'], insertbackground=self.colors['text'],
            relief='flat', highlightthickness=1, highlightbackground=self.colors['border'], highlightcolor=self.colors['accent']
        )
        self.entry.pack(side='left', ipady=6, padx=(0, 10))
        self.entry.bind('<Return>', lambda e: self.guess())
        self.button(entry_row, 'Guess', self.guess, small=True).pack(side='left')

        action_row = tk.Frame(left_inner, bg=self.colors['panel'])
        action_row.pack(pady=(4, 0))
        self.button(action_row, 'Hint', self.hint, kind='ghost', small=True).pack(side='left', padx=4)
        self.button(action_row, 'Save', self.save_game, kind='ghost', small=True).pack(side='left', padx=4)
        self.button(action_row, 'Restart', self.restart_game, kind='ghost', small=True).pack(side='left', padx=4)
        self.button(action_row, 'Home', self.go_home, kind='ghost', small=True).pack(side='left', padx=4)

        # On-screen alphabet keyboard
        kb = tk.Frame(left_inner, bg=self.colors['panel'])
        kb.pack(pady=(16, 0))
        self.letter_buttons = {}
        rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
        for r, row_letters in enumerate(rows):
            row_frame = tk.Frame(kb, bg=self.colors['panel'])
            row_frame.pack(pady=2)
            if r == 2:
                tk.Frame(row_frame, width=20, bg=self.colors['panel']).pack(side='left')
            for ch in row_letters:
                b = tk.Button(
                    row_frame, text=ch.upper(), width=3, font=(BODY_FONT, 10, 'bold'),
                    bg=self.colors['tile_idle'], fg=self.colors['text'], relief='flat', bd=0,
                    cursor='hand2', command=lambda c=ch: self.guess_letter_direct(c)
                )
                b.pack(side='left', padx=2, pady=2)
                self.letter_buttons[ch] = b

        # ----- Right: score + stats + achievements
        right = tk.Frame(main, bg=self.colors['bg'])
        right.grid(row=0, column=1, sticky='nsew')

        score_card = self.card(right)
        score_card.pack(fill='x', pady=(0, 14))
        sc_inner = tk.Frame(score_card, bg=self.colors['panel'])
        sc_inner.pack(fill='both', expand=True, padx=20, pady=18)
        self.section_label(sc_inner, 'Score').pack(anchor='w')
        self.score_label = tk.Label(sc_inner, text='0', font=(DISPLAY_FONT, 30, 'bold'), bg=self.colors['panel'], fg=self.colors['accent'])
        self.score_label.pack(anchor='w', pady=(2, 0))

        stats_card = self.card(right)
        stats_card.pack(fill='x', pady=(0, 14))
        st_inner = tk.Frame(stats_card, bg=self.colors['panel'])
        st_inner.pack(fill='both', expand=True, padx=20, pady=16)
        self.section_label(st_inner, 'Session Stats').pack(anchor='w', pady=(0, 8))
        self.stats_label = tk.Label(st_inner, text='', bg=self.colors['panel'], fg=self.colors['text'], font=(BODY_FONT, 10), justify='left')
        self.stats_label.pack(anchor='w')

        ach_card = self.card(right)
        ach_card.pack(fill='both', expand=True)
        ac_inner = tk.Frame(ach_card, bg=self.colors['panel'])
        ac_inner.pack(fill='both', expand=True, padx=20, pady=16)
        self.section_label(ac_inner, 'Achievements').pack(anchor='w', pady=(0, 8))
        self.ach_text = tk.Label(ac_inner, text='', bg=self.colors['panel'], fg=self.colors['muted'], font=(BODY_FONT, 10), justify='left', wraplength=240)
        self.ach_text.pack(anchor='w')

        self.update_screen()
        self.round_start = datetime.now()
        self.start_timer()

    def guess_letter_direct(self, letter):
        if letter in self.guessed:
            return
        self.entry.delete(0, 'end')
        self.entry.insert(0, letter)
        self.guess()

    # ---------------------------------------------------------------- RENDERING
    def update_screen(self):
        # Word tiles
        for w in self.word_tiles_frame.winfo_children():
            w.destroy()
        for ch in self.word:
            shown = ch.upper() if ch in self.guessed else ''
            revealed = ch in self.guessed
            tile = tk.Label(
                self.word_tiles_frame, text=shown, width=2, height=1,
                font=(MONO_FONT, 18, 'bold'),
                bg=self.colors['panel_alt'] if revealed else self.colors['tile_idle'],
                fg=self.colors['good'] if revealed else self.colors['tile_idle_text'],
                relief='flat', highlightthickness=1, highlightbackground=self.colors['border']
            )
            tile.pack(side='left', padx=3)

        self.hint_label.config(
            text='💡 ' + (self.word_info['hint1'] if self.hints_used == 0
                         else self.word_info['hint2'] if self.hints_used == 1
                         else 'No more hints available')
        )

        self.draw_gallows()
        self.draw_progress()

        # Keyboard button states
        for ch, btn in self.letter_buttons.items():
            if ch in self.guessed:
                if ch in self.word:
                    btn.config(bg=self.colors['good'], fg='#0b1f14', state='disabled')
                else:
                    btn.config(bg=self.colors['bad'], fg='#2a0a0d', state='disabled')
            else:
                btn.config(bg=self.colors['tile_idle'], fg=self.colors['text'], state='normal')

        self.score_label.config(text=str(self.score))
        st = self.data.stats
        self.stats_label.config(
            text=f"Games played   {st['games_played']}\n"
                 f"Wins                {st['wins']}\n"
                 f"Losses             {st['losses']}\n"
                 f"Win rate          {self.win_rate():.1f}%\n"
                 f"Best score       {st.get('best_score', 0)}\n"
                 f"Streak              {st.get('current_streak', 0)}"
        )
        ach_lines = []
        for key, (icon, label) in ACH_LABELS.items():
            if self.data.achievements.get(key):
                ach_lines.append(f'{icon} {label}')
        self.ach_text.config(text='\n'.join(ach_lines) if ach_lines else 'None unlocked yet')

        if hasattr(self, 'timer_label'):
            self.timer_label.config(text=f'⏱ {self.time_left}s')

    def draw_gallows(self):
        c = self.gallows_canvas
        c.delete('all')
        col = self.colors
        cx = 130
        base_y = 220

        # base + post + beam (always visible)
        c.create_line(40, base_y, 200, base_y, fill=col['post'], width=5)  # base
        c.create_line(70, base_y, 70, 30, fill=col['post'], width=5)        # upright
        c.create_line(70, 30, 170, 30, fill=col['post'], width=5)           # beam
        c.create_line(160, 30, 160, 55, fill=col['rope'], width=3)          # rope

        stage = min(self.wrong, 6)
        parts_total = max(self.max_attempts, 1)
        # scale stage to however many attempts are allowed, capped at 6 body parts
        ratio = self.wrong / parts_total if parts_total else 0
        stage = min(6, math.ceil(ratio * 6)) if self.wrong > 0 else 0

        head_y0, head_y1 = 55, 85
        body_y1 = 140
        if stage >= 1:
            c.create_oval(145, head_y0, 175, head_y1, outline=col['bad'], width=3)
        if stage >= 2:
            c.create_line(160, head_y1, 160, body_y1, fill=col['text'], width=3)
        if stage >= 3:
            c.create_line(160, 95, 130, 120, fill=col['text'], width=3)
        if stage >= 4:
            c.create_line(160, 95, 190, 120, fill=col['text'], width=3)
        if stage >= 5:
            c.create_line(160, body_y1, 135, 175, fill=col['text'], width=3)
        if stage >= 6:
            c.create_line(160, body_y1, 185, 175, fill=col['text'], width=3)
            # X eyes for game over emphasis on final stage
            c.create_line(150, 65, 158, 73, fill=col['bad'], width=2)
            c.create_line(158, 65, 150, 73, fill=col['bad'], width=2)
            c.create_line(162, 65, 170, 73, fill=col['bad'], width=2)
            c.create_line(170, 65, 162, 73, fill=col['bad'], width=2)

        c.create_text(cx, base_y + 14, text=f'{self.wrong} / {self.max_attempts} wrong', fill=col['muted'], font=(BODY_FONT, 9))

    def draw_progress(self):
        self.progress.delete('all')
        total = self.max_attempts
        used = min(self.wrong, total)
        width = 420
        w = width * (used / total if total else 0)
        self.progress.create_rectangle(0, 0, width, 10, fill=self.colors['tile_idle'], outline='')
        color = self.colors['good'] if used < total * 0.5 else self.colors['warn'] if used < total - 1 else self.colors['bad']
        if w > 0:
            self.progress.create_rectangle(0, 0, w, 10, fill=color, outline='')

    def win_rate(self):
        gp = self.data.stats['games_played']
        return (self.data.stats['wins'] / gp * 100) if gp else 0.0

    # ---------------------------------------------------------------- GAME LOGIC
    def guess(self):
        letter = self.entry.get().strip().lower()
        self.entry.delete(0, 'end')
        if len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning('Invalid input', 'Enter exactly one letter.')
            return
        if letter in self.guessed:
            messagebox.showwarning('Already guessed', 'You already tried this letter.')
            return

        self.guessed.append(letter)

        if letter in self.word:
            self.score += 10
            if self.data.settings.get('sound', True):
                beep('ok')
        else:
            self.wrong += 1
            self.score -= 5
            if self.data.settings.get('sound', True):
                beep('bad')

        self.evaluate()
        self.update_screen()

    def hint(self):
        if self.hints_used >= 2:
            messagebox.showinfo('Hint', 'No more hints available.')
            return
        self.hints_used += 1
        self.score = max(0, self.score - 2)
        self.update_screen()

    def evaluate(self):
        if all(c in self.guessed for c in self.word):
            self.end_game(True)
        elif self.wrong >= self.max_attempts:
            self.end_game(False)
        elif self.time_left == 0:
            self.end_game(False, timeout=True)

    def start_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        if not self.data.settings.get('timer_enabled', True):
            return

        def tick():
            if self.time_left <= 0:
                self.time_left = 0
                self.update_screen()
                self.end_game(False, timeout=True)
                return
            self.time_left -= 1
            self.update_screen()
            self.timer_job = self.root.after(1000, tick)

        self.timer_job = self.root.after(1000, tick)

    def end_game(self, won, timeout=False):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        self.data.stats['games_played'] += 1

        if won:
            self.data.stats['wins'] += 1
            self.data.stats['current_streak'] = self.data.stats.get('current_streak', 0) + 1
            self.score += 50
            self.data.stats['best_score'] = max(self.data.stats.get('best_score', 0), self.score)
            self.data.stats['total_score'] = self.data.stats.get('total_score', 0) + self.score

            if self.data.settings.get('sound', True):
                beep('ok')

            if not self.data.achievements.get('first_win'):
                self.data.achievements['first_win'] = True
            if self.data.stats['current_streak'] >= 3:
                self.data.achievements['streak_3'] = True
            if self.wrong == 0:
                self.data.achievements['perfect_game'] = True
            if self.hints_used == 0:
                self.data.achievements['no_hint_win'] = True
            if self.time_left >= 30:
                self.data.achievements['fast_30'] = True

            self.save_leaderboard(True)
            self.data.save_all()
            self.update_screen()
            messagebox.showinfo('Congratulations!', f'You won!\nWord: {self.word.upper()}\nFinal Score: {self.score}')
        else:
            self.data.stats['losses'] += 1
            self.data.stats['current_streak'] = 0
            self.data.stats['total_score'] = self.data.stats.get('total_score', 0) + self.score

            if self.data.settings.get('sound', True):
                beep('bad')

            self.save_leaderboard(False)
            self.data.save_all()
            self.update_screen()
            msg = 'Time is up!' if timeout else 'Game Over!'
            messagebox.showerror('Game Over', f'{msg}\nWord: {self.word.upper()}\nFinal Score: {self.score}')

        self.update_screen()
        self.ask_restart()

    def save_leaderboard(self, won):
        entry = {
            'name': self.player_name,
            'score': self.score,
            'won': won,
            'category': self.selected_category.get(),
            'difficulty': self.selected_difficulty.get(),
            'attempts_used': self.wrong,
            'time_left': self.time_left,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        lb = self.data.leaderboard
        lb.append(entry)
        lb[:] = sorted(lb, key=lambda x: (x['score'], x['won']), reverse=True)[:20]
        self.data.save_json(LEADERBOARD_FILE, lb)

    def ask_restart(self):
        if messagebox.askyesno('Play Again', 'Do you want to play again?'):
            self.restart_game()
        else:
            self.go_home()

    def restart_game(self):
        self.new_round(from_resume=False)
        self.build_game_screen()

    def go_home(self):
        self.build_start_screen()

    def save_game(self):
        state = {
            'player_name': self.player_name,
            'category': self.selected_category.get(),
            'difficulty': self.selected_difficulty.get(),
            'word': self.word,
            'word_info': self.word_info,
            'guessed': self.guessed,
            'wrong': self.wrong,
            'score': self.score,
            'hints_used': self.hints_used,
            'time_left': self.time_left,
            'timer_value': self.timer_value,
            'max_attempts': self.max_attempts,
            'settings': self.data.settings,
            'stats': self.data.stats,
            'achievements': self.data.achievements
        }
        self.data.save_json(SAVE_FILE, state)
        messagebox.showinfo('Saved', 'Game saved successfully.')

    def resume_game(self):
        if not os.path.exists(SAVE_FILE):
            messagebox.showwarning('No save file', 'No saved game found.')
            return

        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)

        self.player_name = state['player_name']
        self.selected_category.set(state['category'])
        self.selected_difficulty.set(state['difficulty'])
        self.word = state['word']
        self.word_info = state['word_info']
        self.guessed = state['guessed']
        self.wrong = state['wrong']
        self.score = state['score']
        self.hints_used = state['hints_used']
        self.time_left = state['time_left']
        self.timer_value = state.get('timer_value', 60)
        self.max_attempts = state.get('max_attempts', 6)
        self.data.settings = state.get('settings', self.data.settings)
        self.data.stats = state.get('stats', self.data.stats)
        self.data.achievements = state.get('achievements', self.data.achievements)

        self.apply_theme()
        self.build_game_screen()
        self.update_screen()
        self.start_timer()

    # ---------------------------------------------------------------- LEADERBOARD
    def show_leaderboard(self):
        lb = self.data.leaderboard[:10]
        win = tk.Toplevel(self.root)
        win.title('Leaderboard')
        win.geometry('780x460')
        win.configure(bg=self.colors['bg'])

        tk.Label(
            win, text='🏆 Top Scores', font=(DISPLAY_FONT, 18, 'bold'),
            bg=self.colors['bg'], fg=self.colors['text']
        ).pack(pady=(18, 4))
        tk.Label(
            win, text='Best runs across every player and category', font=(BODY_FONT, 9),
            bg=self.colors['bg'], fg=self.colors['muted']
        ).pack(pady=(0, 14))

        frame = tk.Frame(win, bg=self.colors['bg'])
        frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        cols = ('Name', 'Score', 'Won', 'Category', 'Difficulty', 'Attempts', 'Time Left', 'Date')
        widths = (10, 7, 5, 11, 10, 9, 9, 14)

        header_row = tk.Frame(frame, bg=self.colors['panel_alt'])
        header_row.pack(fill='x')
        for c, w in zip(cols, widths):
            tk.Label(
                header_row, text=c, bg=self.colors['panel_alt'], fg=self.colors['muted'],
                width=w, font=(BODY_FONT, 9, 'bold'), anchor='w', padx=4, pady=8
            ).pack(side='left')

        list_area = tk.Frame(frame, bg=self.colors['bg'])
        list_area.pack(fill='both', expand=True)

        if not lb:
            tk.Label(
                list_area, text='No leaderboard data yet — play a round to set the first score.',
                bg=self.colors['bg'], fg=self.colors['muted'], font=(BODY_FONT, 10), pady=30
            ).pack()
        else:
            for i, e in enumerate(lb):
                row_bg = self.colors['panel'] if i % 2 == 0 else self.colors['bg']
                row = tk.Frame(list_area, bg=row_bg)
                row.pack(fill='x')
                vals = [e['name'], e['score'], '✓' if e['won'] else '✗', e['category'], e['difficulty'], e['attempts_used'], e['time_left'], e['date']]
                for v, w in zip(vals, widths):
                    fg = self.colors['good'] if v == '✓' else self.colors['bad'] if v == '✗' else self.colors['text']
                    tk.Label(
                        row, text=str(v), bg=row_bg, fg=fg, width=w,
                        font=(BODY_FONT, 9), anchor='w', padx=4, pady=6
                    ).pack(side='left')

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = HangmanApp(root)
    app.run()
