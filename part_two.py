import networkx as nx  # 每个.py文件叫模块
import pandas as pd
import numpy as np

# 人数
PERSON_NUM = 100
ROUND_NUM = 1501


# 获取下一轮的函数
def next_round(graph):
    """
    get result of next round, change on origin graph.
    :param graph: input graph
    :return: None
    """
    for pid in range(0, PERSON_NUM):
        if graph.nodes[pid]['fortune'] == 0:  # 若金额为0, 则跳过
            continue
        else:  # 从邻接的节点中选择节点进行随机分配
            graph.nodes[pid]['fortune'] = graph.nodes[pid]['fortune'] - 1
            adj_node_list = list(graph[pid])  # 获取邻接的节点列表
            j = np.random.choice(adj_node_list)  # 随机选择一个节点
            graph.nodes[j]['fortune'] = graph.nodes[j]['fortune'] + 1  # 分配


if __name__ == '__main__':
    # 生成一个连通率为0.1的随机图
    G = nx.gnp_random_graph(100, 0.1)

    # 设置初始金额
    for node in G:
        G.nodes[node]['fortune'] = 100

    # 保存结果
    result = pd.DataFrame({'1': [100 for _ in range(PERSON_NUM)]})

    # 下一轮分配
    for round_id in range(1, ROUND_NUM):
        next_round(G)
        if round_id % 20 == 0:  # 每20轮次进行记录
            fortune_list = []
            for i in G.nodes.data('fortune'):
                fortune_list.append(i[1])
            result[str(round_id)] = fortune_list
        # 加入节点的度信息
        degree_list = []
        for i in G.degree:
            degree_list.append(i[1])
        result['degree'] = degree_list

    # result.to_csv('result/part_two_result.csv')
    print(result)
