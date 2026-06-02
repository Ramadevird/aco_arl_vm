import numpy as np
import random
from config import (
    NUM_VIRTUAL_MACHINES, Q_LEARNING_ALPHA,
    Q_LEARNING_GAMMA, Q_LEARNING_EPSILON, RANDOM_SEED
)

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


class QLearningAgent:
    def __init__(self):
        self.q_table = np.zeros((3, 5, NUM_VIRTUAL_MACHINES))  

    def _priority_to_index(self, priority):
        mapping = {"Low": 0, "Medium": 1, "High": 2}
        return mapping.get(priority, 1)

    def _load_to_index(self, avg_vm_load):
        if avg_vm_load <= 1:
            return 0
        elif avg_vm_load <= 3:
            return 1
        else:
            return 2

    def choose_action(self, task, vm_list):
        state = self._get_state(task, vm_list)
        priority_idx, load_idx = state

        if random.uniform(0, 1) < Q_LEARNING_EPSILON:
            return random.randint(0, NUM_VIRTUAL_MACHINES - 1)
        else:
            return int(np.argmax(self.q_table[priority_idx, load_idx]))

    def update_q_value(self, task, vm_id, reward, vm_list):
        if task.priority == "High":
            reward += 2
        elif task.priority == "Medium":
            reward += 1

        state = self._get_state(task, vm_list)
        priority_idx, load_idx = state

        current_q = self.q_table[priority_idx][load_idx][vm_id]
        max_future_q = np.max(self.q_table[priority_idx][load_idx])
        new_q = current_q + Q_LEARNING_ALPHA * (reward + Q_LEARNING_GAMMA * max_future_q - current_q)

        self.q_table[priority_idx][load_idx][vm_id] = new_q

    def _get_state(self, task, vm_list):
        priority_idx = self._priority_to_index(task.priority)
        avg_load = sum(vm.get_load() for vm in vm_list) / len(vm_list)
        load_idx = self._load_to_index(avg_load)
        return (priority_idx, load_idx)

    def print_q_table(self):
        print("Q-table snapshot:")
        print(self.q_table)