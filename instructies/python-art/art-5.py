from turtle import *

colors = ["red", "cyan", "green", "yellow", "purple", "orange", "blue"]
bgcolor("black")
speed(0)

a = 0
b = 0
penup()
goto(0, 200)
pendown()

while b < 210:
    pencolor(colors[b % len(colors)])
    forward(a)
    right(b)
    a += 3
    b += 1
    hideturtle()

done()
