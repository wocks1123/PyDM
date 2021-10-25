from asyncio import Queue, QueueEmpty


class BufferQueue(Queue):
    SENTINEL = object()

    def __init__(self, maxsize=0):
        super().__init__(maxsize=maxsize)

    async def __aiter__(self):
        while True:
            item = await self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()

    def __len__(self):
        return self.qsize()

    def close(self):
        self.put(self.SENTINEL)

    # def get_list(self):
    #     return self.queue


class RemovableQueue(Queue):

    def __init__(self, maxsize=0):
        super().__init__(maxsize=maxsize)

    async def remove(self, item):
        while self.empty():
            getter = self._loop.create_future()
            self._getters.append(getter)
            try:
                await getter
            except:
                getter.cancel()  # Just in case getter is not done yet.
                try:
                    # Clean self._getters from canceled getters.
                    self._getters.remove(getter)
                except ValueError:
                    # The getter could be removed from self._getters by a
                    # previous put_nowait call.
                    pass
                if not self.empty() and not getter.cancelled():
                    # We were woken up by put_nowait(), but can't take
                    # the call.  Wake up the next in line.
                    self._wakeup_next(self._getters)
                raise
        return self.get_nowait_item(item)

    def get_nowait_item(self, item):
        """Remove and return an item from the queue.

        Return an item if one is immediately available, else raise QueueEmpty.
        """
        if self.empty():
            raise QueueEmpty
        item = self._remove(item)
        self._wakeup_next(self._putters)
        return item

    def _remove(self, item):
        return self._queue.remove(item)