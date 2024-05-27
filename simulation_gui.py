import tkinter as tk
from agents import Agent
from queueModel import Queue, Counter
import random


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


class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agent Simulation")

        # Initialize agents
        self.agents = [Agent(1), Agent(2), Agent(3)]
        self.simulation = Simulation(self.agents, geo_queue=0.2, init=5)

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Create frames
        self.queue_frame = tk.Frame(self.root)
        self.queue_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.counter_frame = tk.Frame(self.root)
        self.counter_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Queue label and listbox
        self.queue_label = tk.Label(self.queue_frame, text="Queue")
        self.queue_label.pack()

        self.queue_listbox = tk.Listbox(self.queue_frame)
        self.queue_listbox.pack()

        # Counter label and value
        self.counter_label = tk.Label(self.counter_frame, text="Counter")
        self.counter_label.pack()

        self.counter_value = tk.Label(self.counter_frame, text="")
        self.counter_value.pack()

        # Buttons
        self.next_step_button = tk.Button(
            self.root, text="Next Step", command=self.next_step
        )
        self.next_step_button.pack()

    def update_display(self):
        self.queue_listbox.delete(0, tk.END)
        for agent in self.simulation.wait_line.queue:
            self.queue_listbox.insert(tk.END, str(agent))

        current_agent = self.simulation.counter.current_agent
        self.counter_value.config(text=str(current_agent) if current_agent else "None")

    def next_step(self):
        self.simulation.run(1)
        self.update_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()
