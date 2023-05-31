# part_two: simple allocation in random network
import networkx as nx  # 每个.py文件叫模块
import pandas as pd
import numpy as np

# 人数和轮次
PERSON_NUM = 100
ROUND_NUM = 1501


# 获取下一轮的函数
def next_round(graph):
    """
    get result of next round, change on input graph.
    :param graph: input graph
    :return: None
    """
    for pid in range(0, PERSON_NUM):
        graph.nodes[pid]['fortune'] = graph.nodes[pid]['fortune'] + 0.5
        if graph.nodes[pid]['fortune'] < 1:  # 若金额为0, 则跳过
            continue
        else:  # 从邻接的节点中选择节点进行随机分配
            graph.nodes[pid]['fortune'] = graph.nodes[pid]['fortune'] - 1
            adj_node_list = list(graph[pid])  # 获取邻接的节点列表
            j = np.random.choice(adj_node_list)  # 随机选择一个节点
            graph.nodes[j]['fortune'] = graph.nodes[j]['fortune'] + 1  # 分配


def set_result(rid, input_result, graph):
    if rid % 20 == 0:  # 每20轮次进行记录
        fortune_list = [0 for _ in range(PERSON_NUM)]
        for i in graph.nodes.data('fortune'):
            fortune_list[i[0]] = i[1]
        input_result[str(rid)] = fortune_list
    # 加入节点的度信息
    degree_list = [0 for _ in range(PERSON_NUM)]
    for i in graph.degree:
        degree_list[i[0]] = i[1]
    input_result['degree'] = degree_list


def analyse_wealth_gini_coefficient(input_result, *args):
    """
        分析图的基尼系数
    :param input_result: 输入分配之后的结果
    :param args: 可选, 输入字符串part_n, 将结果写道csv文件中
    :return: 基尼系数(double)
    """
    person_num = len(input_result)
    # 查看财富最多的人占有社会多少财富
    percent_analyse = pd.DataFrame({'degree':input_result['degree'],'fortune':input_result['last_round']}).sort_values(by='fortune', ascending=False).reset_index(names='id')
    total_fortune = percent_analyse.fortune.sum()
    percent_analyse['percentage'] = percent_analyse['fortune'] / total_fortune
    percent_analyse['cumulative_fortune'] = percent_analyse['fortune'].cumsum()
    percent_analyse['cumulative_proportion'] = percent_analyse['cumulative_fortune'] / total_fortune # 求累计占比
    print(percent_analyse)
    print()
    if len(args) != 0:
        percent_analyse.to_csv('result/'+args[0]+'_percent_analyse.csv')
    # 求财富基尼指数 相关链接：https://zh.wikipedia.org/wiki/%E5%9F%BA%E5%B0%BC%E7%B3%BB%E6%95%B0
    gini_analyse = pd.DataFrame({'fortune':input_result['last_round']}).sort_values(by='fortune', ascending=True).reset_index(names='id')
    gini_analyse['cumulative_fortune'] = gini_analyse['fortune'].cumsum()
    gini_coefficient = (person_num * total_fortune - 2*gini_analyse['cumulative_fortune'].sum()) / (person_num * total_fortune)
    return gini_coefficient


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
        set_result(round_id, result, G)

    # result.to_csv('result/part_two_result.csv')
    print(result)
