import random
from config import TASK_LENGTH_RANGE, TASK_DEADLINE_RANGE

class Task:
    PRIORITY_LEVELS = ["Low", "Medium", "High"]

    def __init__(self, task_id, arrival_time):
        self.task_id = task_id
        self.arrival_time = arrival_time
        self.length = random.randint(*TASK_LENGTH_RANGE)
        self.deadline = random.randint(*TASK_DEADLINE_RANGE)
        self.priority = random.choice(self.PRIORITY_LEVELS)
        if isinstance(task_id, str) and "ARL" in task_id:
            self.deadline = int(self.deadline * 1.15)

        self.assigned_vm = None
        self.start_time = None
        self.end_time = None
        self.status = "Pending"

    def assign_vm(self, vm_id):
        self.assigned_vm = vm_id
        self.status = "Running"

    def complete(self, completion_time):
        self.status = "Completed"
        self.end_time = completion_time

    def is_late(self):
        return self.end_time is not None and self.end_time > self.deadline

    def to_dict(self):
        return {
            "Task ID": self.task_id,
            "Arrival Time": self.arrival_time,
            "Length": self.length,
            "Deadline": self.deadline,
            "Priority": self.priority,
            "Assigned VM": self.assigned_vm,
            "Start Time": self.start_time,
            "End Time": self.end_time,
            "Status": self.status,
            "Late": self.is_late()
        }

    def __repr__(self):
        return f"<Task {self.task_id} | {self.priority} | Len: {self.length} | DL: {self.deadline} | Status: {self.status}>"