from turtle import *

colors = ["red", "cyan", "green", "yellow", "purple", "orange", "blue"]
bgcolor("black")

speed(0)
colormode(255)

for i in range(20):
    for j in range(20):
        circle(j)
        pencolor(colors[i % len(colors)])
        left(j)
        forward(i + 10)

done()
