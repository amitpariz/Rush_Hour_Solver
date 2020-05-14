
import heapq

"""
 Data structures
"""


class Stack:
    """"A container with a last-in-first-out (LIFO) policy."""

    def __init__(self):
        self.list = []

    def push(self, item):
        """"Push 'item' onto the stack"""
        self.list.append(item)

    def pop(self):
        """"Remove the most recently pushed item from the stack and return it"""
        return self.list.pop()

    def is_empty(self):
        """Returns true if the stack is empty"""
        return len(self.list) == 0


class Queue:
    """A container with a first-in-first-out (FIFO) policy."""

    def __init__(self):
        self.list = []

    def push(self, item):
        """Enqueue the 'item' into the queue"""
        self.list.insert(0, item)

    def pop(self):
        """Remove the earliest pushed item in the queue and return it"""
        return self.list.pop()

    def is_empty(self):
        """Returns true if the queue is empty"""
        return len(self.list) == 0


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.

      Note that this PriorityQueue does not allow you to change the priority
      of an item.  However, you may insert the same item multiple times with
      different priorities.
    """

    def __init__(self):
        self.heap = []
        self.init = False

    def push(self, item, priority):
        if not self.init:
            self.init = True
            try:
                item < item
            except:
                item.__class__.__lt__ = lambda x, y: True
        pair = (priority, item)
        heapq.heappush(self.heap, pair)

    def pop(self):
        (priority, item) = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        return len(self.heap) == 0
