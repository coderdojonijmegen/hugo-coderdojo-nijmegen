from turtle import *
import random

speed(0)
penup()
bgcolor("black")
colors = ["red", "cyan", "green", "yellow", "purple", "orange", "blue"]


def vorm(x, y, rib, hoeken, rotatie=0):
    goto(x, y)
    right(rotatie)
    pendown()
    for _ in range(hoeken):
        forward(rib)
        right(180 - ((hoeken - 2) * 180 / hoeken))
    penup()
    right(-rotatie)


for i in range(int(360 / 15)):
    pencolor(colors[i % len(colors)])
    vorm(0, 0, 100, 9, 15 * i)

done()
