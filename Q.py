from state import *
import random
from itertools import product
from math import exp
import time
from aux_Q import *
import yaml
from tqdm import tqdm


config = yaml.safe_load(open("config.yaml", "r"))
Rmove = config['Rmove']
Rgoal = config['Rgoal']
Rwrong = config['Rwrong']
epsilon = config['epsilon']
gamma = config['gamma']
alpha = config['alpha']
lim = config['lim']
epoch = config['epochs']
iterations = config['iterations']


grid = [[0] * lim for x in range(lim)]


def init_gen():
    init = (random.randint(0, lim-1), random.randint(0, lim-1))
    return init


def goal_gen():
    goal = (random.randint(0, lim-1), random.randint(0, lim-1))
    return goal


def create():
    Q = dict()
    t1 = list(product([i for i in range(lim)], repeat=2))
    for i in range(lim):
        for j in range(lim):
            for k in t1:
                for l in t1:
                    set1 = actions(state(i, j, k, l, False), lim)
                    set2 = actions(state(i, j, k, l, True), lim)
                    Q[state(i, j, k, l, False)] = dict(
                        zip(set1, [0]*len(set1)))
                    Q[state(i, j, k, l, True)] = dict(zip(set2, [0]*len(set2)))
    return Q


def epsilonGreedy(q):
    actions = list(q.keys())
    if random.uniform(0, 1) < epsilon:
        a = actions[random.randint(0, len(actions)-1)]
    else:
        a = actions[actions.index(max(q, key=q.get))]

    return a


def softmax(q):
    softmax_temp = config['softmax_temperature']
    actions = list(q.keys())
    t = sum([exp(q[x]/softmax_temp) for x in q.keys()])
    weights = [(exp(q[x]/softmax_temp)/t) for x in q.keys()]
    a = random.choices(actions, weights=weights)[0]
    return a


def reward(s, goal, state_blocks, action, action_blocks):
    if (s.x, s.y) == goal and s.aE:
        return Rgoal
    elif s.aE or (s.x, s.y) in state_blocks or ((s.x, s.y) in action_blocks and action.__name__ in action_blocks[(s.x, s.y)]):
        return Rwrong
    else:
        return Rmove


def episode(Q, state_blocks, action_blocks, init, goal, update=False):
    s = state(init[0], init[1], False)
    s.set_init(init)
    s.set_goal(goal)
    moves = []
    Return = 0
    while True:
        qa = Q[s]
        # a = epsilonGreedy(qa)
        a = softmax(qa)
        next_state = a(s)
        r = reward(next_state, goal, state_blocks, a, action_blocks)
        if update:
            Q[s][a] += alpha * \
                (r + gamma*(max(Q[next_state].values())) - Q[s][a])

        if s.aE or (s.x, s.y) in state_blocks or ((s.x, s.y) in action_blocks and a.__name__ in action_blocks[(s.x, s.y)]):
            break

        moves.append((next_state, a))
        s = next_state
        Return += (gamma**(len(moves)-1))*r
        if len(moves) > 5*lim:
            break
    return moves, Return


def train(Q, state_blocks, action_blocks, epochs, iterations):
    start = time.time()
    aT = []
    aR = []
    for epoch in tqdm(range(epochs)):
        #print("Simulating Epoch", epoch)
        goal = goal_gen()
        init = init_gen()
        avgReturn = 0
        for iteration in range(iterations):
            moves, Return = episode(
                Q, state_blocks, action_blocks, init, goal, True)
            avgReturn = (avgReturn*(iteration) + Return)/(iteration+1)
        aT.append((time.time()-start))
        aR.append(avgReturn)
        start = time.time()
        if (epoch+1) % (epochs//20) == 0 and epoch > 0:
            plot(aT, aR, epoch+1, epochs//20)
    dump(Q, state_blocks, action_blocks, lim)
    plot(aT, aR, epochs, epochs//20)


def sim(Q, state_blocks, action_blocks, init, goal):
    moves, _ = episode(Q, state_blocks, action_blocks, init, goal)
    print(init[0], init[1], goal[0], goal[1])
    print("Moves:")
    print("Start: (", init[0], ",", init[1], ")")
    for t in moves:
        print("(", t[0].x, ",", t[0].y, "Move: ", t[1].__name__, ")")
        print()
    return moves
