import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT = "Arial"
try:
    file = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    file = pandas.read_csv("data/french_words.csv")
data = file.to_dict("records")
random_dict = {}


# NEXT CARD
def red_check():
    global timer
    window.after_cancel(timer)
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(title_text, text="French", fill="black")
    global random_dict
    random_dict = random.choice(data)
    canvas.itemconfig(word, text=random_dict["French"], fill="black")
    window.after(3000, func=card_flip)


def green_check():
    to_learn()
    global random_dict, timer
    window.after_cancel(timer)
    try:
        random_dict = random.choice(data)
    except IndexError:
        canvas.itemconfig(canvas_image, image=card_front_img)
        canvas.itemconfig(title_text, text="Title", fill="black")
        canvas.itemconfig(word, text="No word left", fill="black")
    else:
        canvas.itemconfig(canvas_image, image=card_front_img)
        canvas.itemconfig(title_text, text="French", fill="black")
        canvas.itemconfig(word, text=random_dict["French"], fill="black")
        timer = window.after(3000, func=card_flip)


# CARD FLIP
def card_flip():
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(word, text=random_dict["English"], fill="white")
    canvas.itemconfig(title_text, text="English", fill="white")


# TO LEARN
def to_learn():
    try:
        data.remove(random_dict)
    except ValueError:
        pass
    else:
        to_learn_list = pandas.DataFrame(data)
        to_learn_list.to_csv("data/words_to_learn.csv", index=False)


# UI
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, func=card_flip)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526)
canvas_image = canvas.create_image(400, 253, image=card_front_img)
title_text = canvas.create_text(400, 150, text="Title", font=(FONT, 40, "italic"))
word = canvas.create_text(400, 263, text="Word", font=(FONT, 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)
canvas.config(highlightthickness=0, bg=BACKGROUND_COLOR)

right_button = Button(image=right_img, bg=BACKGROUND_COLOR, command=green_check)
right_button.grid(column=1, row=1)

wrong_button = Button(image=wrong_img, bg=BACKGROUND_COLOR, command=red_check)
wrong_button.grid(column=0, row=1)

red_check()
window.mainloop()
