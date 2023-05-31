# part_three: simple allocation in BA network
import networkx as nx  # 每个.py文件叫模块
import pandas as pd
import part_two

# 人数和轮次
PERSON_NUM = 100
ROUND_NUM = 1501

if __name__ == '__main__':
    # # 生成一个BA无标度网络, 每次加新节点的时候连四个边
    # G = nx.barabasi_albert_graph(100, 4)
    # nx.write_edgelist(G, 'ba_graph.edges')

    # 读取网络
    G = nx.read_edgelist('ba_graph.edges', nodetype=int)

    # 设置初始金额
    for node in G:
        G.nodes[node]['fortune'] = 100

    # 保存结果
    result = pd.DataFrame({'1': [100 for _ in range(PERSON_NUM)]})

    for round_id in range(1, ROUND_NUM):
        part_two.next_round(G)
        part_two.set_result(round_id, result, G)

    # result.to_csv('result/part_three_result.csv')
    result.rename(columns={'1500': 'last_round'}, inplace=True)
    print("Correlation_coefficient: ", result.degree.corr(result['last_round']))
    print()
    print("Gini_coefficient: ", part_two.analyse_wealth_gini_coefficient(result, "part_three"))
