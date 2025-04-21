import logging
from gevent import sleep
from abc import ABC, abstractmethod
from enum import Enum

logger = logging.getLogger(__name__)

class AbstractNode(ABC):
    def __init__(self):
        # different layer of nodes will have different serial number
        # inherited from the parent node group
        self.serial_number = []
        self.__name__ = self.__class__.__name__
        self.head = None
        self.tail = None
        self.is_start = False

    def set_name(self, name):
        self.__name__ = name

    def set_serial_number(self, serial_number):
        self.serial_number = serial_number

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def end(self):
        pass
    
    @abstractmethod
    def halt(self):
        pass
    
    @abstractmethod
    def is_empty(self):
        pass
    
    def wait_for_empty(self):
        while not self.is_empty():
            sleep(0)
        logger.info(f"Node {self.__name__} has finished processing all data")
        return
