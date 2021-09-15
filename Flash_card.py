from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3 as sql
import string
import os


window = Tk()
window.title("Flash card")
window.iconbitmap(r"media/flash-card.ico")
window.option_add("*font", "Century 20")
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))


connect = sql.connect(r"Dictionary.db")
vacab_now = ""
def Next():
    global connect, i, vocab_now
    i = 0
    vocab_combo.current(0)
    next_btn.config(text="Next")
    flip_btn.config(state=NORMAL)
    char_get = combo.get()
    if char_get == "":
        flip_btn.config(state=DISABLED)
        vocab_label.config(text="Choose the first letter 🡵")
        return
    if char_get != "All":
        cur = connect.cursor()
        cur.execute(f"""SELECT * FROM {char_get.lower()}_table ORDER BY RANDOM() LIMIT 1""")
        eng = cur.fetchone()[0]
        vocab_label.config(text=eng)
        vocab_now = eng
        cur.close()
    if char_get == "All":
        cur = connect.cursor()
        cur.execute(f"""SELECT * FROM all_table ORDER BY RANDOM() LIMIT 1""")
        eng = cur.fetchone()[0]
        vocab_label.config(text=eng)
        vocab_now = eng
        cur.close()

i = 0
def Flip():
    global connect, i, vocab_now
    if i % 2 == 0:
        i += 1
        cur = connect.cursor()
        char_get = combo.get()
        cur.execute(f"SELECT value FROM {char_get.lower()}_table WHERE key='{vocab_now}'")
        thai = cur.fetchone()
        vocab_label.config(text=thai)
        cur.close()
    else:
        i += 1
        vocab_label.config(text=vocab_now)


def OpenPDF():
    os.startfile(r"Vocabulary.pdf")


def ChangeValues(e):
    global connect
    vocab_combo.current(0)
    vocab_label.config(text="")
    char_get = combo.get()
    if char_get == "":
        vocab_combo.config(values=[""])
        return
    else:
        cur = connect.cursor()
        cur.execute(f"SELECT key FROM {char_get.lower()}_table")
        vocab = [""] + cur.fetchall()
        vocab_combo.config(values=vocab)

def ChangeDisplay(e):
    global connect
    flip_btn.config(state=DISABLED)
    vocab_get = vocab_combo.get()
    if vocab_get == "":
        vocab_label.config(text="")
        return
    char_get = combo.get()
    cur = connect.cursor()
    cur.execute(f"SELECT * FROM {char_get.lower()}_table WHERE key='{vocab_get}'")
    translate = cur.fetchone()[1]
    vocab_label.config(text=f"{vocab_get} ☞ {translate}")


fm1 = Frame(bg="#2E4053")
fm1.pack(fill=BOTH)

open_img = Image.open(r"media/main_image.png")
resize = open_img.resize((250, 250), Image.ANTIALIAS)
image = ImageTk.PhotoImage(resize)

img_label = Label(fm1, image=image, bg="#2E4053")
img_label.grid(row=0, column=0, rowspan=2, padx=50, pady=40)

flash_card_label = Label(fm1, text="Flash card⚡", font="broadway 85", fg="#F1C40F", bg="#2E4053")
flash_card_label.grid(row=0, column=1, columnspan=4, padx=20, pady=20)


fm2 = Frame(bg="#2E4053")
fm2.pack(fill=BOTH)

all_ascii = list(string.ascii_uppercase)
all_value = ["", "All"] + all_ascii
combo = ttk.Combobox(fm1, values=all_value, width=8, font="Century 20 bold", cursor="hand2")
combo.current(0)
combo.grid(row=1, column=4, padx=20, pady=20)
combo.bind("<Key>", "break")
combo.bind("<<ComboboxSelected>>", ChangeValues)

Label(fm1, text="      First letter :", bg="#2E4053", fg="white", font="Century 18").grid(row=1, column=3)

vocab_combo = ttk.Combobox(fm1, values=[""], width=18, font="Century 20 bold", cursor="hand2")
vocab_combo.grid(row=1, column=2, padx=20, pady=20)
vocab_combo.bind("<Key>", "break")
vocab_combo.bind("<<ComboboxSelected>>", ChangeDisplay)

Label(fm1, text="All vocabulary from first letter :", bg="#2E4053", fg="white", font="Century 18").grid(row=1, column=1)


fm2 = Frame(bg="#2E4053")
fm2.pack(fill=BOTH)

vocab_label = Label(fm2, text="Let's start🏁", bg="#5D6D7E", fg="white", font="Century 60 bold")
vocab_label.pack(fill=BOTH, ipady=130)


fm3 = Frame(bg="#2E4053")
fm3.pack(fill=BOTH)

flip_btn = Button(fm3, text="Flip", bg="#C0392B", font="Century 20 bold", cursor="hand2", command=Flip, state=DISABLED)
flip_btn.pack(side=LEFT, padx=34, pady=39, ipadx=48, ipady=4)
flip_btn.bind("<Enter>", lambda x: flip_btn.config(fg="#F1C40F"))
flip_btn.bind("<Leave>", lambda x: flip_btn.config(fg="black"))

next_btn = Button(fm3, text="Start", bg="#117864", font="Century 20 bold", cursor="hand2", command=Next)
next_btn.pack(side=LEFT, ipadx=42, ipady=4)
next_btn.bind("<Enter>", lambda x: next_btn.config(fg="#F1C40F"))
next_btn.bind("<Leave>", lambda x: next_btn.config(fg="black"))

pdf_btn = Button(fm3, text="PDF file", bg="#2471A3", font="Century 20 bold", cursor="hand2", command=OpenPDF)
pdf_btn.pack(side=RIGHT, padx=34, ipadx=20, ipady=4)
pdf_btn.bind("<Enter>", lambda x: pdf_btn.config(fg="#F1C40F"))
pdf_btn.bind("<Leave>", lambda x: pdf_btn.config(fg="black"))


window.mainloop()