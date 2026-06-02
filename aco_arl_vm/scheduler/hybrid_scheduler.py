from scheduler.q_learning import QLearningAgent
from scheduler.aco import AntColonyOptimizer

class HybridScheduler:
    def __init__(self):
        self.rl_agent = QLearningAgent()
        self.aco_agent = AntColonyOptimizer()

    def schedule(self, task_queue, vm_list, current_time):
        if not task_queue:
            return

        for task in list(task_queue):  
            aco_suggestion = self.aco_agent.choose_vm(vm_list)

            
            rl_choice = self.rl_agent.choose_action(task, vm_list)

            
            if task.priority == "High":
                final_vm = rl_choice  
            elif task.priority == "Low":
                final_vm = aco_suggestion  
            else:
                final_vm = aco_suggestion if current_time % 2 == 0 else rl_choice

            
            vm_list[final_vm].assign_task(task, current_time)
            task.assign_vm(final_vm)
            task_queue.remove(task)

            load = vm_list[final_vm].get_load()
            reward = 10 - (load * 2)
            reward = max(-10, min(10, reward))
            self.rl_agent.update_q_value(task, final_vm, reward, vm_list)
            self.aco_agent.update_pheromone(final_vm, reward)

    def debug(self):
        print("\n--- Q-Learning ---")
        self.rl_agent.print_q_table()
        print("--- ACO ---")
        self.aco_agent.print_pheromones()