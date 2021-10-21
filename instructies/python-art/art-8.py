from turtle import *
import random

speed(0)
penup()
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


k = 0
for j in range(400, 0, -60):
    for i in range(-425, 425, 60):
        fillcolor(colors[random.randint(0, len(colors) - 1)])
        begin_fill()
        vorm(i, j, 45, 5, k)
        end_fill()
        k += 1

for _ in range(100):
    fillcolor(colors[random.randint(0, len(colors) - 1)])
    begin_fill()
    vorm(random.randint(-400, 400), random.randint(-400, 0), random.randint(10, 100), 7, random.randint(0, 90))
    end_fill()

done()
