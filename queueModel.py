from agents import Agent
from collections import deque
import random


class Queue:
    def __init__(self, agents, prob_empty=0.1, init=3):
        self.prob_empty = prob_empty
        self.queue = deque()
        self.initialize_queue(agents, init)

    def initialize_queue(self, agents, init):
        weights = [agent.freq for agent in agents]
        for _ in range(init):
            new_agent = random.choices(agents, weights=weights, k=1)[0]
            self.ajouter_agent(new_agent)

    def ajouter_agent(self, agent):
        self.queue.append(agent)

    def retirer_agent(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return None

    def prochain_agent(self):
        return self.queue[0] if self.queue else None

    def arriver_nouvel_agent(self, agents):
        if random.random() > self.prob_empty:
            weights = [agent.freq for agent in agents]
            new_agent = random.choices(agents, weights=weights, k=1)[0]
            self.ajouter_agent(new_agent)

    def __repr__(self):
        return f"FileAttente({list(self.queue)})"


class Counter:
    def __init__(self):
        self.agent_actuel = None

    def remplacer_agent(self, agent):
        ancien_agent = self.agent_actuel
        self.agent_actuel = agent
        return ancien_agent

    def tour(self):
        if self.agent_actuel:
            if self.agent_actuel.quits():
                reward = self.agent_actuel.reward
                self.agent_actuel = None
                return reward
        return 0

    def __repr__(self):
        return f"Comptoir(agent_actuel={self.agent_actuel})"
