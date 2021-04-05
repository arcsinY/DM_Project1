import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import sys

# 统计标称属性attr各个类别出现频数，返回dict{类别：频数}
def nominal_attr_statistic(data, attr):
    res = {}
    for i in data[attr]:
        if pd.isnull(i):
            continue
        if i in res:
            res[i] += 1
        else:
            res[i] = 1
    return res
    
# 输出一个字典
def print_dict(dict):
    for k,v in dict.items():
        print(k, ": ", v)

# 数值属性的5数描述+缺失值
def quantity_attr_statistic(data, attr):
    arr = data[attr]
    max = arr.max()
    min = arr.min()
    median = arr.median()
    one_fourth = arr.quantile(0.25)
    three_fourth = arr.quantile(0.75)
    miss = 0
    for i in data[attr]:
        if pd.isnull(i):
            miss += 1
    print(attr+'属性的五数描述: max=', max, '  min=',min,'  中位数=', median, 
    '  四分之一分位数=', one_fourth, '  四分之三分位数=', three_fourth)
    print(attr+'属性的缺失值个数=', miss, '\n')
    return (max, min, median, one_fourth, three_fourth, miss)

# 标称属性柱状图绘制
def nominal_barchart(dict, attr, bound = 0):
    key = []
    value = []
    # 找出满足要求的key和value
    key = []
    value = []
    for k,v in dict.items():
        if v >= bound:
            key.append(k)
            value.append(v)
    key = np.array(key)
    value = np.array(value)
    # 绘制图像
    fig, ax = plt.subplots()
    bar_chart = ax.bar(key, value)
    ax.set_title(attr+' bar chart')
    ax.set_ylabel('number')
    ax.set_xlabel(attr)
    plt.xticks(rotation=90)

# 绘制指定属性的盒图
def box_plot(data, attr):
    plt.figure()
    data[attr].plot.box(whis=(0,100))

# 数值属性直方图
def histogram(data, attr):
    plt.figure()
    data[attr].plot.hist(bins=100, rwidth=100)

# 用最高频率替代缺失值
def fill_miss_by_freq(data, attr):
    dict = {}  # 每个数值出现次数
    max_value = 0
    max_freq = 0
    for i in data[attr]:
        if i in dict:
            dict[i] += 1
        else:
            dict[i] = 1
        if dict[i] > max_freq:
            max_value = i
            max_freq = dict[i]
    data[attr].fillna(max_value)

# 计算n1，n2的欧式距离(n1有缺失值，n2没有缺失值)
def compute_dis(data, n1, n2):
    if pd.isnull(data.iloc[n1]['price']):
        return math.sqrt((data.iloc[n1]['points']-data.iloc[n2]['points'])*(data.iloc[n1]['points']-data.iloc[n2]['points']))
    if pd.isnull(data.iloc[n1]['points']):
        return math.sqrt((data.iloc[n1]['price']-data.iloc[n2]['price'])*(data.iloc[n1]['price']-data.iloc[n2]['price']))
    return math.sqrt((data.iloc[n1]['price']-data.iloc[n2]['price'])*(data.iloc[n1]['price']-data.iloc[n2]['price']) + (data.iloc[n1]['points']-data.iloc[n2]['points'])*(data.iloc[n1]['points']-data.iloc[n2]['points']))

# 划分为有缺失值的与没有缺失值的
def partition(data):
    # n是有缺失值的，y是没有的
    n = []
    y = []
    t = False
    for i in range(150930):
        if i % 1000 == 0:
            print(i)
        t = False
        for attr in data.columns.delete(0):
            if pd.isnull(data.iloc[i][str(attr)]):
                n.append(i)
                t = True
                break
        if t == False:
            y.append(i)
    return n, y

# 填充missing
def fill_miss_by_dis(data, n, y):
    for i in n:
        min = 0
        min_dis = sys.maxsize
        for j in y:
            dis = compute_dis(data, i, j)
            if dis < min_dis:
                min_dis = dis
                min = j
        for attr in data.columns.delete(0):
            if pd.isnull(data.iloc[i][str(attr)]):
                data.loc[i:i, (str(attr))] = data.iloc[min][str(attr)]

# 查找指定元素在有序数组中的位置
def rank(arr, val):
    left = 0
    high = len(arr) - 1
    while left <= high:
        mid = (left + high) / 2
        if arr[mid] == val:
            return mid
        if arr[mid] < val:
            left = mid + 1
        else:
            high = mid - 1
    return left


# 缺失属性为miss，与之相关属性为attr
def fill_miss_by_corr(data, attr, miss):
    missing = []
    arr = []
    for i in data[attr]:
        arr.append(i)
    for i in data[miss]:
        if not pd.isnull(i):
            missing.append(i)
    arr.sort()
    missing.sort()
    for i in range(150930):
        if pd.isnull(data.iloc[i][miss]):
            r = rank(arr, data.iloc[i][attr]) / len(arr)
            data.loc[i:i, (str(miss))] = missing[(int)(r*len(missing))]

# 读取数据
data = pd.read_csv('Wine Review\\winemag-data_first150k.csv', sep=',')
country = nominal_attr_statistic(data, 'country')
nominal_barchart(country, 'country', 1000)

designation = nominal_attr_statistic(data, 'designation')
nominal_barchart(designation, 'designation', 1000)

province = nominal_attr_statistic(data, 'province')
nominal_barchart(province, 'province', 1000)

region_1 = nominal_attr_statistic(data, 'region_1')
nominal_barchart(region_1, 'region_1', 1000)

region_2 = nominal_attr_statistic(data, 'region_2')
nominal_barchart(region_2, 'region_2', 1000)

variety = nominal_attr_statistic(data, 'variety')
nominal_barchart(variety, 'variety', 1000)

winery = nominal_attr_statistic(data, 'winery')
nominal_barchart(winery, 'winery', 150)


# 五数描述
price = quantity_attr_statistic(data, 'price')
point = quantity_attr_statistic(data, 'points')

# 数据盒图
box_plot(data, 'price')
box_plot(data, 'points')

# 数据直方图
histogram(data, 'price')
histogram(data, 'points')

# 使用最高频率填补缺失值
fill_miss_by_freq(data, 'price')
fill_miss_by_freq(data, 'region_1')
fill_miss_by_freq(data, 'region_2')
fill_miss_by_freq(data, 'designation')

# 使用相似度填补缺失值
a, b = partition(data)
fill_miss_by_dis(data, a, b)

fill_miss_by_corr(data, 'price', 'points')

plt.show()
