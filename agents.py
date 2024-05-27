import numpy as np

agent_types = {
    1: [0.3, 2, 7],
    2: [0.5, 1, 5],
    3: [0.2, 3, 10],
}


class Agent:
    def __init__(self, type):
        self.type = type
        self.prob_quit = agent_types[self.type][0]
        self.freq = agent_types[self.type][1]
        self.reward = agent_types[self.type][2]
        self.time_to_quit = self.next_quit_time()

    def __repr__(self):
        return f"Agent_{self.type}"

    def next_quit_time(self):
        return np.random.geometric(p=self.prob_quit)

    def decrement_time_to_quit(self):
        if self.time_to_quit > 0:
            self.time_to_quit -= 1

    def is_quitting(self):
        return self.time_to_quit == 0
