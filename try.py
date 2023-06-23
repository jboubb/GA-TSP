import numpy as np
import config as conf
from ga import Ga
import matplotlib.pyplot as plt
import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from config import print_config
# 8、用遗传算法求解TSP问题
# （1）编程实现遗传算法，允许用户自定义算法参数； 11111111
# （2）要求用可视化界面演示算法执行过程，设置一个演示速度参数，以使演示进度可控；11111
# （3）提供自定义TSP问题的接口。 111111111
#TkAgg是一种支持动画的后端。
#设置了这个后端之后,我们的代码就可以正常工作,不会出现上半部分空白的问题。

config = conf.get_config()
# 添加图例
plt.legend(labels=['频次'])


def build_dist_mat(input_list):
    if isinstance(input_list, dict):
        input_list = list(input_list.values())

    n = config.city_num

    dist_mat = np.zeros([n, n])
    for i in range(len(input_list)):
        for j in range(i + 1, len(input_list)):
        # 首先判断索引是否超出范围
            if i >= input_list.shape[0] or j >= input_list.shape[0]:
                break
            # 访问元素
            d = input_list[i, :] - input_list[j, :]
            dist_mat[i, j] = np.dot(d, d)
            dist_mat[j, i] = dist_mat[i, j]
    return dist_mat

#city_num=config.city_num

city_dict = {
        '山东': [117.000923, 36.675807],
        '河北': [115.48333, 38.03333],
        '吉林': [125.35000, 43.88333],
        '黑龙江': [127.63333, 47.75000],
        '辽宁': [123.38333, 41.80000],
        '内蒙古': [111.670801, 41.818311],
        '新疆': [87.68333, 43.76667],
        '甘肃': [103.73333, 36.03333],
        '宁夏': [106.26667, 37.46667],
        '山西': [112.53333, 37.86667],
        '陕西': [108.95000, 34.26667],
        '河南': [113.65000, 34.76667],
        '安徽': [117.283042, 31.86119],
        '江苏': [119.78333, 32.05000],
        '浙江': [120.20000, 30.26667],
        '福建': [118.30000, 26.08333],
        '广东': [113.23333, 23.16667],
        '江西': [115.90000, 28.68333],
        '海南': [110.35000, 20.01667],
        '广西': [108.320004, 22.82402],
        '贵州': [106.71667, 26.56667],
        '湖南': [113.00000, 28.21667],
        '湖北': [114.298572, 30.584355],
        '四川': [104.06667, 30.66667],
        '云南': [102.73333, 25.05000],
        '西藏': [91.00000, 30.60000],
        '青海': [96.75000, 36.56667],
        '天津': [117.20000, 39.13333],
        '上海': [121.55333, 31.20000],
        '重庆': [106.45000, 29.56667],
        '北京': [116.41667, 39.91667],
        '台湾': [121.30, 25.03],
        '香港': [114.10000, 22.20000],
        '澳门': [113.50000, 22.20000],
    }
city_pos_list = []
for city in city_dict.keys():
    city_pos_list.append(city_dict[city])
pos_list = np.array(city_pos_list)

# 计算距离矩阵
dist_mat = build_dist_mat(pos_list)

threshold = 1085.5

count=0


while True:
    # 运行遗传算法
    ga = Ga(dist_mat)
    result_list, fitness_list = ga.train()
    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['KaiTi']
    plt.rcParams['axes.unicode_minus'] = False
    # 重复运行遗传算法,直到找到路径长度小于阈值的解
    while True:
        # 每100代打印一次迭代次数
        if count % 100 == 0:
            print(f'迭代次数:{count}')
        count += 1
        ga = Ga(dist_mat)
        result_list, fitness_list = ga.train()
        # 取出遗传算法最后一代的路径
        last_result = result_list[-1]
        last_result_pos_list = pos_list[last_result, :]
        # 计算路径长度
        last_total_length = 0
        for i in range(config.city_num):
            from_city = last_result[i]
            to_city = last_result[(i + 1) % config.city_num]
            last_total_length += dist_mat[from_city, to_city]
            # 如果路径长度小于阈值,说明找到了满意解,绘制路径,输出信息,退出循环
        if last_total_length < threshold:
            # 绘制路径,添加城市名称,输出信息
            plt.plot(last_result_pos_list[:, 0], last_result_pos_list[:, 1], 'o-r')
            plt.title(u"路径长度:%d,重复运行次数:%d" % (last_total_length, count))
            for i in range(len(city_dict)):
                plt.text(pos_list[i, 0], pos_list[i, 1], list(city_dict.keys())[i], size=12)
            plt.show()
            break
            # 如果路径长度大于阈值,重复运行遗传算法
    else:
        continue
    # 此方法通过设置阈值和重复遗传算法减小随机性影响,提高结果可靠性,找到较优解。
    # 但阈值设置、重复运行次数会影响效率。算法本身的设计与优化更为关键。











