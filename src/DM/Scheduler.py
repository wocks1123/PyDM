from DM.BufferQueue import BufferQueue, RemovableQueue


class Scheduler:

    def __init__(self):
        self.waiting_q = RemovableQueue()
        self.running_q = []

        self.worker_list = []

    async def append(self, worker_name):
        self.worker_list.append(worker_name)
        await self.waiting_q.put(worker_name)

    async def remove(self, worker_name):
        if worker_name in self.running_q:
            self.running_q.remove(worker_name)
        else:
            await self.waiting_q.remove(worker_name)

    async def get_next(self):
        worker_name = await self.waiting_q.get()
        self.running_q.append(worker_name)
        return worker_name

    async def task_done(self, worker_name):
        self.running_q.remove(worker_name)
        await self.waiting_q.put(worker_name)

    def close(self):
        self.waiting_q.join()
