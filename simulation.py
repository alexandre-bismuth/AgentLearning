from agents import Agent
from queueModel import Queue, Counter
import random
import numpy as np


class Simulation:
    def __init__(self, agents, geo_queue=0.1, init=0):
        self.wait_line = Queue(agents, geo_queue, init)
        self.counter = Counter()
        self.agents = agents
        self.total_reward = 0
        self.time = 0

    def run(self, max_time):
        for _ in range(max_time):
            self.time += 1
            print(f"Time t_{self.time}:")

            # New agent in the waiting line
            self.wait_line.new_agent_arrival(self.agents)

            # Player's decision
            if self.counter.current_agent is None or self.player_decision():
                agent_to_replace = self.choose_agent_from_queue()
                if agent_to_replace:
                    self.wait_line.add_agent(
                        self.counter.replace_agent(agent_to_replace)
                    )
                    print(f"Agent {agent_to_replace} is now at the counter")

            reward = self.counter.tour()
            self.total_reward += reward
            if reward > 0:
                print(
                    f"Agent au counter successfully exited, récompense gagnée: {reward}"
                )

            print(f"counter: {self.counter}")
            print(f"Récompense totale: {self.total_reward}\n")

    def player_decision(self):
        decision = input("Do you want to replace the current agent ? (y/n) ")
        return decision.lower() == "y"

    def choose_agent_from_queue(self):
        if not self.wait_line.queue:
            print("The waiting line is empty")
            return None

        print("Agents in the waiting line :")
        for i, agent in enumerate(self.wait_line.queue):
            print(f"{i}: {agent}")

        if self.counter.current_agent:
            print(f"The current agent at the counter is {self.counter.current_agent}")
        else:
            print("There is noone at the counter for now")

        choix = int(input(f"Choose an Agent (0-{len(self.wait_line.queue) - 1}) : "))
        if 0 <= choix < len(self.wait_line.queue):
            selected_agent = self.wait_line.queue[choix]
            self.wait_line.queue.remove(selected_agent)
            return selected_agent
        else:
            print("Invalid Choice")
            return None


# Exemple d'utilisation
agents = [
    Agent(1),
    Agent(2),
    Agent(3),
]

simulation = Simulation(agents, geo_queue=0.2, init=5)
simulation.run(10)
