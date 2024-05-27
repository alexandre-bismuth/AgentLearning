from collections import deque
import random
import numpy as np


class Queue:
    def __init__(self, agents, geo_param, init):
        self.geo_param = geo_param
        self.queue = deque()
        self.time_to_next_arrival = self.next_arrival_time()
        self.initialize_queue(agents, init)

    def next_arrival_time(self):
        return np.random.geometric(p=1 - self.geo_param)

    def initialize_queue(self, agents, init):
        weights = [agent.freq for agent in agents]
        for _ in range(init):
            new_agent = random.choices(agents, weights=weights, k=1)[0]
            self.add_agent(new_agent)

    def add_agent(self, agent):
        self.queue.append(agent)

    def pull_agent(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return None

    def next_agent(self):
        return self.queue[0] if self.queue else None

    def new_agent_arrival(self, agents):
        if self.time_to_next_arrival == 0:
            weights = [agent.freq for agent in agents]
            new_agent = random.choices(agents, weights=weights, k=1)[0]
            self.add_agent(new_agent)
            self.time_to_next_arrival = self.next_arrival_time()
        else:
            self.time_to_next_arrival -= 1

    def __repr__(self):
        return f"Waiting Line:({list(self.queue)})"


class Counter:
    def __init__(self):
        self.current_agent = None

    def replace_agent(self, agent):
        old_agent = self.current_agent
        self.current_agent = agent
        return old_agent

    def tour(self):
        if self.current_agent:
            self.current_agent.decrement_time_to_quit()
            if self.current_agent.is_quitting():
                reward = self.current_agent.reward
                self.current_agent = None
                return reward
        return 0

    def __repr__(self):
        return f"Counter(current_agent={self.current_agent})"
