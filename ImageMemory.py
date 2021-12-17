from constants import *


class ImageMemory:
    """A class used to store previous images in order to recognize gestures"""

    def __init__(self, memory_size=MEMORY_SIZE):
        assert memory_size > 0
        self.memory = []
        self.memory_size = memory_size

    def add(self, img):
        # If the memory is full, delete the oldest image
        if len(self.memory) >= self.memory_size:
            _ = self.memory.pop(0)
        self.memory.append(img)

    def _get_oldest_image(self):
        """Return the oldest image stored in memory if exists"""
        if len(self.memory) != 0:
            return self.memory[0]
        else:
            return None

    def _get_newest_image(self):
        """Return the newest image stored in memory is exists"""
        if len(self.memory) != 0:
            return self.memory[-1]
        else:
            return None
