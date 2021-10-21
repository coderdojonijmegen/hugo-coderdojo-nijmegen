from turtle import *

colors = ["red", "cyan", "green", "yellow", "white", "orange"]

colormode(255)
speed(0)
width(1)
bgcolor(50, 0, 70)
pencolor(255, 255, 0)


def shape(angle, side, limit):
    reverse_direction = 200
    forward(side)

    pencolor(colors[side % 6])
    if side % (reverse_direction * 2) == 0:
        angle = angle + 2
    elif side % reverse_direction == 0:
        angle = angle - 1

    right(angle)
    side += 2
    if side < limit:
        shape(angle, side, limit)


angle = 119
side = 0
limit = 800
shape(angle, side, limit)

done()
