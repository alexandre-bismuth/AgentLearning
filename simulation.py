import numpy as np
import tkinter as tk


class Agent:
    def __init__(self, agent_type, service_prob, reward):
        self.agent_type = agent_type
        self.service_prob = service_prob
        self.reward = reward
        self.time_in_queue = 0

    def __str__(self):
        return f"Agent {self.agent_type} ({self.time_in_queue})"


class QueueSimulation:
    def __init__(
        self,
        num_agent_types,
        service_probs,
        rewards,
        arrival_prob,
        type_distribution,
        k=4,
        sim_mode="manual",
        priority_list=None,
    ):
        self.num_agent_types = num_agent_types
        self.service_probs = service_probs
        self.rewards = rewards
        self.arrival_prob = arrival_prob
        self.type_distribution = type_distribution
        self.k = k
        self.sim_mode = sim_mode
        self.priority_list = priority_list if priority_list is not None else []
        self.queue = [self.create_agent() for _ in range(k)]
        self.current_agent = None
        self.time = 0
        self.total_reward = 0
        self.length = len(self.queue)

    def create_agent(self):
        agent_type = np.random.choice(
            range(self.num_agent_types), p=self.type_distribution
        )
        return Agent(
            agent_type, self.service_probs[agent_type], self.rewards[agent_type]
        )

    def step(self):
        # Check if the current agent is done being served
        if self.current_agent:
            if np.random.rand() < self.current_agent.service_prob:
                self.total_reward += self.current_agent.reward
                self.current_agent = None

        # Increment time_in_queue for all agents in the queue
        for agent in self.queue:
            agent.time_in_queue += 1

        # Add new agent to the queue based on arrival probability
        if np.random.rand() < self.arrival_prob:
            new_agent = self.create_agent()
            self.queue.append(new_agent)

        self.time += 1

        # Automatic mode: select the highest priority agent from the queue
        if self.sim_mode == "automatic" and self.queue:
            # Find the highest priority agent in the queue
            highest_priority_index = min(
                range(len(self.queue)),
                key=lambda i: self.priority_list.index(self.queue[i].agent_type),
            )
            self.swap_agents(highest_priority_index)

        self.length = len(self.queue)

    def get_queue_status(self):
        self.length = len(self.queue)
        return [str(agent) for agent in self.queue]

    def get_current_agent(self):
        return str(self.current_agent) if self.current_agent else "None"

    def get_total_reward(self):
        return self.total_reward

    def swap_agents(self, queue_index):
        if 0 <= queue_index < len(self.queue):
            if self.current_agent:
                self.queue[queue_index], self.current_agent = (
                    self.current_agent,
                    self.queue[queue_index],
                )
            else:
                self.current_agent = self.queue.pop(queue_index)


class QueueSimulationGUI:
    def __init__(self, master, simulation):
        self.master = master
        self.simulation = simulation
        self.master.title("Queue Simulation")

        # Frame for displaying the time
        self.time_frame = tk.Frame(master)
        self.time_frame.pack(pady=10)

        self.time_label = tk.Label(
            self.time_frame, text="Time: 0", font=("Helvetica", 14)
        )
        self.time_label.pack()

        # Frame for displaying the queue
        self.queue_frame = tk.Frame(master)
        self.queue_frame.pack(pady=10)

        self.queue_label = tk.Label(
            self.queue_frame,
            text=f"Queue - Length: {self.simulation.length}",
            font=("Helvetica", 14),
        )
        self.queue_label.pack()

        self.queue_canvas = tk.Canvas(
            self.queue_frame, width=600, height=150, bg="white"
        )
        self.queue_canvas.pack()

        # Frame for displaying the current agent at the counter
        self.counter_frame = tk.Frame(master)
        self.counter_frame.pack(pady=10)

        self.counter_label = tk.Label(
            self.counter_frame, text="Counter", font=("Helvetica", 14)
        )
        self.counter_label.pack()

        self.counter_canvas = tk.Canvas(
            self.counter_frame, width=200, height=100, bg="white"
        )
        self.counter_canvas.pack()

        # Frame for displaying the total reward
        self.reward_frame = tk.Frame(master)
        self.reward_frame.pack(pady=10)

        self.reward_label = tk.Label(
            self.reward_frame, text="Total Reward: 0", font=("Helvetica", 14)
        )
        self.reward_label.pack()

        # Frame for action buttons
        self.action_frame = tk.Frame(master)
        self.action_frame.pack(pady=10)

        self.next_step_button = tk.Button(
            self.action_frame, text="Next Step", command=self.next_step
        )
        self.next_step_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(
            self.action_frame, text="Reset", command=self.reset_simulation
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Frame for input and switch button
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=10)

        self.index_label = tk.Label(
            self.input_frame, text="Enter Queue Index:", font=("Helvetica", 14)
        )
        self.index_label.pack(side=tk.LEFT)

        self.index_entry = tk.Entry(self.input_frame, width=5)
        self.index_entry.pack(side=tk.LEFT, padx=5)

        self.switch_button = tk.Button(
            self.input_frame, text="Switch", command=self.switch_agent
        )
        self.switch_button.pack(side=tk.LEFT, padx=10)

        self.reset_simulation()

    def next_step(self):
        self.simulation.step()
        self.update_labels()

    def switch_agent(self):
        try:
            agent_index = int(self.index_entry.get())
            self.simulation.swap_agents(agent_index)
            self.update_labels()
        except Exception:
            pass  # We could imagine adding an error message here

    def update_labels(self):
        self.time_label.config(text=f"Time: {self.simulation.time}")
        self.reward_label.config(
            text=f"Total Reward: {self.simulation.get_total_reward()}"
        )
        self.queue_label.config(
            text=f"Queue - Length: {self.simulation.length}",
        )

        # Update queue visualization
        self.queue_canvas.delete("all")
        for idx, agent in enumerate(self.simulation.queue):
            self.queue_canvas.create_rectangle(
                10 + 110 * idx, 10, 100 + 110 * idx, 60, fill="lightblue"
            )
            self.queue_canvas.create_text(55 + 110 * idx, 35, text=str(agent))

        # Update counter visualization
        self.counter_canvas.delete("all")
        if self.simulation.current_agent:
            self.counter_canvas.create_rectangle(50, 10, 150, 60, fill="lightgreen")
            self.counter_canvas.create_text(
                100, 35, text=str(self.simulation.current_agent.agent_type)
            )
        else:
            self.counter_canvas.create_text(100, 35, text="Empty")

    def reset_simulation(self):
        self.simulation = QueueSimulation(
            self.simulation.num_agent_types,
            self.simulation.service_probs,
            self.simulation.rewards,
            self.simulation.arrival_prob,
            self.simulation.type_distribution,
            self.simulation.k,
            self.simulation.sim_mode,
            self.simulation.priority_list,
        )
        self.update_labels()


def main():
    # Number of agent types
    num_agent_types = 6

    # Service probabilities for each type
    service_probs = [
        0.7,
        0.5,
        0.3,
        0.4,
        0.8,
        0.5,
    ]

    # Rewards for each type
    # Can be uniform if we want to maximise speed of service
    rewards = [10, 20, 30, 20, 4, 50]  # Rewards for each type

    # Probabilty that a new agent joins the queue
    arrival_prob = 0.5

    # If someone joins the queue, distribution of agent types
    type_distribution = [
        0.3,
        0.15,
        0.2,
        0.1,
        0.2,
        0.05,
    ]

    # Number of agents in the queue at t = 0
    nb_agents_in_queue = 5

    # Do we choose manually each time or do we setup a priority list ?
    sim_mode = "automatic"  # "manual" or "automatic"
    priority_list = [0, 1, 2, 3, 4, 5]

    # Simulation execution
    simulation = QueueSimulation(
        num_agent_types,
        service_probs,
        rewards,
        arrival_prob,
        type_distribution,
        nb_agents_in_queue,
        sim_mode,
        priority_list,
    )
    root = tk.Tk()
    gui = QueueSimulationGUI(root, simulation)
    root.mainloop()


if __name__ == "__main__":
    main()
