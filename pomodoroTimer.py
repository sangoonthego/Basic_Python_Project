import tkinter as tk
import winsound

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15

# Theme color sets
themes = {
    "light": {
        "BG": "#f7f7f7",
        "ACCENT": "#4f8cff",
        "TIMER": "#222831",
        "BUTTON": "#ffffff",
        "BUTTON_ACTIVE": "#e0e7ff",
        "LABEL": "#393e46",
        "TITLE": "#4f8cff"
    },
    "dark": {
        "BG": "#23272f",
        "ACCENT": "#7abaff",
        "TIMER": "#f7f7f7",
        "BUTTON": "#2c313c",
        "BUTTON_ACTIVE": "#3a4252",
        "LABEL": "#e0e7ef",
        "TITLE": "#7abaff"
    }
}
FONT_FAMILY = "Segoe UI, Arial, Helvetica Neue, sans-serif"

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.theme = "light"
        self.colors = themes[self.theme]
        self.mode = tk.StringVar(value="work")
        self.modes = {
            "work": ("Pomodoro", WORK_MIN * 60),
            "short": ("Short Break", SHORT_BREAK_MIN * 60),
            "long": ("Long Break", LONG_BREAK_MIN * 60)
        }
        self.timer_running = False
        self.timer_paused = False
        self.timer_id = None
        self.current_mode = "work"
        self.remaining = self.modes[self.current_mode][1]

        self.root.configure(bg=self.colors["BG"])
        self.create_theme_button()
        self.create_title_label()
        self.create_mode_radio_buttons()
        self.create_timer_label()
        self.create_control_buttons()
        self.create_status_label()
        self.set_mode(self.mode.get())

    def create_theme_button(self):
        self.theme_icon = tk.StringVar()
        self.theme_icon.set("🌞")
        self.theme_button = tk.Button(
            self.root, textvariable=self.theme_icon, command=self.switch_theme,
            font=(FONT_FAMILY, 18), fg=self.colors["ACCENT"], bg=self.colors["BG"],
            activebackground=self.colors["BG"], activeforeground=self.colors["ACCENT"],
            relief="flat", bd=0, highlightthickness=0, cursor="hand2"
        )
        self.theme_button.place(x=560, y=10, width=32, height=32)

    def create_title_label(self):
        self.title_label = tk.Label(self.root, text="Pomodoro Timer", font=(FONT_FAMILY, 20, "bold"), fg=self.colors["TITLE"], bg=self.colors["BG"])
        self.title_label.pack(pady=(18, 0))

    def create_mode_radio_buttons(self):
        self.radio_frame = tk.Frame(self.root, bg=self.colors["BG"])
        self.radio_frame.pack(pady=(10, 0))
        self.radio_buttons = []
        for value, (text, _) in self.modes.items():
            rb = tk.Radiobutton(
                self.radio_frame, text=text, variable=self.mode, value=value, command=self.change_mode,
                font=(FONT_FAMILY, 12), fg=self.colors["LABEL"], bg=self.colors["BG"], selectcolor=self.colors["ACCENT"], activebackground=self.colors["BG"],
                borderwidth=0, highlightthickness=0, indicatoron=0, width=12, pady=6, padx=2, relief="flat"
            )
            rb.pack(side=tk.LEFT, padx=6)
            self.radio_buttons.append(rb)

    def create_timer_label(self):
        self.timer_label = tk.Label(self.root, text="25:00", font=(FONT_FAMILY, 54, "bold"), fg=self.colors["TIMER"], bg=self.colors["BG"])
        self.timer_label.pack(pady=(30, 10))

    def create_control_buttons(self):
        self.button_frame = tk.Frame(self.root, bg=self.colors["BG"])
        self.button_frame.pack(pady=8)
        self.start_button = tk.Button(
            self.button_frame, text="Start", command=self.start_timer, width=10, font=(FONT_FAMILY, 12, "bold"),
            fg=self.colors["ACCENT"], bg=self.colors["BUTTON"], activebackground=self.colors["BUTTON_ACTIVE"], activeforeground=self.colors["ACCENT"],
            relief="flat", bd=0, highlightthickness=0, cursor="hand2"
        )
        self.start_button.pack(side=tk.LEFT, padx=12)
        self.pause_button = tk.Button(
            self.button_frame, text="Pause", command=self.pause_timer, width=10, font=(FONT_FAMILY, 12, "bold"),
            fg=self.colors["ACCENT"], bg=self.colors["BUTTON"], activebackground=self.colors["BUTTON_ACTIVE"], activeforeground=self.colors["ACCENT"],
            relief="flat", bd=0, highlightthickness=0, cursor="hand2"
        )
        self.pause_button.pack(side=tk.LEFT, padx=12)
        self.reset_button = tk.Button(
            self.button_frame, text="Reset", command=self.reset_timer, width=10, font=(FONT_FAMILY, 12, "bold"),
            fg=self.colors["ACCENT"], bg=self.colors["BUTTON"], activebackground=self.colors["BUTTON_ACTIVE"], activeforeground=self.colors["ACCENT"],
            relief="flat", bd=0, highlightthickness=0, cursor="hand2"
        )
        self.reset_button.pack(side=tk.LEFT, padx=12)

    def create_status_label(self):
        self.status_label = tk.Label(self.root, text="Ready to work!", font=(FONT_FAMILY, 14), fg=self.colors["LABEL"], bg=self.colors["BG"])
        self.status_label.pack(pady=(18, 0))

    def set_mode(self, mode):
        self.current_mode = mode
        self.work_sec = self.modes[mode][1]
        self.remaining = self.work_sec
        self.timer_label.config(text=self.format_time(self.remaining))
        if mode == "work":
            self.status_label.config(text="Ready to work!")
        elif mode == "short":
            self.status_label.config(text="Short break! Relax!")
        elif mode == "long":
            self.status_label.config(text="Long break! Enjoy!")
        self.timer_running = False
        self.timer_paused = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def change_mode(self):
        self.set_mode(self.mode.get())

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer_paused = False
            if self.current_mode == "work":
                self.status_label.config(text="Working...")
            elif self.current_mode == "short":
                self.status_label.config(text="Short break in progress...")
            elif self.current_mode == "long":
                self.status_label.config(text="Long break in progress...")
            self.countdown()

    def pause_timer(self):
        if self.timer_running:
            self.timer_paused = True
            self.timer_running = False
            self.status_label.config(text="Paused")
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None

    def reset_timer(self):
        self.set_mode(self.current_mode)

    def countdown(self):
        if self.timer_running and not self.timer_paused and self.remaining > 0:
            self.timer_label.config(text=self.format_time(self.remaining))
            self.remaining -= 1
            self.timer_id = self.root.after(1000, self.countdown)
        elif self.remaining == 0 and self.timer_running:
            self.timer_label.config(text="00:00")
            self.status_label.config(text="Time's up! Take a break!")
            winsound.Beep(1000, 1000)
            self.timer_running = False
            self.timer_paused = False
            self.timer_id = None

    def switch_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.colors = themes[self.theme]
        self.theme_icon.set("🌙" if self.theme == "dark" else "🌞")
        self.update_theme()

    def update_theme(self):
        self.root.configure(bg=self.colors["BG"])
        self.title_label.config(fg=self.colors["TITLE"], bg=self.colors["BG"])
        self.radio_frame.config(bg=self.colors["BG"])
        for rb in self.radio_buttons:
            rb.config(fg=self.colors["LABEL"], bg=self.colors["BG"], selectcolor=self.colors["ACCENT"], activebackground=self.colors["BG"])
        self.timer_label.config(fg=self.colors["TIMER"], bg=self.colors["BG"])
        self.button_frame.config(bg=self.colors["BG"])
        self.start_button.config(fg=self.colors["ACCENT"], bg=self.colors["BUTTON"], activebackground=self.colors["BUTTON_ACTIVE"], activeforeground=self.colors["ACCENT"])
        self.pause_button.config(fg=self.colors["ACCENT"], bg=self.colors["BUTTON"], activebackground=self.colors["BUTTON_ACTIVE"], activeforeground=self.colors["ACCENT"])
        self.reset_button.config(fg=self.colors["ACCENT"], bg=self.colors["BUTTON"], activebackground=self.colors["BUTTON_ACTIVE"], activeforeground=self.colors["ACCENT"])
        self.status_label.config(fg=self.colors["LABEL"], bg=self.colors["BG"])
        self.theme_button.config(fg=self.colors["ACCENT"], bg=self.colors["BG"], activebackground=self.colors["BG"], activeforeground=self.colors["ACCENT"])

    # --- Utility ---
    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()