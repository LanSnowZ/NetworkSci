# part_six: 节点钱多的每次分配时拿出来的钱就多 模拟消费因素（也可以说模拟慈善行为）
import networkx as nx  # 每个.py文件叫模块
import numpy as np
import pandas as pd
import part_two

# 人数和轮次
PERSON_NUM = 100
ROUND_NUM = 1501
# 教育因素
EDU_RATE = 2
# 消费率 收入多的节点分配的时候拿出的钱占自己钱的比率
GIVE_RATE = 0.2

def next_round_edu_consume(graph):
    """
    get result of next round, change on input graph, edu factors considered.
    :param graph: input graph
    :return: None
    """
    for pid in range(0, PERSON_NUM):
        if graph.nodes[pid]['fortune'] < 1:  # 若金额为0, 则跳过
            continue
        else:  # 从邻接的节点中选择节点进行随机分配
            give_fortune = graph.nodes[pid]['fortune']*GIVE_RATE
            graph.nodes[pid]['fortune'] = graph.nodes[pid]['fortune'] - give_fortune
            adj_node_list = list(graph[pid])  # 获取邻接的节点列表
            # 这里设置了受教育的节点获得收益的概率为其他节点的2倍
            append_list = []
            for i in adj_node_list:
                if graph.nodes[i]['edu']:
                    for _ in range(EDU_RATE-1):
                        append_list.append(i)
            adj_node_list = adj_node_list + append_list
            j = np.random.choice(adj_node_list)  # 根据概率随机选择一个节点
            graph.nodes[j]['fortune'] = graph.nodes[j]['fortune'] + give_fortune  # 分配


if __name__ == '__main__':
    # 读取无标度网络 设置节点类型为int
    G = nx.read_edgelist('ba_graph.edges', nodetype=int)

    # 保存结果
    result = pd.DataFrame({'1': [100 for _ in range(PERSON_NUM)]})

    # 设置初始金额和教育水平
    for node in G:
        G.nodes[node]['fortune'] = 100
        # 节点的教育为真
        if node >= 90:
            G.nodes[node]['edu'] = True
        else:
            G.nodes[node]['edu'] = False

    for round_id in range(1, ROUND_NUM):
        next_round_edu_consume(G)
        part_two.set_result(round_id, result, G)

    # result.to_csv('result/part_six_result.csv')
    result.rename(columns={'1500': 'last_round'}, inplace=True)
    print("Correlation_coefficient: ", result.degree.corr(result['last_round']))
    print()
    print("Gini_coefficient: ", part_two.analyse_wealth_gini_coefficient(result, "part_six"))
