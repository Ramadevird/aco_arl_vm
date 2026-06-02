import random
from config import NUM_VIRTUAL_MACHINES, NUM_TASKS, SIMULATION_TIME, SCHEDULING_INTERVAL, RANDOM_SEED
from environment.virtual_machine import VirtualMachine
from environment.task import Task

class CloudEnvironment:
    def __init__(self, mode=None):
        random.seed(RANDOM_SEED)
        self.vms = [VirtualMachine(vm_id=i) for i in range(NUM_VIRTUAL_MACHINES)]
        self.mode = mode
        self.tasks = self._generate_tasks()
        self.time = 0
        self.completed_tasks = []
        self.waiting_tasks = []
        self.scheduler = None

    def _generate_tasks(self):
        tasks = []
        for i in range(NUM_TASKS):
            
            arrival_time = random.randint(0, SIMULATION_TIME // 2)
            task = Task(task_id=f"ARL-{i}", arrival_time=arrival_time) if self.mode == "ARL" else Task(task_id=i, arrival_time=arrival_time)
            tasks.append(task)
        tasks.sort(key=lambda t: t.arrival_time)
        return tasks

    def register_scheduler(self, scheduler):
        self.scheduler = scheduler

    def run(self):
        dt = 1  
        while self.time < SIMULATION_TIME:
            self._process_new_arrivals()
            if self.scheduler:
                self.scheduler.schedule(self.waiting_tasks, self.vms, self.time)
            self._run_vm_executions()

            if self.time % SCHEDULING_INTERVAL == 0:
                self._check_and_migrate()

            self.time += dt

    def _process_new_arrivals(self):
        
        arriving_tasks = [t for t in self.tasks if t.arrival_time == self.time]
        if arriving_tasks:
            self.waiting_tasks.extend(arriving_tasks)
            self.tasks = [t for t in self.tasks if t.arrival_time != self.time]

    def _run_vm_executions(self):
        for vm in self.vms:
            executed_task = vm.execute_next(self.time)
            if executed_task:
                self.completed_tasks.append(executed_task)
                
                self.waiting_tasks = [t for t in self.waiting_tasks if t.task_id != executed_task.task_id]

    def _check_and_migrate(self):
        overloaded_vms = [vm for vm in self.vms if vm.is_overloaded()]
        underloaded_vms = [vm for vm in self.vms if vm.get_load() == 0]
        for vm in overloaded_vms:
            if vm.task_queue:
                
                task_to_migrate, _ = vm.task_queue.pop(0)
                vm.migrate_task(task_to_migrate)
                if underloaded_vms:
                    target_vm = underloaded_vms.pop(0)
                else:
                    target_vm = min(self.vms, key=lambda vm: vm.get_load())
                target_vm.assign_task(task_to_migrate, self.time)
                
    def get_results(self):
        return {
            "total_tasks": NUM_TASKS,
            "completed_tasks": len(self.completed_tasks),
            "vm_stats": [vm.to_dict() for vm in self.vms],
            "task_stats": [task.to_dict() for task in self.completed_tasks]
        }

    def __repr__(self):
        return f"<CloudEnvironment Time: {self.time} | Waiting Tasks: {len(self.waiting_tasks)} | VMs: {len(self.vms)}>"