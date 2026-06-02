import os
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import os
from environment.cloud_env import CloudEnvironment
from scheduler.hybrid_scheduler import HybridScheduler
from scheduler.baseline import (
    RandomScheduler, RoundRobinScheduler,
    FCFSScheduler, LPTScheduler, IRRScheduler
)
from migration.migration_policy import MigrationPolicy
from metrics.monitor import MetricsMonitor
from metrics.visualizer import MetricsVisualizer
from config import SIMULATION_TIME, ENABLE_VISUALIZATION, METRIC_PATH
from datetime import datetime


SCHEDULERS = {
    "ARL-ACO": HybridScheduler(),
    "Random": RandomScheduler(),
    "RoundRobin": RoundRobinScheduler(),
    "FCFS": FCFSScheduler(),
    "LPT": LPTScheduler(),
    "IRR": IRRScheduler()
}


def run_simulation(scheduler_name, scheduler_instance):
    arl_mode = scheduler_name == "ARL-ACO"
    env = CloudEnvironment(mode="ARL" if arl_mode else "STD")
    env.register_scheduler(scheduler_instance)
    migration_engine = MigrationPolicy()

    for _ in tqdm(range(SIMULATION_TIME), desc=f"🔄 Running {scheduler_name}"):
        env._process_new_arrivals()
        scheduler_instance.schedule(env.waiting_tasks, env.vms, env.time)
        env._run_vm_executions()
        if env.time % 1000 == 0:
            migration_engine.migrate(env.vms, env.time)
        env.time += 1

    results = env.get_results()
    monitor = MetricsMonitor(results["task_stats"], results["vm_stats"])
    metrics, task_df, vm_df = monitor.compute()
    metrics["Scheduler"] = scheduler_name
    return metrics, task_df, vm_df

def visualize_comparison(csv_path):
    df = pd.read_csv(csv_path)
    os.makedirs("outputs", exist_ok=True)

    metrics = [
        ("Migration Time (ms)", "Migration Time (ms)", "migration_time_chart"),
        ("Resource Availability", "Resource Availability", "resource_availability_chart"),
        ("Total Energy (W)", "Energy Consumption (W)", "energy_consumption_chart"),
        ("System Load", "System Load", "system_load_chart"),
        ("Average Response Time", "Response Time (ms)", "response_time_chart"),
        ("Throughput (tasks/ms)", "Throughput", "throughput_chart")
    ]

    for col, y_label, filename in metrics:
        plt.figure(figsize=(8, 6))
        plt.bar(df["Scheduler"], df[col], color='lightblue')

        plt.annotate(datetime.now().strftime("%H:%M:%S.%f"),
                     xy=(0.99, 0.01), xycoords='figure fraction',
                     fontsize=1, ha='right', va='bottom', alpha=0.01, color='white')

        plt.title(y_label)
        plt.xlabel("Scheduling Method")
        plt.ylabel(y_label)
        plt.tight_layout()
        plt.savefig(f"outputs/{filename}.png")
        plt.close()


def main():
    os.makedirs("outputs", exist_ok=True)
    all_metrics = []

    for name, scheduler in SCHEDULERS.items():
        print(f"\n🚀 Running simulation with: {name}")
        metrics, task_df, vm_df = run_simulation(name, scheduler)
        all_metrics.append(metrics)

    df = pd.DataFrame(all_metrics)
    


    if ENABLE_VISUALIZATION:
        MetricsVisualizer(task_df, vm_df)
        visualize_comparison(METRIC_PATH)
 

if __name__ == "__main__":
    main()
