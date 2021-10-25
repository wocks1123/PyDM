from DM.Worker import Worker


class ModuleWrapper:

    def __init__(self):
        self.worker = Worker()
        self.worker.add_work(self.work)

    def work(self, task_id, *args, **kwargs):
        pass

    def run(self):
        self.worker.run()
