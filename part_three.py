import networkx as nx  # 每个.py文件叫模块
import pandas as pd
import part_two

# 人数
PERSON_NUM = 100
ROUND_NUM = 1501

if __name__ == '__main__':
    # 生成一个BA无标度网络, 每次加新节点的时候连四个边
    G = nx.barabasi_albert_graph(100, 4)

    # 设置初始金额
    for node in G:
        G.nodes[node]['fortune'] = 100

    # 保存结果
    result = pd.DataFrame({'1': [100 for _ in range(PERSON_NUM)]})

    for round_id in range(1, ROUND_NUM):
        part_two.next_round(G)
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

    result.to_csv('result/part_three_result.csv')
