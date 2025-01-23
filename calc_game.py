
import tkinter as tk
from tkinter import ttk
import random
import math

class App:

    lvl = 1
    operators = ["+", "-"]
    current_operator = "+"
    problem = "2+2"
    score = 0
    score_t = 5
    answer = 4
    number_1 = 2
    number_2 = 2
    timer = 11
    lost = 0
    welcome_screen = True
    timeout = False
    gameFrm = None
    lvlT = None
    prblmT = None
    submitBtn = None
    welcFrm = None

    def __init__(self, master) -> None:
        self.master = master
        s = ttk.Style()
        s.configure('mw.TButton', font=("Arial", 25), padding=10)
        s.configure('mw.TLabel', font=("Arial", 19), padding=5)
        s.configure('mw.TEntry', font=("Arial", 19), padding=5)
        self.TimerT = ttk.Label(master, text="", style='mw.TLabel')
        self.answer_entry = ttk.Entry(master, style="mw.TEntry", width=30)
        self.restart()
        self.update_timer()

    def restart(self):
        self.lvl = 1
        self.score = 0
        self.score_t = 5
        self.operators = ["+", "-"]
        self.timer = 11
        if self.welcFrm:
            self.welcFrm.grid_forget()
        self.welcFrm = ttk.Frame(self.master, padding=10)
        self.welcFrm.grid()
        self.welcFrm.place(relx=.5, rely=0.5, anchor="c")
        WT1 = ttk.Label(self.welcFrm, text="Добро пожаловать.", style='mw.TLabel')
        WT1.grid(column=0, row=0, pady=(0, 0))
        WT2 = ttk.Label(self.welcFrm, text="Нажмите на кнопку ниже чтобы начать игру", style='mw.TLabel')
        WT2.grid(column=0, row=1, pady=(10, 0))
        startBtn = ttk.Button(self.welcFrm, text="Начать игру",
                              command=lambda: [WT1.grid_forget(), WT2.grid_forget(), startBtn.grid_forget(),
                                               self.welcFrm.grid_forget(), self.game()],
                              style='mw.TButton')
        startBtn.grid(column=0, row=2, pady=(85, 0), ipadx=20, ipady=20)

    def game(self):
        self.welcome_screen = False
        if self.timeout:
            self.update_timer()
            self.timeout = False
        self.timer = 11  # Сбрасываем таймер при начале новой игры
        self.gameFrm = ttk.Frame(self.master, padding=10)
        self.gameFrm.grid()
        self.gameFrm.place(relx=.5, rely=.5, anchor="c")
        self.lvlT = ttk.Label(self.gameFrm, text="Ваш уровень: " + str(self.lvl) + "\nОчки: " + str(int(self.score)), style='mw.TLabel')
        self.lvlT.grid(column=0, row=0, rowspan=1)
        self.prblmT = ttk.Label(self.gameFrm, text="Сколько будет " + self.problem + "?", style='mw.TLabel')
        self.prblmT.grid(column=0, row=1, rowspan=1)
        self.answer_entry.grid(column=0, row=2, sticky="ew", pady=(10,0))


        def game_update():
            try:
                user_answer = float(self.answer_entry.get())
                if math.isclose(user_answer, self.answer, abs_tol=0.001):
                    self.score += (2 ** self.lvl) / 2
                    if self.score > self.score_t:
                        self.lvl += 1
                        self.score_t = (2 ** self.lvl / 2) * 5
                    self.generate_problem()
                    self.lvlT.config(text="Ваш уровень: " + str(self.lvl) + "\nОчки: " + str(int(self.score)))
                    self.prblmT.config(text="Сколько будет " + self.problem + "?")
                    self.answer_entry.delete(0, tk.END)
                    self.timer = 11
                else:
                    self.lost_game()
            except ValueError:
                    self.prblmT.config(text="Пожалуйста введите число")
            

        self.submitBtn = ttk.Button(self.gameFrm, text="Подтвердить", command=game_update, style='mw.TButton')
        self.submitBtn.grid(column=0, row=3, rowspan=1, pady=(10, 0))
        self.generate_problem()
        self.lvlT.config(text="Ваш уровень: " + str(self.lvl) + "\nОчки: " + str(int(self.score)))
        self.prblmT.config(text="Сколько будет " + self.problem + "?")
        self.TimerT.grid(column=0, row=1, pady=(10,0))

    def generate_problem(self):
        self.current_operator = random.choice(self.operators)
        if self.lvl > 2 and "*" not in self.operators:
            self.operators.append("*")
            self.operators.append("/")

        if self.current_operator in ["+", "-"]:
            self.number_1 = random.randint(1, 10 + 2 ** self.lvl)
            self.number_2 = random.randint(1, 10 + 2 ** self.lvl)
            self.problem = str(self.number_1) + self.current_operator + str(self.number_2)
        elif self.current_operator == "*":
            self.number_1 = random.randint(2, int(1 + 1.5 ** self.lvl))
            self.number_2 = random.randint(2, int(1 + 1.5 ** self.lvl))
            self.problem = str(self.number_1) + self.current_operator + str(self.number_2)
        elif self.current_operator == "/":
            self.number_2 = random.randint(2, int(1 + 1.5 ** self.lvl))
            self.number_1 = self.number_2 * random.randint(2, int(2 ** (self.lvl / 2)))
            self.problem = str(self.number_1) + self.current_operator + str(self.number_2)
        self.calculate_answer()
    def calculate_answer(self):
        self.answer = eval(self.problem)

    def update_timer(self):
        if self.welcome_screen:
            self.timer = 11
        if self.timer > 0:
            self.timer -= 1
            self.TimerT.config(text="Времени на ответ осталось: " + str(self.timer))
            self.master.after(1000, self.update_timer)
        else:
            self.lost_game()
            self.timeout = True

    def lost_game(self):
        self.timer = 11 # Сбрасываем таймер при проигрыше
        self.lost = 1
        if self.gameFrm:
            self.lvlT.grid_forget()
            self.prblmT.grid_forget()
            self.answer_entry.grid_forget()
            self.submitBtn.grid_forget()
            self.TimerT.grid_forget()
            self.gameFrm.grid_forget()
        if self.welcFrm:
            self.welcFrm.grid_forget()
        lostFrm = ttk.Frame(self.master, padding=10)
        lostFrm.grid()
        lostFrm.place(relx=.5, rely=0.5, anchor="c")
        LT1 = ttk.Label(lostFrm, text="Вы проиграли.", style='mw.TLabel')
        LT1.grid(column=0, row=0, pady=(0, 0))
        LT2 = ttk.Label(lostFrm, text="Вы продержались до " + str(self.lvl) + " уровня\nОчки: "+ str(int(self.score)), style='mw.TLabel')
        LT2.grid(column=0, row=1, pady=(10, 0))
        startBtn = ttk.Button(lostFrm, text="Начать заново",
                              command=lambda: [LT1.grid_forget(), LT2.grid_forget(), startBtn.grid_forget(),
                                               lostFrm.grid_forget(), self.game()],
                              style='mw.TButton')
        startBtn.grid(column=0, row=2, pady=(85, 0), ipadx=20, ipady=20)
        self.lvl = 1
        self.score = 0
        self.score_t = 5
        self.operators = ["+", "-"]

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Игровой калькулятор")
    root.iconbitmap("calc.ico")
    root.geometry("700x500")
    root.resizable(width=False, height=False)
    app = App(root)
    root.mainloop()
