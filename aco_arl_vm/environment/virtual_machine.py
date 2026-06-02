import random
from config import VM_SPEED_RANGE, VM_MEMORY_RANGE, VM_ENERGY_COST_PER_MS, MIGRATION_ENERGY_COST

class VirtualMachine:
    def __init__(self, vm_id):
        self.vm_id = vm_id
        self.speed = random.randint(*VM_SPEED_RANGE)
        self.memory = random.randint(*VM_MEMORY_RANGE)
        self.task_queue = []  
        self.energy_consumed = 0.0
        self.total_tasks_executed = 0
        self.total_execution_time = 0.0
        self.total_migration_cost = 0.0
        self.load_history = []
        self.status = "Idle"

    def assign_task(self, task, current_time):
        self.task_queue.append((task, current_time))
        self.status = "Busy"

    def execute_next(self, current_time):
        if not self.task_queue:
            self.status = "Idle"
            return None

        task, enqueue_time = self.task_queue.pop(0)
        exec_time = task.length / self.speed
        energy_used = exec_time * VM_ENERGY_COST_PER_MS

        self.energy_consumed += energy_used
        self.total_execution_time += exec_time
        self.total_tasks_executed += 1
        self.load_history.append(self.get_load())

        task.start_time = current_time
        task.complete(current_time + exec_time)

        self.status = "Busy" if self.task_queue else "Idle"
        return task

    def migrate_task(self, task):
        self.total_migration_cost += MIGRATION_ENERGY_COST
        self.energy_consumed += MIGRATION_ENERGY_COST

    def get_load(self):
        return len(self.task_queue)

    def is_overloaded(self):
        
        return self.get_load() > 3

    def to_dict(self):
        avg_load = sum(self.load_history) / len(self.load_history) if self.load_history else 0
        return {
            "VM ID": self.vm_id,
            "Speed": self.speed,
            "Memory": self.memory,
            "Queue Length": self.get_load(),
            "Energy": self.energy_consumed,
            "Tasks Executed": self.total_tasks_executed,
            "Avg Load": avg_load,
            "Max Load": max(self.load_history) if self.load_history else 0,
            "Min Load": min(self.load_history) if self.load_history else 0,
            "Total Migration Cost": self.total_migration_cost
        }

    def __repr__(self):
        return f"<VM {self.vm_id} | Speed: {self.speed} | Memory: {self.memory}GB | Energy: {self.energy_consumed:.2f} | Load: {self.get_load()}>"
