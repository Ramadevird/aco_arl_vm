import pandas as pd

class MetricsMonitor:
    def __init__(self, task_stats, vm_stats):
        self.task_stats = task_stats
        self.vm_stats = vm_stats

    def compute(self):
        task_df = pd.DataFrame(self.task_stats)
        vm_df = pd.DataFrame(self.vm_stats)

        
        avg_queue = sum(vm["Queue Length"] for vm in self.vm_stats) / len(self.vm_stats)
        system_load = avg_queue
        resource_availability = 1.0 - min(avg_queue / 5.0, 1.0)

        
        task_df["SLA_Violated"] = task_df.apply(
            lambda row: row["End Time"] > row["Deadline"] if pd.notnull(row["End Time"]) else False, axis=1
        )
        task_df["Response Time"] = task_df.apply(
            lambda row: row["End Time"] - row["Arrival Time"] if pd.notnull(row["End Time"]) else None, axis=1
        )

        sla_violations = task_df["SLA_Violated"].sum()
        total_time = task_df["End Time"].max() if not task_df["End Time"].isnull().all() else 0

        metrics = {
            "Total Tasks": len(task_df),
            "Completed Tasks": task_df["Status"].eq("Completed").sum(),
            "Average Response Time": task_df["Response Time"].mean() if not task_df["Response Time"].isnull().all() else 0,
            "SLA Violations": sla_violations,
            "Throughput (tasks/ms)": len(task_df) / total_time if total_time > 0 else 0,
            "Total Energy (W)": vm_df["Energy"].sum(),
            "System Load": system_load,
            "Resource Availability": resource_availability,
            "Migration Time (ms)": 20.0,  
            "Average VM Load": vm_df["Queue Length"].mean(),
            "Max VM Load": vm_df["Queue Length"].max(),
            "Min VM Load": vm_df["Queue Length"].min()
        }

        return metrics, task_df, vm_df

    def print_summary(self, metrics):
        print("\n===== SIMULATION METRICS =====")
        for k, v in metrics.items():
            if isinstance(v, float):
                print(f"{k}: {v:.3f}")
            else:
                print(f"{k}: {v}")
        print("=" * 33)
