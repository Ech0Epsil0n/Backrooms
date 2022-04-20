from tkinter import *
import random
from random import randint

root = Tk()
root.geometry("800x600")
root.title("backrooms test")
root.iconbitmap("e:/PycharmProjects/Backrooms/Assets/Video/Main Menu")

global our_images, count
count = -1

out_images = [PhotoImage(file = "e:/PycharmProjects/Backrooms/Assets/Video/Main Menu/main menu.png"),
              PhotoImage(file = "e:/PycharmProjects/Backrooms/Assets/Video/Main Menu/main menu2.png")]

# Create a canvas
my_canvas = Canvas(root, width = 800, height = 600, highlightthickness = 0)
my_canvas.pack(fill = "both", expand = True)

# Set canvas image
my_canvas.create_image(0, 0, image = out_images[0], anchor = "nw")

def next():
    global count
    if count == 1:
        my_canvas.create_image(0, 0, image = out_images[0], anchor = "nw")
        count = 0
    else:
        my_canvas.create_image(0, 0, image = out_images[count + 1], anchor = "nw")
        count += 1

    root.after(randint(200, 2000), next)

next()
mainloop()
