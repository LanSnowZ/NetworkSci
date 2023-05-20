import networkx as nx  # 每个.py文件叫模块
from matplotlib import pyplot as plt
import time
import pandas as pd
import numpy as np

# 人数
PERSON_NUM = 100

# 生成一个联通率为0.1的随机图
G = nx.gnp_random_graph(100, 0.1)

# 设置初始金额
for node in G:
    G.nodes[node]['fortune'] = 100


# 下一轮分配
def next_round(graph):
    """
    get result of next round.
    :param graph: input graph
    :return: None
    """
    for i in range(0, PERSON_NUM):
        if graph.nodes[i]['fortune'] == 0:  # 若金额为0, 则跳过
            continue
        else:  # 从邻接的节点中选择节点进行随机分配
            graph.nodes[i]['fortune'] = graph.nodes[i]['fortune'] - 1
            adj_node_list = list(graph[i])
            j = np.random.choice(adj_node_list)
            graph.nodes[j]['fortune'] = graph.nodes[j]['fortune'] + 1


round_id = 0
for round_id in range(1, 100):
    next_round(G)

print(G.nodes.data('fortune'))  # 查看节点财富情况
print(G.degree)  #  查看节点度的情况
