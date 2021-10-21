from turtle import *

colors = ["red", "cyan", "green", "yellow", "purple", "orange", "blue"]
bgcolor("black")
color("white")
speed(0)


def square(x, y, s, c):
    goto(x, y)
    pendown()
    right(c)
    for _ in range(4):
        forward(s)
        right(90)
    penup()


for i in range(1, 7):
    for j in range(10):
        pencolor(colors[i % len(colors)])
        square(0, 0, j * 5 + 50, i * 3)

done()
