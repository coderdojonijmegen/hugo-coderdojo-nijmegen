import turtle
from collections import namedtuple
from math import sin, cos
from random import randint
from time import sleep


WindowSize = namedtuple("WindowSize", "w, h")
Speed = namedtuple("Speed", "x, y")
Color = namedtuple("Color", "r, g, b")
Position = namedtuple("Position", "x, y")

WINDOW_SIZE = WindowSize(1000, 1000)
NUM_FIREWORKS = 40
MAX_X_SPEED = 20
START_COLOR = Color(255, 170, 0)
FULLY_DIMMED_COLOR = Color(0, 0, 0)
START_POS = Position(0, -500)
DIM_FACTOR = 0.96
GRAVITY = 0.3
RADIUS_SPARKS = 6
RADIUS = 2


class Window:
    def __init__(self):
        self.window = turtle.Screen()
        self.window.setup(*WINDOW_SIZE)
        self.window.tracer(0)
        self.window.colormode(255)
        self.window.bgcolor(0, 0, 0)

    def update(self):
        self.window.update()


class Firework:

    def __init__(self, color: Color, pos: Position, start_speed: Speed, dim_factor: float = 0.0) -> None:
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.start_pos = pos
        self.dim_factor = dim_factor
        self.pos_x = pos.x
        self.pos_y = pos.y
        self.speed_x = start_speed.x
        self.speed_y = start_speed.y
        self.gravity = GRAVITY
        self.radius = RADIUS_SPARKS
        self.color = color
        self.turtle.setposition(self.pos_x, self.pos_y)

    def draw(self) -> None:
        self.turtle.clear()
        self.turtle.color(self.color)
        if self.is_from_ground:
            self.turtle.setposition(self.pos_x, self.pos_y)
            self.turtle.dot(RADIUS)
        else:
            self.dim_color()
            self.turtle.penup()
            self.turtle.setposition(self.pos_x, self.pos_y)
            self.turtle.pendown()
            self.turtle.dot(RADIUS_SPARKS)

    def move(self) -> None:
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.speed_y -= self.gravity

    @property
    def is_on_screen(self) -> bool:
        return (-WINDOW_SIZE.w / 2 <= self.pos_x <= WINDOW_SIZE.w / 2 and
                -WINDOW_SIZE.h / 2 <= self.pos_y <= WINDOW_SIZE.h / 2)

    @property
    def is_fully_dimmed(self) -> bool:
        return self.color == FULLY_DIMMED_COLOR

    @property
    def is_going_down(self) -> bool:
        return self.speed_y <= 0

    @property
    def is_from_ground(self):
        return self.start_pos == START_POS

    @property
    def pos(self) -> Position:
        return Position(self.pos_x, self.pos_y)

    @property
    def speed(self) -> Speed:
        return Speed(self.speed_x, self.speed_y)

    def clear(self) -> None:
        self.turtle.clear()

    def dim_color(self):
        color = self.color
        new_color = []
        for i, c in enumerate(color):
            new_color.append(int(c * self.dim_factor))
        self.color = Color(*new_color)


def random_start_speed() -> Speed:
    return Speed(randint(-MAX_X_SPEED, MAX_X_SPEED) / 4, 20 + randint(-3, 40) / 10)


def random_speed(current_speed: Speed, speed: int, spark: int, sparks: int) -> Speed:
    angle = spark * 180 / sparks
    speed_variance = (randint(10, 14) / 10)
    speed_x = speed * sin(angle) * speed_variance
    speed_y = speed * cos(angle) * speed_variance
    return Speed(current_speed.x + speed_x,
                 current_speed.y + speed_y)


def random_color() -> Color:
    return Color(randint(0, 255), randint(0, 255), randint(0, 255))


def do_fireworks():
    window = Window()

    text = turtle.Turtle()
    text.hideturtle()
    text.color("gold")
    text.penup()
    text.setposition((0, -200))
    text.pendown()
    text.write("Gelukkig 2025!", font=("serif", 50, "normal"), align="center")
    text.penup()
    text.setposition((0, -250))
    text.pendown()
    text.write("CoderDojo Nijmegen", font=("sans serif", 25, "normal"), align="center")

    fireworks = []
    while True:
        for firework in fireworks:
            firework.move()
            firework.draw()
            if firework.is_fully_dimmed:
                firework.clear()
                fireworks.remove(firework)
            if firework.is_going_down and firework.is_from_ground:
                firework.clear()
                num_sparks = randint(10, 25)
                color = random_color()
                speed = randint(1, 3)
                for i in range(0, num_sparks):
                    fireworks.append(Firework(color, firework.pos, random_speed(firework.speed, speed, i, num_sparks),
                                              DIM_FACTOR))
                fireworks.remove(firework)
        if len(fireworks) < NUM_FIREWORKS:
            fireworks.append(Firework(START_COLOR, START_POS, random_start_speed()))
        window.update()
        sleep(0.02)


if __name__ == "__main__":
    do_fireworks()
