from config import MIGRATION_OVERHEAD_TIME, MIGRATION_ENERGY_COST

class MigrationPolicy:
    def __init__(self):
        pass

    def migrate(self, vms, current_time):
        migrations = 0
        overloaded_vms = [vm for vm in vms if vm.is_overloaded()]
        underloaded_vms = [vm for vm in vms if vm.get_load() == 0]

        for source_vm in overloaded_vms:
            if not source_vm.task_queue:
                continue

            
            task_to_migrate, enqueue_time = source_vm.task_queue.pop(0)
            source_vm.migrate_task(task_to_migrate)

            if underloaded_vms:
                target_vm = underloaded_vms.pop(0)
            else:
                target_vm = min(vms, key=lambda vm: vm.get_load())
            
            target_vm.assign_task(task_to_migrate, current_time + MIGRATION_OVERHEAD_TIME)
            migrations += 1

        return migrations