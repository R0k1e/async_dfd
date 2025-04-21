import pytest
from gevent import sleep
from gevent.queue import Queue
from async_dfd.node import Node
from async_dfd.node_group import Pipeline

class SimplePipeline(Pipeline):
    def _connect_nodes(self):
        # 简单地将所有节点按顺序连接
        for i in range(len(self.all_nodes) - 1):
            self.all_nodes[i].connect(self.all_nodes[i + 1])

def test_pipeline_with_external_queue():
    """测试Pipeline连接外部队列的功能"""
    # 创建两个处理节点
    node1 = Node(lambda x: x + 1)
    node2 = Node(lambda x: x * 2)
    
    # 创建pipeline
    pipeline = SimplePipeline([node1, node2])
    
    # 创建外部队列
    external_queue = Queue()
    pipeline.connect(external_queue)
    
    # 启动pipeline
    pipeline.start()
    
    # 输入测试数据
    test_data = [1, 2, 3]
    for x in test_data:
        pipeline.put(x)
    
    # 等待处理完成
    pipeline.end()
    
    # 验证结果
    results = []
    while not external_queue.empty():
        results.append(external_queue.get())
    
    # 检查结果是否正确
    assert sorted(results) == [4, 6, 8]  # (1+1)*2=4, (2+1)*2=6, (3+1)*2=8


if __name__ == "__main__":
    pytest.main([__file__])
