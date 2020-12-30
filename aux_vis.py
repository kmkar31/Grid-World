from turtle import *
from PIL import Image


def draw_base(k, lim,):
    speed(0)
    # GRID
    pu()
    forward(k*lim//2)
    right(90)
    forward(k*lim//2)
    right(90)
    pd()

    # Outer Edges
    for i in range(4):
        width(2)
        color("midnight blue")
        forward(k*lim)
        right(90)
    width(1)
    # Vertical Edges
    color("black")

    def grid():
        for i in range(lim//2):
            pu()
            forward(k)
            right(90)
            pd()
            forward(k*lim)
            pu()
            left(90)
            forward(k)
            left(90)
            pd()
            forward(k*lim)
            right(90)

    grid()
    pu()
    setpos(-(k*lim//2), (-k*lim//2))
    right(90)
    grid()
    speed(0)


def draw_blocks(state_blocks, action_blocks, c, L, R, U, D, k, lim):
    # Filling state_blocks Squares:
    for t in state_blocks:
        pu()
        seth(0)
        color("saddle brown")
        setpos(c(t))
        backward(k//2)
        right(90)
        forward(k//2)
        left(90)
        pd()
        seth(0)
        begin_fill()
        for i in range(4):
            forward(k)
            left(90)
        pd()
        end_fill()

    for a in action_blocks.keys():
        if a[0] < 0 or a[0] >= lim or a[1] < 0 or a[1] >= lim:
            continue
        for x in action_blocks[a]:
            color("maroon")
            pensize(4)
            pu()
            setpos(c(a))
            seth(0)
            if x == L.__name__:
                backward(k//2)

            elif x == R.__name__:
                forward(k//2)

            elif x == U.__name__:
                seth(90)
                forward(k//2)

            elif x == D.__name__:
                seth(90)
                backward(k//2)

            left(90)
            backward(k//2)
            pd()
            forward(k)


def load_assets(k):
    correct = Image.open('assets/correct.gif')
    correct = correct.resize((k-5, k-5))
    correct.save('assets/correct.gif')
    wrong = Image.open('assets/wrong.gif')
    wrong = wrong.resize((k-5, k-5))
    wrong.save('assets/wrong.gif')
    screen = Screen()
    screen.register_shape('assets/correct.gif')
    screen.register_shape('assets/wrong.gif')
    ht()
