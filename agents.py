import random


class Agent:
    def __init__(self, prob_quit, freq=1, reward=0):
        self.prob_quit = prob_quit
        self.freq = freq
        self.reward = reward

    def __repr__(self):
        return f"Agent(p={self.prob_quit}, freq={self.freq}, reward={self.reward})"

    def quits(self):
        return random.random() < self.prob_quit
