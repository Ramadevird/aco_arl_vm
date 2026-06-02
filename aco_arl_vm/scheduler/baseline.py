import random

class RandomScheduler:
    def schedule(self, task_queue, vm_list, current_time):
        for task in list(task_queue):
            vm = random.choice(vm_list)
            vm.assign_task(task, current_time)
            task.assign_vm(vm.vm_id)
            task_queue.remove(task)

class RoundRobinScheduler:
    def __init__(self):
        self.index = 0

    def schedule(self, task_queue, vm_list, current_time):
        for task in list(task_queue):
            vm = vm_list[self.index % len(vm_list)]
            vm.assign_task(task, current_time)
            task.assign_vm(vm.vm_id)
            task_queue.remove(task)
            self.index += 1

class LPTScheduler:
    def schedule(self, task_queue, vm_list, current_time):
        task_queue.sort(key=lambda t: t.length, reverse=True)
        for task in list(task_queue):
            least_loaded = min(vm_list, key=lambda vm: vm.get_load())
            least_loaded.assign_task(task, current_time)
            task.assign_vm(least_loaded.vm_id)
            task_queue.remove(task)

class IRRScheduler:
    def __init__(self):
        self.index = 0

    def schedule(self, task_queue, vm_list, current_time):
        for task in list(task_queue):
            attempts = 0
            while attempts < len(vm_list):
                vm = vm_list[self.index % len(vm_list)]
                self.index += 1
                if not vm.is_overloaded():
                    vm.assign_task(task, current_time)
                    task.assign_vm(vm.vm_id)
                    task_queue.remove(task)
                    break
                attempts += 1

class FCFSScheduler:
    def schedule(self, task_queue, vm_list, current_time):
        for task in list(task_queue):
            least_loaded = min(vm_list, key=lambda vm: vm.get_load())
            least_loaded.assign_task(task, current_time)
            task.assign_vm(least_loaded.vm_id)
            task_queue.remove(task)
