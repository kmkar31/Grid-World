from turtle import *
from Q import *
import random
import sys
import time
from copy import deepcopy
from PIL import Image
from aux_vis import *


k = config['scale_factor']


def c(p):
    return ((k*(1-lim)//2+k*p[0]), (k*(1-lim)//2+k*p[1]))
# ==========================================================================================================


def extrapolate(action_blocks):
    forbidden = deepcopy(action_blocks)
    for x in action_blocks:
        if action_blocks[x] == [L.__name__]:
            if (x[0]-1, x[1]) in forbidden:
                forbidden[(x[0]-1, x[1])] += [R.__name__]
            else:
                forbidden[(x[0]-1, x[1])] = [R.__name__]
        elif action_blocks[x] == [R.__name__]:
            if (x[0]+1, x[1]) in forbidden:
                forbidden[(x[0]+1, x[1])] += [L.__name__]
            else:
                forbidden[(x[0]+1, x[1])] = [L.__name__]
        elif action_blocks[x] == [U.__name__]:
            if (x[0], x[1]+1) in forbidden:
                forbidden[(x[0], x[1]+1)] += [D.__name__]
            else:
                forbidden[(x[0], x[1]+1)] = [D.__name__]
        elif action_blocks[x] == [D.__name__]:
            if (x[0], x[1]-1) in forbidden:
                forbidden[(x[0], x[1]-1)] += [U.__name__]
            else:
                forbidden[(x[0], x[1]-1)] = [U.__name__]
    return forbidden


def random_gen(state_blocks):
    inits = []
    goals = []
    for i in range(6):
        init = (random.randint(0, lim-1), random.randint(0, lim-1))
        goal = (random.randint(0, lim-1), random.randint(0, lim-1))

        while init in state_blocks:
            init = (random.randint(0, lim-1), random.randint(0, lim-1))
        while goal in state_blocks:
            goal = (random.randint(0, lim-1), random.randint(0, lim-1))
        inits.append(init)
        goals.append(goal)
    #inits.append((0, 9))
    #goals.append((9, 0))
    return inits, goals


def visualize(inits, goals, state_blocks, action_blocks, Q):
    draw_base(k, lim)
    draw_blocks(state_blocks, action_blocks, c, L, R, U, D, k, lim)
    colors = ["purple", "red", "green", "orange",
              "dark slate blue", "light sea green", "lime"]
    i = 0
    for init, goal in zip(inits, goals):
        color(colors[i % 7])
        moves = sim(Q, state_blocks, action_blocks, init, goal)
        pu()
        setpos(c(list(goal)))
        pd()
        write("GOAL", align="center", font=("Arial", "8", "bold"))
        pu()
        setpos(c(list(init)))
        pd()
        write("START", align="center", font=("Arial", "8", "bold"))
        pensize(2)
        for i in range(len(moves)):
            t = moves[i]
            speed(1)
            setpos(c([t[0].x, t[0].y]))
            if i == len(moves) - 1:
                if pos() == c(goal):
                    shape('assets/correct.gif')
                    stamp()
                else:
                    shape('assets/wrong.gif')
                    stamp()
        ht()
        i += 1
        time.sleep(1)


def main(args):
    actions = [x.__name__ for x in [L, R, U, D]]
    if args[1] in ["True", "true"]:
        if args[0] in ["True", "true"]:
            state_blocks = [init_gen()
                            for i in range(int(float(args[2])*lim**2))]
            action_blocks = dict(zip([init_gen()
                                      for i in range(int(float(args[2])*lim**2))], [[random.choice(actions)] for i in range(int(float(args[2])*lim**2))]))
            inits, goals = random_gen(state_blocks)
        else:
            state_blocks = []
            action_blocks = dict()
            inits = []
            goals = []
            for x in open(args[3], 'r'):
                state_blocks.append((int(x.split()[0]), int(x.split()[1])))
            for x in open(args[4], 'r'):
                action_blocks[(int(x.split()[0]), int(x.split()[1]))
                              ] = [actions[int(x.split()[2])]]
            for x in open(args[5], 'r'):
                inits.append((int(x.split()[0]), int(x.split()[1])))
                goals.append((int(x.split()[2]), int(x.split()[3])))
        action_blocks = extrapolate(action_blocks)
        print("Training")
        Q = create()
        avg = train(Q, state_blocks, action_blocks, epoch, iterations)
    else:
        Q, state_blocks, action_blocks = load(args[2])
        if args[0] in ["True", "true"]:
            inits, goals = random_gen(state_blocks)
        else:
            inits = []
            goals = []
            for x in open(args[3], 'r'):
                inits.append((int(x.split()[0]), int(x.split()[1])))
                goals.append((int(x.split()[2]), int(x.split()[3])))

    load_assets(k)
    print("Simulating")
    visualize(inits, goals, state_blocks, action_blocks, Q)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Insufficient Arguments.")
        print("Argument 1: Random or User-Defined Initialization")
        print("Argument 2: Train or Load pretrained Q values")
        print("If User Defined: Arguments 3 and 4 are state_blocks areas and action_blocks respty ")
        print("Argument 5: A list of pairs of starts and goals respty IF User Defined")
        sys.exit()
    main(sys.argv[1:])
    done()
