import copy
import numpy as np

# dtype的认识 注意这里('lan',)是ndarray中的一个元素了就
# 使用了自定义 带名称的 dtype后每个元素就会用()括起来, 用元组表示, 如果只有单个元素的话就会多一个逗号以作为元组
student = np.dtype([('name', 'S20')])
a = np.array(['lan', 'ak', 'm4'], dtype=student)
print(a.shape)
print(a)

# 如果写成这样就不会多出逗号, 因为这样是不命名的简单结构
student = np.dtype('S20')
a = np.array(['lan', 'ak', 'm4'], dtype=student)
print(a.shape)
print(a)

# 但是如果有多个域, 不是简单结构, 就必须都命名, 否则会报错
student = np.dtype([('name', 'S20'), ('num', 'i4')])
# student = np.dtype(['S20', 'i4']) 这样是错滴
a = np.array([('lan', 1), ('ak', 2), ('m4', 3)], dtype=student)
print(a.shape)
print(a)

dt = np.dtype([('age', np.int8, (2, 4))])
a = np.array([(((1, 2, 3, 4), (2, 3, 4, 5)),)], dtype=dt)
print(a)
print(a.shape)

a = np.array([['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'y']])
print(a)
