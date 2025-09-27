import queue
from abc import ABC, abstractmethod

class AbstractQueueStrategy(ABC):
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self._queue = self._create_queue()

    @abstractmethod
    def _create_queue(self):
        pass

    def get(self):
        return self._queue.get()

    def put_nowait(self, item, priority=None, tie_breaker=0):
        self._put_item(item, priority, tie_breaker)

    @abstractmethod
    def _put_item(self, item, priority, tie_breaker):
        pass
    
    def qsize(self):
        return self._queue.qsize()

    def full(self):
        return self._queue.full()
    
    def task_done(self):
        self._queue.task_done()


class PriorityStrategy(AbstractQueueStrategy):
    """Estratégia baseada em Prioridade."""
    def _create_queue(self):
        return queue.PriorityQueue(self.maxsize)

    def _put_item(self, item, priority=10, tie_breaker=0):
        try:
            priority_num = int(priority)
        except (ValueError, TypeError):
            priority_num = 10

        self._queue.put_nowait((priority_num, tie_breaker, item))

    def get(self):
        _priority, _tie_breaker, item = self._queue.get()
        return item