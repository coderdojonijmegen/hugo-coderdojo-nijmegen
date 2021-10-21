from turtle import *

colors = ["red", "cyan", "green", "yellow", "purple", "orange", "blue"]
bgcolor("black")
speed(0)

sides = 5
distance = 100
for i in range(10 * sides):
    pencolor(colors[i % len(colors)])
    distance += 20
    forward(distance)
    right(2 * 360.0 / sides + 1)

done()
