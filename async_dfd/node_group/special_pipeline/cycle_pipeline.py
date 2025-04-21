import logging
from ..pipeline import Pipeline

logger = logging.getLogger(__name__)


class CyclePipeline(Pipeline):

    def __init__(self, all_nodes, tail_node_index=None):
        super().__init__(all_nodes=all_nodes)
        self.tail.connect(self.head)
        if tail_node_index:
            self.tail = all_nodes[tail_node_index]

    def end(self):
        self.wait_for_empty()
        super().end()

    def _topological_sort(self, nodes):
        logger.info(f"Due to the cycle, the topological sort is not applied in {self.__name__}")
        return nodes