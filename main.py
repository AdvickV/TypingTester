import json
import math
import random
from tkinter import *
import pyglet

COUNT = 0

pyglet.font.add_file('digital-7.ttf')


MILLISECONDS = 0


class TypingTester:

    def __init__(self):
        self.window = Tk()
        self.window.title("Typing Test")
        self.window.config(pady=50, padx=50, bg="#3DB2FF")

        self.seconds = 0
        self.minutes = 0

        self.completed_check = None

        self.inst_label = Label(text="Start typing!", font=("Comic Sans MS", 25, "bold"),  bg="#3DB2FF", fg="#FF2442")
        self.inst_label.grid(column=0, row=0)

        self.timer_label = Label(text="0:00", font=('digital-7', 50, "bold"), bg="#3DB2FF")
        self.timer_label.grid(column=1, row=0, columnspan=2)

        self.canvas = Canvas(width=800, height=100, highlightthickness=1, highlightbackground="black")
        self.text_to_type = self.canvas.create_text(400, 50, font=("None", 10, "bold"), text=self.get_sentence(), width=800, fill="#3E00FF")
        self.canvas.grid(column=0, row=1, columnspan=3, pady=25)

        self.typing_area = Entry(width=133)
        self.typing_area.focus()
        self.typing_area.grid(column=0, row=2, columnspan=3, pady=25)

        self.wpm_label = Label(text="Gross WPM: 0", font=("Times New Roman", 100, "bold"), fg="#FFB830", bg="#3DB2FF")
        self.wpm_label.grid(column=0, row=3, columnspan=3)

        self.started_check = self.window.after(1000, self.check_started)

        self.window.mainloop()

    def get_sentence(self):
        with open("paragraphs.json") as file:
            data = json.load(file)
            sentences = [sentence for sentence in data.values()]
        return random.choice(sentences)

    def check_started(self):
        if self.typing_area.get() == "":
            self.started_check = self.window.after(10, self.check_started)
        else:
            self.window.after_cancel(self.started_check)
            self.start_timer()


    def start_timer(self):
        self.completed_check = self.window.after(10, func=self.check_completed)
        self.inst_label.config(text="Go!")

    def check_completed(self):
        global COUNT, MILLISECONDS
        text_typed = self.typing_area.get()
        if len(text_typed) >= len(self.canvas.itemcget(self.text_to_type, 'text')):
            self.window.after_cancel(self.completed_check)
            wpm = round(float(len(text_typed) / 5) / round(float(self.minutes + (self.seconds / 60)), 2), 2)
            if text_typed == self.canvas.itemcget(self.text_to_type, 'text'):
                self.inst_label.config(text="No Mistakes!")
                self.wpm_label.config(text=f"WPM: {wpm}")
            else:
                self.inst_label.config(text="Mistakes Made!")
                self.wpm_label.config(text=f"WPM: {wpm}")
            return
        else:
            if MILLISECONDS % 800 == 0:
                COUNT += 1
                self.minutes = math.floor(COUNT / 60)
                self.seconds = COUNT % 60
                if len(str(self.minutes)) == 1:
                    minutes_text = f"0{self.minutes}"
                else:
                    minutes_text = self.minutes
                if len(str(self.seconds)) == 1:
                    seconds_text = f"0{self.seconds}"
                else:
                    seconds_text = self.seconds
                self.timer_label.config(text=f"{minutes_text}:{seconds_text}")
            MILLISECONDS += 10
            self.completed_check = self.window.after(10, func=self.check_completed)


TypingTester()
