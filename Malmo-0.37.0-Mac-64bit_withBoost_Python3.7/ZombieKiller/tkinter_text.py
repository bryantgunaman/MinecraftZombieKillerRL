import tkinter as tk
from past.utils import old_div
import time

arena_width=20
arena_breadth=20
canvas_border=20
canvas_width=400

canvas_height = canvas_border + ((canvas_width - canvas_border) * arena_breadth / arena_width)

print(f"canvas_height: {canvas_height}")

canvas_scalex = old_div((canvas_width- canvas_border),arena_width)

canvas_scaley = old_div((canvas_height- canvas_border),arena_breadth)
canvas_orgx = old_div(-arena_width,canvas_scalex)
canvas_orgy = old_div(-arena_breadth,canvas_scaley)

print(f"scalex: {canvas_scalex}")
print(f"scaley: {canvas_scaley}")
print(f"orgx: {canvas_orgx}")
print(f"orgy: {canvas_orgy}")

def canvasX(x):
    return (old_div(canvas_border,2)) + (0.5 + old_div(x,float(arena_width))) * (canvas_width-canvas_border)

def canvasY(y):
    return (old_div(canvas_border,2)) + (0.5 + old_div(y,float(arena_breadth))) * (canvas_height-canvas_border)

while True:
    root = tk.Tk()
    root.wm_title("test")

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, borderwidth=0, highlightthickness=0, bg="black")
    canvas.pack()
    root.update()

    # in the draw
    canvas.delete("all")
    # The board
    canvas.create_rectangle(canvasX(old_div(-arena_width,2)), canvasY(old_div(-arena_breadth,2)), canvasX(old_div(arena_width,2)), canvasY(old_div(arena_breadth,2)), fill="#888888")
    root.update()
    time.sleep(5)



