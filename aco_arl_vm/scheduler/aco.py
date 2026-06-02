import numpy as np
import random
from config import (
    NUM_VIRTUAL_MACHINES,
    ACO_ALPHA, ACO_BETA,
    ACO_EVAPORATION_RATE, ACO_PHEROMONE_INIT, ACO_PHEROMONE_BOOST, RANDOM_SEED
)

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

class AntColonyOptimizer:
    def __init__(self):
        
        self.pheromone = np.full(NUM_VIRTUAL_MACHINES, ACO_PHEROMONE_INIT, dtype=float)

    def choose_vm(self, vm_list):
        heuristic = np.array([self._heuristic(vm) for vm in vm_list])
        probs = (self.pheromone ** ACO_ALPHA) * (heuristic ** ACO_BETA)

        probs /= probs.sum() if probs.sum() != 0 else 1
        selected = np.random.choice(len(vm_list), p=probs)
        return selected

    def _heuristic(self, vm):

        return 1.0 / (vm.get_load() + 1)

    def update_pheromone(self, selected_vm, reward):
        adjusted_reward = reward * 1.2
        self.pheromone *= (1 - ACO_EVAPORATION_RATE)
        self.pheromone[selected_vm] += ACO_PHEROMONE_BOOST * adjusted_reward

    def print_pheromones(self):
        print("Pheromone Levels:", self.pheromone.round(3).tolist())