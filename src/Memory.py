from .Landmarks import Landmarks
from etc.constants import *


class Memory:
    """A class used to store previous images data in order to recognize gestures"""

    def __init__(self, memory_size=MEMORY_SIZE):
        assert memory_size > 0
        self.memory = []
        self.memory_size = memory_size

    def add(self, data: Landmarks):
        # If the memory is full, delete the oldest data
        if len(self.memory) >= self.memory_size:
            _ = self.memory.pop(0)
        self.memory.append(data)

    def get_oldest_data(self)-> Landmarks:
        """Return the oldest data stored in memory if exists"""
        if len(self.memory) != 0:
            return self.memory[0]
        else:
            return None

    def get_newest_data(self)-> Landmarks:
        """Return the newest data stored in memory is exists"""
        if len(self.memory) != 0:
            return self.memory[-1]
        else:
            return None
