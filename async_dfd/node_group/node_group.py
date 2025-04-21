import logging
from abc import ABC, abstractmethod

import gevent
from gevent import spawn, sleep
from ..node.abstract_node import AbstractNode

logger = logging.getLogger(__name__)


class NodeGroup(AbstractNode, ABC):
    def __init__(self, all_nodes):
        super().__init__()
        assert len(all_nodes) != 0, f"No node to compose the node group {self.__name__}"
        self.all_nodes = {node.__name__: node for node in all_nodes}
        self.sorted_nodes = self._topological_sort(self.all_nodes)
        self._connect_nodes()
        self._watch_nodes = gevent.spawn(self._watch_nodes)

    @abstractmethod
    def _connect_nodes(self):
        logger.error(
            f"Not implemented the self._connect_nodes method in {self.__name__}"
        )

    def _watch_nodes(self):
        while self.is_start:
            if all([not node.is_start for node in self.all_nodes.values()]):
                self.is_start = False
            gevent.sleep(5)

    def start(self):
        if self.serial_number is None:
            self.serial_number = [0]
        for i, node in enumerate(self.all_nodes.values()):
            node.set_serial_number(self.serial_number + [i])
            node.start()
        self.is_start = True
        logger.info(f"Node Group {self.__name__} has been started")
        return

    def end(self):
        self.is_start = False
        for node in self.sorted_nodes:
            node.end()
        logger.info(f"Node Group {self.__name__} has been ended")

    def halt(self):
        self.is_start = False
        for node in self.sorted_nodes:
            node.halt()
        logger.info(f"Node Group {self.__name__} has been halted")
        return

    def is_empty(self):
        for node in self.sorted_nodes:
            if not node.is_empty():
                return False
        return True
    
    @abstractmethod
    def _topological_sort(self, nodes):
        pass