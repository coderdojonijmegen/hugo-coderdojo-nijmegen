from turtle import *
from math import sin

bgcolor("black")
pencolor("white")
speed(0)
a = 6
b = 7
x = 0
y = 0
s = 300

for i in range(1000):
    goto(s * sin(x/150), s * sin(y/150))
    x += a
    y += b

done()
