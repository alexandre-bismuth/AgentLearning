from agents import Agent
from queueModel import Queue, Counter
import random


class Simulation:
    def __init__(self, agents, prob_empty=0.1, init=3):
        self.file_attente = Queue(agents, prob_empty, init)
        self.comptoir = Counter()
        self.agents = agents
        self.recompense_totale = 0
        self.temps = 0

    def run(self, temps_max):
        for t in range(temps_max):
            self.temps += 1
            print(f"Temps {self.temps}")

            # Arrivée d'un nouvel agent dans la file d'attente
            self.file_attente.arriver_nouvel_agent(self.agents)
            print(f"File d'attente: {self.file_attente}")

            # Décision du joueur de remplacer l'agent au comptoir
            if self.comptoir.agent_actuel is None or self.player_decision():
                agent_a_remplacer = self.choose_agent_from_queue()
                if agent_a_remplacer:
                    self.file_attente.ajouter_agent(
                        self.comptoir.remplacer_agent(agent_a_remplacer)
                    )
                    print(f"Agent {agent_a_remplacer} est maintenant au comptoir")

            # Tour du comptoir
            recompense = self.comptoir.tour()
            self.recompense_totale += recompense
            if recompense > 0:
                print(f"Agent au comptoir a quitté, récompense gagnée: {recompense}")

            print(f"Comptoir: {self.comptoir}")
            print(f"Récompense totale: {self.recompense_totale}\n")

    def player_decision(self):
        # Le joueur décide s'il veut remplacer l'agent actuel ou non
        decision = input("Voulez-vous remplacer l'agent actuel ? (o/n) ")
        return decision.lower() == "o"

    def choose_agent_from_queue(self):
        # Le joueur choisit un agent dans la file d'attente
        if not self.file_attente.queue:
            print("La file d'attente est vide.")
            return None

        print("Agents dans la file d'attente :")
        for i, agent in enumerate(self.file_attente.queue):
            print(f"{i}: {agent}")

        choix = int(
            input(f"Choisissez un agent (0-{len(self.file_attente.queue) - 1}) : ")
        )
        if 0 <= choix < len(self.file_attente.queue):
            selected_agent = self.file_attente.queue[choix]
            self.file_attente.queue.remove(selected_agent)
            return selected_agent
        else:
            print("Choix invalide.")
            return None


# Exemple d'utilisation
agents = [
    Agent(prob_quit=0.2, freq=3, reward=10),
    Agent(prob_quit=0.5, freq=1, reward=5),
    Agent(prob_quit=0.3, freq=2, reward=7),
]
simulation = Simulation(agents, prob_empty=0.2)
simulation.run(10)
