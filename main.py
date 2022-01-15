import tkinter as tk
from tkinter import *

root = Tk()
root.geometry("1300x600+0+0")
root.title("Automat sprzedający napoje")
root.configure(bg="light blue")
root.iconbitmap('./assets/icon.ico')

# FUN button_click
expression = ""
equation = StringVar()
def button_click(number):
    global expression
    expression = expression + str(number)
    equation.set(expression)

def clear():
    global expression
    expression = ""
    equation.set("")

def getProductNumberFromUser():
    print(expression)

# LABEL FRAME

left = LabelFrame(root, width=400, height=600, bg="light blue", text="Wprowadź numer produktu", relief=SUNKEN)
left.pack(side=LEFT,padx=10, pady=10)

main = LabelFrame(root, width=500, height=600, bg="light blue", text="Produkty", relief=SUNKEN)
main.pack(side=LEFT, padx=10, pady=10)

right = LabelFrame(root, width=400, height=600, bg="light blue", text="Portfel", relief=SUNKEN)
right.pack(side=RIGHT, padx=10, pady=10)

# LEFT SECTION

keyboard = Label(left, width=350, height=350, bg="light blue", relief=RAISED)
keyboard.pack(side=BOTTOM, padx=10, pady=10)

# ENTRY SECTION

keyboard_Display = Entry(keyboard, width=30, borderwidth=5, textvariable=equation)
keyboard_Display.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

# DEFINE KEYBOARD BUTTONS

button_1 = Button(keyboard, text="1", padx=20, pady=20, command=lambda: button_click(1))
button_2 = Button(keyboard, text="2", padx=20, pady=20, command=lambda: button_click(2))
button_3 = Button(keyboard, text="3", padx=20, pady=20, command=lambda: button_click(3))
button_4 = Button(keyboard, text="4", padx=20, pady=20, command=lambda: button_click(4))
button_5 = Button(keyboard, text="5", padx=20, pady=20, command=lambda: button_click(5))
button_6 = Button(keyboard, text="6", padx=20, pady=20, command=lambda: button_click(6))
button_7 = Button(keyboard, text="7", padx=20, pady=20, command=lambda: button_click(7))
button_8 = Button(keyboard, text="8", padx=20, pady=20, command=lambda: button_click(8))
button_9 = Button(keyboard, text="9", padx=20, pady=20, command=lambda: button_click(9))
button_0 = Button(keyboard, text="0", padx=20, pady=20, command=lambda: button_click(0))
button_clear = Button(keyboard, text="Clear", padx=43, pady=20, command=clear)
button_buy = Button(keyboard, text="Buy Product", padx=57, pady=20, bg="tomato", command=getProductNumberFromUser)

# RENDER BUTTON

button_1.grid(row=1, column=0)
button_2.grid(row=1, column=1)
button_3.grid(row=1, column=2)
button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)
button_7.grid(row=3, column=0)
button_8.grid(row=3, column=1)
button_9.grid(row=3, column=2)
button_0.grid(row=4, column=0)
button_clear.grid(row=4, column=1, columnspan=2)
button_buy.grid(row=5, column=0, columnspan=3)


root.mainloop()