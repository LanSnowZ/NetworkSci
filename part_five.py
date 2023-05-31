# part_five: 考虑税收因素 每轮收入高的节点收税 发给收入最低的十个节点
import networkx as nx  # 每个.py文件叫模块
import numpy as np
import pandas as pd
import part_two

# 人数和轮次
PERSON_NUM = 100
ROUND_NUM = 1501
# 教育因素
EDU_RATE = 2
# 收税门槛和税率
TEX_THRESHOLD = 3
TEX_RATE = 0.3
POOR_NUM = 10


def next_round_edu_tex(graph, income):
    """
    get result of next round, change on input graph, edu and tex factors considered.
    :param income: income list
    :param graph: input graph
    :return: None
    """
    for pid in range(0, PERSON_NUM):
        if graph.nodes[pid]['fortune'] < 1:  # 若金额小于1, 则跳过
            continue
        else:  # 从邻接的节点中选择节点进行随机分配
            graph.nodes[pid]['fortune'] = graph.nodes[pid]['fortune'] - 1
            adj_node_list = list(graph[pid])  # 获取邻接的节点列表
            # 这里通过增加列表中受教育节点的出现次数 设置了受教育的节点获得收益的概率为其他节点的2倍
            append_list = []
            for i in adj_node_list:
                if graph.nodes[i]['edu']:
                    for _ in range(EDU_RATE - 1):
                        append_list.append(i)
            adj_node_list = adj_node_list + append_list
            j = np.random.choice(adj_node_list)  # 随机选择一个节点
            graph.nodes[j]['fortune'] = graph.nodes[j]['fortune'] + 1  # 分配
            income[j] = income[j] + 1  # 记录每个节点该轮的收入


if __name__ == '__main__':
    # 读取无标度网络 设置节点类型为int
    G = nx.read_edgelist('ba_graph.edges', nodetype=int)

    # 保存结果
    result = pd.DataFrame({'1': [100.0 for _ in range(PERSON_NUM)]})

    # 设置初始金额
    for node in G:
        G.nodes[node]['fortune'] = 100
        # 节点的教育为真
        if node >= 90:
            G.nodes[node]['edu'] = True
        else:
            G.nodes[node]['edu'] = False

    # 分配
    for round_id in range(1, ROUND_NUM):
        round_income = [-1 for _ in range(PERSON_NUM)]
        next_round_edu_tex(G, round_income)
        # 收取税款
        round_tex = 0
        for i in range(PERSON_NUM):
            if round_income[i] >= 3:
                G.nodes[i]['fortune'] = G.nodes[i]['fortune'] - round_income[i] * TEX_RATE
                round_tex = round_tex + round_income[i] * TEX_RATE
        # 发放给最穷的十个人
        tmp_list = [i[1] for i in list(G.nodes.data('fortune'))]
        tmp_df = pd.DataFrame({'fortune': tmp_list})
        poor_list = list(tmp_df.sort_values(by='fortune').index)  # 记录最穷的节点的id
        piece_of_money = round_tex / POOR_NUM  # 每份的金额
        for i in range(POOR_NUM):  # 发放
            G.nodes[poor_list[i]]['fortune'] = G.nodes[poor_list[i]]['fortune'] + piece_of_money
        part_two.set_result(round_id, result, G)

    # result.to_csv('result/part_five_result.csv')
    result.rename(columns={'1500': 'last_round'}, inplace=True)
    print("Correlation_coefficient: ", result.degree.corr(result['last_round']))
    print()
    print("Gini_coefficient: ", part_two.analyse_wealth_gini_coefficient(result, "part_five"))
