import networkx as nx  # 每个.py文件叫模块
from matplotlib import pyplot as plt
import time
import pandas as pd
import numpy as np

PERSON_NUM = 100

# 100个人 初始化每个人100块
fortune = pd.DataFrame({'fortune': [100 for i in range(PERSON_NUM)]})
fortune.index.name = 'id'
round_id = 0


# 分配实验1
def get_next_round(pre_round):
    round_person_num = len(pre_round[pre_round > 0])  # 本轮分配的总金额, 没钱的人不拿钱出来
    this_round = pd.DataFrame({'pre_round': pre_round})  # 本轮分配的结果
    this_round['lost'] = np.where(this_round['pre_round'] > 0, 1, 0)  # 仍然有钱的人拿出一块钱来
    # 进行随机分配
    allocate = pd.Series(np.random.choice(PERSON_NUM, round_person_num))
    gain = pd.DataFrame({'gain': allocate.value_counts()})
    this_round = this_round.join(gain).fillna(0)
    # 返回结果
    return this_round['pre_round'] - this_round['lost'] + this_round['gain']


def draw_column_graph()
    plt.figure(figsize=(10, 6))
    plt.bar(datai.index, datai.values, color='gray', alpha=0.8, width=0.9)
    plt.ylim((0, 400))
    plt.xlim((-10, 110))
    plt.title('Round %d' % n)
    plt.xlabel('PlayerID')
    plt.ylabel('Fortune')
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.savefig('graph2_round_%d.png' % n, dpi=200)

start_time = time.time()
for _ in range(1, 27000):
    fortune['fortune'] = get_next_round(fortune['fortune'])
    round_id = round_id + 1
end_time = time.time()
print('模型用时%.3f秒' % (end_time - start_time))
print(fortune)
print('轮次: ', round_id)
