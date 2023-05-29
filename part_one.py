# 第一部分: 只考虑随机分配的完全图模型
# 每个.py文件叫模块
import networkx as nx
from matplotlib import pyplot as plt
import time
import pandas as pd
import numpy as np

PERSON_NUM = 100
ROUND_NUM = 1501

# 100个人 初始化每个人100块
fortune = pd.DataFrame({'fortune': [100 for _ in range(PERSON_NUM)]})
fortune.index.name = 'id'
result = pd.DataFrame({'1': [100 for _ in range(PERSON_NUM)]})  # 保存result
fortune.index.name = 'id'


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


def draw_bar_graph(data):
    """
    绘制数据的直方图
    
    data - pd.Series类型 data.name=fortune
    """
    sorted_data = pd.DataFrame(data.sort_values()).reset_index()
    plt.figure(figsize=[10, 6])
    plt.bar(sorted_data.index, sorted_data['fortune'].values, color='gray', alpha=0.8, width=0.9)
    for x, y in enumerate(sorted_data['fortune']):
        plt.text(x, y, int(y), ha='center', va='bottom', rotation=90, fontsize=3)  # 标记金额
        plt.text(x, -1.5, sorted_data['id'][x], ha='center', va='top', fontsize=3)  # 在底部标上id
    plt.ylim([0, 400])
    plt.xlim([-2, 102])
    plt.title('Round %d' % round_id)
    plt.xlabel('ID', labelpad=9)
    plt.ylabel('Fortune')
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    ax = plt.gca()  # 获取当前坐标轴
    ax.axes.xaxis.set_ticks([])  # 取消横轴
    plt.savefig('pic/part_one/round_%d.png' % round_id, dpi=600)  # 保存图片


start_time = time.time()
round_id = 1  # 画图用
for i in range(1, ROUND_NUM):
    fortune['fortune'] = get_next_round(fortune['fortune'])
    round_id = round_id + 1
    if i % 20 == 0:
        result[str(round_id - 1)] = fortune['fortune']
end_time = time.time()
print('模型用时%.3f秒' % (end_time - start_time))

# draw_bar_graph(fortune['fortune'])

result.to_csv('result/part_one_result.csv')
# print('轮次: ', round_id)
