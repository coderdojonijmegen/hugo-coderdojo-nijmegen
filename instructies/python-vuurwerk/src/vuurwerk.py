import turtle
from time import sleep
from random import randint
from math import sin, cos, pi

aantal_vuurpijlen = 7
stukken = 7
start_positie = (0, -390)

class Vuurpijl:
    def __init__(self, kleur, plaats, snelheid):
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.color(*kleur)
        self.plaats_horizontaal = plaats[0]
        self.plaats_verticaal = plaats[1]
        self.snelheid_horizontaal = snelheid[0]
        self.snelheid_verticaal = snelheid[1]
        self.vanaf_de_grond = plaats == start_positie
        self.zwaartekracht = 0.06

    def beweeg(self):
        self.plaats_verticaal = self.plaats_verticaal + self.snelheid_verticaal
        self.plaats_horizontaal = self.plaats_horizontaal + self.snelheid_horizontaal
        self.snelheid_verticaal = self.snelheid_verticaal - self.zwaartekracht
        self.turtle.clear()
        self.turtle.penup()
        self.turtle.setposition(self.plaats_horizontaal, self.plaats_verticaal)
        self.turtle.pendown()
        self.turtle.dot(5)

    def is_boven(self):
        return self.snelheid_verticaal < 0

    def positie(self):
        return self.plaats_horizontaal, self.plaats_verticaal

    def snelheid(self):
        return self.snelheid_horizontaal, self.snelheid_verticaal

    def clear(self):
        self.turtle.clear()

    def is_vanaf_de_grond(self):
        return self.vanaf_de_grond

def zomaar_een_kleur():
    return randint(1, 255), randint(1, 255), randint(1, 255)


def zomaar_een_richting_en_snelheid(snelheid, i):
    hoek = i * 180 / stukken
    return (snelheid[0] + 1 * sin(pi * hoek),
            snelheid[1] + 1 * cos(pi * hoek))


def main():
    venster = turtle.Screen()
    venster.setup(800, 800)
    venster.colormode(255)
    venster.tracer(0)
    venster.bgcolor("black")

    vuurpijlen = []
    while True:
        for vuurpijl in vuurpijlen:
            vuurpijl.beweeg()
            if vuurpijl.is_vanaf_de_grond() and vuurpijl.is_boven():
                vuurpijl.clear()
                for j in range(stukken):
                    vuurpijlen.append(Vuurpijl(zomaar_een_kleur(), vuurpijl.positie(),
                                               zomaar_een_richting_en_snelheid(vuurpijl.snelheid(), j)))
                vuurpijlen.remove(vuurpijl)
            if vuurpijl.positie()[1] < -400:
                vuurpijlen.remove(vuurpijl)
        if len(vuurpijlen) < aantal_vuurpijlen:
            vuurpijlen.append(Vuurpijl(zomaar_een_kleur(), start_positie, (randint(-15, 15) / 10, 6 + randint(20, 30) / 10)))
        venster.update()
        sleep(0.02)

if __name__ == "__main__":
    main()
