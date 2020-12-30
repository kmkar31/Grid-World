class state ():

    def __init__(self, x, y, init=None, goal=None, aE=False):
        self.x = x
        self.y = y
        self.aE = aE
        self.init = init
        self.goal = goal

    def set_init(self, init):
        self.init = init

    def set_goal(self, goal):
        self.goal = goal

    def __hash__(self):
        return hash((self.x, self.y, self.aE, self.init, self.goal))

    def __eq__(self, s):
        return (self.x, self.y, self.aE, self.init, self.goal) == (s.x, s.y, s.aE, s.init, s.goal)


def L(s):
    return state(s.x-1, s.y, s.init, s.goal, s.aE)


def R(s):
    return state(s.x+1, s.y, s.init, s.goal, s.aE)


def D(s):
    return state(s.x, s.y-1, s.init, s.goal, s.aE)


def U(s):
    return state(s.x, s.y+1, s.init, s.goal, s.aE)


def armEngage(s):
    return state(s.x, s.y, s.init, s.goal, not(s.aE))


def actions(s, lim):
    if s.x < lim-1 and s.x > 0:
        actions = [L, R]  # L,R correspond to Left and Right
    elif s.x == lim-1:
        actions = [L]  # Only Left action is allowed
    else:
        actions = [R]  # Only Right action is allowed

    if s.y < lim-1 and s.y > 0:
        actions += [U, D]  # U,D correspond to Up and Down
    elif s.y == lim-1:
        actions.append(D)  # Only Down action is allowed
    else:
        actions.append(U)  # Only Up action is allowed

    if not(s.aE):
        actions.append(armEngage)

    return actions
