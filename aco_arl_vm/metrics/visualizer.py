import matplotlib.pyplot as plt
class MetricsVisualizer:
    def __init__(self, task_df, vm_df):
        self.task_df = task_df
        self.vm_df = vm_df
        plt.savefig(r"outputs\energy_consumption_chart.png")
        plt.savefig(r"outputs\migration_time_chart.png")
        plt.savefig(r"outputs\resource_availability_chart.png")
        plt.savefig(r"outputs\response_time_chart.png")
        plt.savefig(r"outputs\system_load_chart.png")
        plt.savefig(r"outputs\throughput_chart.png")

    def plot_all(self):
        self.plot_vm_energy(prefetch=False)
        self.plot_vm_load(prefetch=False)
        self.plot_response_time(prefetch=False)
        self.plot_sla_pie(prefetch=False)

    def plot_vm_energy(self, prefetch):
        plt.figure()
        plt.bar(self.vm_df["VM ID"], self.vm_df["Energy"])
        plt.title("Energy Consumption per VM")
        plt.xlabel("VM ID")
        plt.ylabel("Energy")
        plt.grid(True)
        plt.tight_layout()
        if prefetch:
            plt.savefig("outputs/vm_energy.png")
        plt.close()

    def plot_vm_load(self, prefetch):
        plt.figure()
        plt.bar(self.vm_df["VM ID"], self.vm_df["Queue Length"])
        plt.title("VM Queue Load")
        plt.xlabel("VM ID")
        plt.ylabel("Queue Length")
        plt.grid(True)
        plt.tight_layout()
        if prefetch:
            plt.savefig("outputs/vm_load.png")
        plt.close()

    def plot_response_time(self, prefetch):
        plt.figure()
        data = self.task_df["Response Time"].dropna()
        if not data.empty:
            plt.boxplot(data)
            plt.title("Task Response Time")
            plt.ylabel("Time")
            plt.grid(True)
            plt.tight_layout()
            if prefetch:
                plt.savefig("outputs/response_time.png")
        plt.close()

    def plot_sla_pie(self, prefetch):
        plt.figure()
        sla_counts = self.task_df["SLA_Violated"].value_counts()
        labels = ["On Time", "Violated"]
        colors = ["#4CAF50", "#F44336"]
        plt.pie(sla_counts, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)
        plt.title("SLA Compliance")
        plt.tight_layout()
        if prefetch:
            plt.savefig("outputs/sla_compliance.png")
        plt.close()
    
    def plot_throughput_bar(self, scheduler_name, throughput, prefetch=False):
        plt.figure()
        plt.bar([scheduler_name], [throughput], color='lightblue')
        plt.title("Throughput")
        plt.xlabel("Scheduling Method")
        plt.ylabel("Throughput")
        plt.tight_layout()
        if prefetch:
            plt.savefig(f"outputs/{scheduler_name}_throughput.png")
        plt.close()
    
    def plot_migration_time_bar(self, scheduler_name, migration_time, prefetch=False):
        plt.figure()
        plt.bar([scheduler_name], [migration_time], color='lightblue')
        plt.title("Migration Time (ms)")
        plt.xlabel("Scheduling Method")
        plt.ylabel("Migration Time (ms)")
        plt.tight_layout()
        if prefetch:
            plt.savefig(f"outputs/{scheduler_name}_migration_time.png")
        plt.close()


    def plot_resource_availability_bar(self, scheduler_name, availability, prefetch=False):
        plt.figure()
        plt.bar([scheduler_name], [availability], color='lightblue')
        plt.title("Resource Availability")
        plt.xlabel("Scheduling Method")
        plt.ylabel("Resource Availability")
        plt.tight_layout()
        if prefetch:
            plt.savefig(f"outputs/{scheduler_name}_resource_availability.png")
        plt.close()