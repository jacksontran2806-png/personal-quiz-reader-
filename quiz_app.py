import tkinter as tk
from tkinter import filedialog, messagebox
import random

# ── Palette ──────────────────────────────────────────────────────────────────
BG        = "#0f0f1a"
CARD      = "#1a1a2e"
ACCENT    = "#e94560"
ACCENT2   = "#0f3460"
TEXT      = "#eaeaea"
MUTED     = "#7a7a9a"
SUCCESS   = "#2ecc71"
ERROR     = "#e74c3c"
BTN_HV    = "#ff6b81"

FONT_TITLE  = ("Georgia", 28, "bold")
FONT_SUB    = ("Georgia", 13, "italic")
FONT_BODY   = ("Courier New", 12)
FONT_BOLD   = ("Courier New", 12, "bold")
FONT_SMALL  = ("Courier New", 10)
FONT_OPTION = ("Courier New", 13)
FONT_BTN    = ("Georgia", 12, "bold")

FORMAT_HINT = """\
Each question block must follow this exact format:

  Question text here
  A) Option one
  B) Option two
  C) Option three
  D) Option four
  B

  ← leave a blank line between questions →

• The correct answer (A/B/C/D) goes alone on the last line.
• Separate every question with one blank line.
• Save the file as plain .txt (UTF-8 encoding)."""


# ── Helpers ──────────────────────────────────────────────────────────────────
def parse_questions(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    questions = []
    for block in blocks:
        lines = block.split("\n")
        if len(lines) < 6:
            continue
        questions.append({
            "question": lines[0].strip(),
            "options":  [lines[i].strip() for i in range(1, 5)],
            "answer":   lines[5].strip().upper(),
        })
    return questions


def validate_questions(questions):
    valid_letters = {"A", "B", "C", "D"}
    for i, q in enumerate(questions, 1):
        if q["answer"] not in valid_letters:
            return False, f"Question {i}: answer '{q['answer']}' is not A/B/C/D."
        if len(q["options"]) != 4:
            return False, f"Question {i}: must have exactly 4 options."
    return True, ""


# ── Splash Screen ─────────────────────────────────────────────────────────────
def show_splash(on_done):
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.configure(bg=BG)
    w, h = 420, 260
    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()
    splash.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    tk.Frame(splash, bg=ACCENT, height=4).pack(fill="x")

    body = tk.Frame(splash, bg=BG, pady=30)
    body.pack(fill="both", expand=True)

    tk.Label(body, text="✦ Quiz App ✦", font=("Georgia", 26, "bold"),
             bg=BG, fg=TEXT).pack()
    tk.Label(body, text="crafted by", font=("Georgia", 11, "italic"),
             bg=BG, fg=MUTED).pack(pady=(18, 2))
    tk.Label(body, text="lamhariem", font=("Georgia", 22, "bold"),
             bg=BG, fg=ACCENT).pack()
    tk.Label(body, text="© 2025  —  All rights reserved",
             font=("Courier New", 9), bg=BG, fg=MUTED).pack(pady=(8, 0))

    tk.Frame(splash, bg=ACCENT, height=4).pack(fill="x")

    splash.after(2200, lambda: [splash.destroy(), on_done()])


# ── App ───────────────────────────────────────────────────────────────────────
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App  •  by lamhariem")
        self.root.configure(bg=BG)
        self.root.geometry("720x580")
        self.root.resizable(False, False)

        self.questions   = []
        self.current_idx = 0
        self.score       = 0
        self.selected    = tk.StringVar()

        self.container = tk.Frame(root, bg=BG)
        self.container.pack(fill="both", expand=True)

        # footer watermark always visible
        tk.Label(root, text="✦ lamhariem",
                 font=("Courier New", 9), bg=BG, fg=MUTED).pack(side="right", padx=10, pady=4)

        self.show_welcome()

    # ── decorative top bar ────────────────────────────────────────────────────
    def _topbar(self, parent, title, subtitle=""):
        bar = tk.Frame(parent, bg=ACCENT2, pady=18)
        bar.pack(fill="x")
        tk.Label(bar, text=title, font=FONT_TITLE,
                 bg=ACCENT2, fg=TEXT).pack()
        if subtitle:
            tk.Label(bar, text=subtitle, font=FONT_SUB,
                     bg=ACCENT2, fg=MUTED).pack(pady=(2, 0))
        # red accent stripe
        tk.Frame(parent, bg=ACCENT, height=3).pack(fill="x")

    # ── clear frame ──────────────────────────────────────────────────────────
    def _clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    # ── button factory ───────────────────────────────────────────────────────
    def _btn(self, parent, text, cmd, color=ACCENT, width=22):
        b = tk.Button(parent, text=text, command=cmd,
                      font=FONT_BTN, bg=color, fg=TEXT,
                      activebackground=BTN_HV, activeforeground=TEXT,
                      relief="flat", cursor="hand2",
                      padx=14, pady=8, width=width)
        b.bind("<Enter>", lambda e: b.config(bg=BTN_HV))
        b.bind("<Leave>", lambda e: b.config(bg=color))
        return b

    # ══════════════════════════════════════════════════════════════════════════
    # SCREEN 1 — Welcome
    # ══════════════════════════════════════════════════════════════════════════
    def show_welcome(self):
        self._clear()
        self._topbar(self.container, "✦ Quiz App ✦", "Test your knowledge")

        body = tk.Frame(self.container, bg=BG, pady=30)
        body.pack(fill="both", expand=True)

        # format hint card
        card = tk.Frame(body, bg=CARD, padx=24, pady=18,
                        highlightbackground=ACCENT2, highlightthickness=1)
        card.pack(padx=40, pady=(0, 24), fill="x")

        tk.Label(card, text="📋  File Format Guide",
                 font=FONT_BOLD, bg=CARD, fg=ACCENT).pack(anchor="w")
        tk.Label(card, text=FORMAT_HINT, font=FONT_SMALL,
                 bg=CARD, fg=TEXT, justify="left").pack(anchor="w", pady=(8, 0))

        self._btn(body, "📂  Load Questions File",
                  self.load_file).pack(pady=(0, 10))
        tk.Label(body, text="Only .txt files are supported",
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack()

    # ══════════════════════════════════════════════════════════════════════════
    # File loading
    # ══════════════════════════════════════════════════════════════════════════
    def load_file(self):
        path = filedialog.askopenfilename(
            title="Select your questions file",
            filetypes=[("Text files", "*.txt")]
        )
        if not path:
            return
        try:
            qs = parse_questions(path)
        except Exception as e:
            messagebox.showerror("Read Error", f"Could not read file:\n{e}")
            return

        if not qs:
            messagebox.showerror("Format Error",
                                 "No valid questions found.\n"
                                 "Please check the format guide.")
            return

        ok, msg = validate_questions(qs)
        if not ok:
            messagebox.showerror("Format Error", msg)
            return

        self.questions = qs
        self.start_quiz()

    # ══════════════════════════════════════════════════════════════════════════
    # SCREEN 2 — Question
    # ══════════════════════════════════════════════════════════════════════════
    def start_quiz(self):
        random.shuffle(self.questions)
        self.current_idx = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        self._clear()
        q   = self.questions[self.current_idx]
        num = self.current_idx + 1
        tot = len(self.questions)

        self._topbar(self.container,
                     f"Question {num} of {tot}",
                     f"Score so far: {self.score}")

        body = tk.Frame(self.container, bg=BG, padx=40, pady=20)
        body.pack(fill="both", expand=True)

        # progress bar
        bar_bg = tk.Frame(body, bg=ACCENT2, height=6)
        bar_bg.pack(fill="x", pady=(0, 20))
        fill_w = int((num - 1) / tot * 720)
        tk.Frame(bar_bg, bg=ACCENT, height=6, width=fill_w).place(x=0, y=0)

        # question text
        q_card = tk.Frame(body, bg=CARD, padx=20, pady=14,
                          highlightbackground=ACCENT2, highlightthickness=1)
        q_card.pack(fill="x", pady=(0, 18))
        tk.Label(q_card, text=q["question"], font=FONT_BOLD,
                 bg=CARD, fg=TEXT, wraplength=580, justify="left").pack(anchor="w")

        # answer options
        self.selected.set("")
        self.option_btns = []
        for opt in q["options"]:
            letter = opt[0]
            rb = tk.Radiobutton(
                body, text=opt, variable=self.selected, value=letter,
                font=FONT_OPTION, bg=BG, fg=TEXT,
                activebackground=BG, activeforeground=ACCENT,
                selectcolor=CARD, indicatoron=True,
                anchor="w", padx=10, pady=4, cursor="hand2"
            )
            rb.pack(fill="x", pady=2)
            self.option_btns.append(rb)

        self.feedback_lbl = tk.Label(body, text="", font=FONT_BOLD,
                                     bg=BG, fg=SUCCESS)
        self.feedback_lbl.pack(pady=(12, 0))

        self.submit_btn = self._btn(body, "Submit Answer", self.submit_answer)
        self.submit_btn.pack(pady=(10, 0))

    def submit_answer(self):
        answer = self.selected.get()
        if not answer:
            messagebox.showwarning("No answer", "Please select an option first!")
            return

        q = self.questions[self.current_idx]
        correct = q["answer"]

        # lock options
        for rb in self.option_btns:
            rb.config(state="disabled")
        self.submit_btn.config(state="disabled")

        if answer == correct:
            self.score += 1
            self.feedback_lbl.config(
                text="✅  Correct!", fg=SUCCESS)
        else:
            self.feedback_lbl.config(
                text=f"❌  Wrong! Correct answer: {correct}", fg=ERROR)

        # next / finish
        if self.current_idx + 1 < len(self.questions):
            self._btn(self.feedback_lbl.master, "Next Question →",
                      self.next_question, color=ACCENT2).pack(pady=(8, 0))
        else:
            self._btn(self.feedback_lbl.master, "See Results",
                      self.show_results, color=ACCENT2).pack(pady=(8, 0))

    def next_question(self):
        self.current_idx += 1
        self.show_question()

    # ══════════════════════════════════════════════════════════════════════════
    # SCREEN 3 — Results
    # ══════════════════════════════════════════════════════════════════════════
    def show_results(self):
        self._clear()
        tot = len(self.questions)
        pct = int(self.score / tot * 100)

        if pct == 100:
            grade, color = "Perfect! 🏆", SUCCESS
        elif pct >= 70:
            grade, color = "Well done! 🎉", ACCENT
        elif pct >= 40:
            grade, color = "Keep practising 📚", "#f39c12"
        else:
            grade, color = "Better luck next time 💪", ERROR

        self._topbar(self.container, "Quiz Complete!", grade)

        body = tk.Frame(self.container, bg=BG, pady=30)
        body.pack(fill="both", expand=True)

        # score card
        card = tk.Frame(body, bg=CARD, padx=30, pady=24,
                        highlightbackground=color, highlightthickness=2)
        card.pack(padx=60, pady=(10, 30))

        tk.Label(card, text=f"{self.score} / {tot}",
                 font=("Georgia", 48, "bold"), bg=CARD, fg=color).pack()
        tk.Label(card, text=f"{pct}% correct",
                 font=FONT_SUB, bg=CARD, fg=MUTED).pack()

        btn_row = tk.Frame(body, bg=BG)
        btn_row.pack()
        self._btn(btn_row, "🔄  Play Again",
                  self.start_quiz, color=ACCENT, width=18).pack(side="left", padx=8)
        self._btn(btn_row, "📂  Load New File",
                  self.show_welcome, color=ACCENT2, width=18).pack(side="left", padx=8)

        tk.Label(body, text="made with ♥ by lamhariem",
                 font=("Georgia", 10, "italic"), bg=BG, fg=MUTED).pack(pady=(24, 0))


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # hide main window until splash is done
    show_splash(lambda: [root.deiconify(), QuizApp(root)])
    root.mainloop()
