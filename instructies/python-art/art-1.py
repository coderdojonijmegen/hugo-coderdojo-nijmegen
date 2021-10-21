from turtle import *


colors = ["red", "cyan", "green", "yellow", "white", "orange"]

bgcolor("black")
speed(0)

for x in range(100, 300):
    pencolor(colors[x % 6])
    width(int(x/100 + 1))
    forward(x)
    # if x < 150:
    #     left(91)
    # else:
    right(59)

hideturtle()
done()
