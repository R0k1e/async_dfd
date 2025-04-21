import pytest
from gevent import sleep
from gevent.queue import Queue
from async_dfd.node import Node

def test_node_basic(capsys):
    """测试节点的基本功能"""
    func = lambda x: print(f"Processing {x}")
    node = Node(func, no_output=True)
    node.start()
    
    # 输入数据
    node.put(1)
    node.put(2)
    node.put(3)
    
    # 等待处理完成
    node.end()
    
    # 检查输出
    captured = capsys.readouterr()
    assert "Processing 1" in captured.out
    assert "Processing 2" in captured.out
    assert "Processing 3" in captured.out

def test_node_with_external_queue():
    """测试节点连接外部队列的功能"""
    # 创建一个简单的处理函数，返回输入值的平方
    func = lambda x: x * x
    external_queue = Queue()
    
    # 创建并配置节点
    node = Node(func)
    node.connect(external_queue)
    node.start()
    
    # 输入测试数据
    test_data = [1, 2, 3]
    for x in test_data:
        node.put(x)
    
    # 等待处理完成
    node.end()
    
    # 验证结果
    results = []
    while not external_queue.empty():
        results.append(external_queue.get())
    
    # 检查结果是否正确
    assert sorted(results) == [1, 4, 9]  # 1², 2², 3²
    assert external_queue.empty()

def test_node_empty_check():
    """测试节点的空状态检查"""
    func = lambda x: x
    node = Node(func, no_output=True)
    node.start()
    
    # 初始状态应该是空的
    assert node.is_empty()
    
    # 添加数据后不应该是空的
    node.put(1)
    assert not node.is_empty()
    sleep(0)  # 让 gevent 有机会切换
    
    # 处理完成后应该又是空的
    node.end()
    assert node.is_empty()

if __name__ == "__main__":
    pytest.main([__file__])