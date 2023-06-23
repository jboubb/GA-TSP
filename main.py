import numpy as np
import config as conf
import random
import config as conf
from ga import Ga
import matplotlib.pyplot as plt
import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from config import print_config
import config as conf

from ga import *
city_dist_mat = None

config = conf.get_config()




# 8、用遗传算法求解TSP问题
# （1）编程实现遗传算法，允许用户自定义算法参数； 11111111
# （2）要求用可视化界面演示算法执行过程，设置一个演示速度参数，以使演示进度可控；11111
# （3）提供自定义TSP问题的接口。 111111111


config = conf.get_config()
# 添加图例
plt.legend(labels=['频次'])


def build_dist_mat(input_list):
    # 检查input_list类型,确保支持索引访问
    if isinstance(input_list, dict) or isinstance(input_list, np.ndarray):
        pass
    else:
        print('输入数据类型不支持,请检查input_list!')
        exit()

    # 获取input_list大小,而不是直接使用city_num
    n = input_list.shape[0]

    # 检查城市数量是否过大
    if n > 500:
        print('城市数量过大,内存可能不足,请减小城市数量!')
        exit()

    dist_mat = np.zeros([n, n])

    for i in range(n):
        for j in range(i + 1, n):
            # 添加索引检查
            if i >= n or j >= n:
                print('索引越界,退出程序!')
                exit()

            # 访问元素
            d = input_list[i, :] - input_list[j, :]
            dist_mat[i, j] = np.dot(d, d)
            dist_mat[j, i] = dist_mat[i, j]

    return dist_mat


#city_num=config.city_num

display_interval = 100
pause_time=1





# 坐标选择方式:
#   1 - 随机坐标
#   2 - 中国省会城市坐标
#   3 - 读取txt文件
# 询问用户选择坐标方式

loc_type_dict = {1: '随机坐标', 2: '省会城市坐标', 3: '文件读取'}

loc_type = int(input('选择坐标方式(1-随机坐标,2-省会城市坐标,3-读取txt文件):'))
while loc_type not in loc_type_dict:
    print('输入错误,请重新选择坐标方式!')
    loc_type = int(input('选择坐标方式(1-随机坐标,2-省会城市坐标,3-读取txt文件):'))

print('你选择了%s方式' % loc_type_dict[loc_type])

# 提示用户是否自定义参数
customize = input('是否需要自定义参数?'
                  '\n以下参数可自定义:'
                  '\n城市数量\n个体数量 \n迭代代数\n变异概率\n交叉概率\n显示间隔\n暂停时间\n(y/n): ')
while customize not in ['y', 'n']:
    print('输入有误,请重新输入!')
    customize = input('是否需要自定义参数?(y/n): ')
# 如果需要自定义参数,读取用户输入的参数
if customize == 'y':
    config.city_num = int(input('请输入新的城市数量: '))
    print('坐标维度:2(此参数不可修改)')
    config.individual_num = int(input('请输入新的个体数量: '))
    config.gen_num = int(input('请输入新的迭代代数: '))
    config.mutate_prob = float(input('请输入新的变异概率(0~1): '))
    config.cross_prob = float(input('请输入新的交叉概率(0~1): '))
    display_interval = int(input('请输入新的显示间隔(代): '))
    pause_time = float(input('请输入暂停时间（秒）: '))
# 否则使用默认参数
elif customize == 'n':
    # 打印默认参数
    print_config()

if loc_type == 1:  # 随机坐标
    pos_list = np.random.rand(config.city_num, config.pos_dimension)
    config.city_num = pos_list.shape[0]
    print(pos_list)
    print('城市数目:', config.city_num)
elif loc_type == 2:  # 中国省会城市坐标
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

elif loc_type == 3:
    with open('city_info.txt',encoding='utf-8') as f:
        city_dict = json.loads(f.read())

    city_pos_list = []
    for city in city_dict.keys():   # 使用city_dict
        city_pos_list.append(city_dict[city])
    pos_list = np.array(city_pos_list)







# 计算距离矩阵
dist_mat = build_dist_mat(pos_list)



# 运行GA
ga = Ga(dist_mat)
result_list, fitness_list = ga.train()

# 取出最后一代路径
result = result_list[-1]
# 将result转换为一维列表
path = [i for i in result]
# 取出路径坐标
size = len(pos_list)
path = [i for i in range(size)]  # 使用范围内的索引

# 打印最后一代最优适应度
print('最后一代最优适应度:', fitness_list[-1])

result_pos_list = pos_list[path]
# 1. 用len()函数确认pos_list的实际元素个数,控制所有索引在该范围内;
# 2. 不要使用随意的硬编码索引值,而是根据pos_list的大小动态计算;
# 3. 可以使用遍历或切片的方式访问pos_list的元素,避免直接使用索引。
# 4. 如果使用索引,一定要确保索引值在pos_list的合法范围内。
# 要解决各种索引越界异常,关键是要清楚所有变量或数据结构的实际大小,以及Python中索引、切片等的工作方式。任何超出范围的索引操作都会导致IndexError。

#绘图
#多绘制了一张图片

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi']
plt.rcParams['axes.unicode_minus'] = False

# 绘制动态演化过程

idx = 0
done_draw = False
need_redraw = True

for idx, result in enumerate(result_list):
    if need_redraw and idx % display_interval == 0:

        if idx == len(result_list) - 1:
            done_draw = True
            last_total_length = get_total_length(result)

            # 绘制最后一代结果
            plt.title(u"最后一代路径(第%d代),总长度:%.2f," %
                      (len(result_list), last_total_length))

            # 取出每代最优路径坐标并绘制
        x = []
        y = []
        for i in range(config.city_num):
            x.append(pos_list[result[i % config.city_num]][0])
            y.append(pos_list[result[i % config.city_num]][1])

        # 绘制路径线条
        plt.plot(x, y, '-b')

        # 相连首尾元素
        plt.plot([x[-1], x[0]], [y[-1], y[0]], '-b')

        # 绘制城市点
        plt.plot(x, y, 'ob', markersize=8)

        # 显示当前迭代代数

        plt.title('第%d代' % idx)  # 使用idx而不是i

        plt.pause(pause_time)

        # 除最后一代外,其他代数绘制后清除
        if idx != len(result_list) - 1:
            plt.cla()
            plt.title('')

        need_redraw = False

    else:
        need_redraw = True

plt.show()
# # 设置图片比例
#plt.figure(figsize=(16,9))
#figsize=(25, 9)
#fig = plt.figure(figsize=(16, 9), dpi=100)



# 取第一代路径
first_result = []
for i in range(len(pos_list)):
    if i not in first_result:
        first_result.append(i)
    if len(first_result) == len(pos_list):
        break
first_result_pos_list = pos_list[first_result, :]

# 创建figure
fig = plt.figure()

# 绘制第一代路径
# 第一代路径图
ax1 = fig.add_subplot(2,2,1)
plt.plot(first_result_pos_list[:, 0], first_result_pos_list[:, 1], 'o-b')

first_total_length = 0
if len(first_result) != config.city_num:
    first_result = []
    for i in range(config.city_num):
        first_result.append(i)

for i in range(config.city_num):
    from_city = first_result[i]
    to_city = first_result[(i + 1) % config.city_num]
    first_total_length += dist_mat[from_city, to_city]

# 添加地点名称
if loc_type == 2:
    for i in range(len(city_dict)):
        plt.text(pos_list[i, 0], pos_list[i, 1],
                 list(city_dict.keys())[i], size=12)
elif loc_type == 3:
    for i in range(len(city_pos_list)):
        plt.text(pos_list[i, 0], pos_list[i, 1],
                 list(city_dict.keys())[i], size=12)

plt.plot(first_result_pos_list[:, 0], first_result_pos_list[:, 1], 'o-b')
plt.title(u"第一代路径,总长度:%.2f" %first_total_length)

# 绘制最终路径
# 取最后代路径
last_result = result_list[-1]

for i in range(len(pos_list)):
    if i not in last_result:
        last_result.append(i)
    if len(last_result) == len(pos_list):
        break
last_result_pos_list = pos_list[last_result, :]
# 绘制最后一代路径
# 最后一代路径图
ax2 = fig.add_subplot(2,2,2)
plt.plot(last_result_pos_list[:, 0], last_result_pos_list[:, 1], 'o-r')

last_total_length = 0
for i in range(config.city_num):
    from_city = last_result[i]
    to_city = last_result[(i + 1) % config.city_num]
    last_total_length += dist_mat[from_city, to_city]

# 添加地点名称
if loc_type == 2:
    for i in range(len(city_dict)):
        plt.text(pos_list[i, 0], pos_list[i, 1],
                 list(city_dict.keys())[i], size=12)
elif loc_type == 3:
    for i in range(len(city_pos_list)):
        plt.text(pos_list[i, 0], pos_list[i, 1],
                 list(city_dict.keys())[i], size=12)

plt.plot(last_result_pos_list[:, 0], last_result_pos_list[:, 1], 'o-r')
plt.title(u"最后一代路径,总长度:%.2f" % last_total_length)
# 绘制最后一代结果
绘制最后一代结果
plt.title(u"最后一代路径（第%d代）,总长度:%.2f," %
          (len(result_list) ,last_total_length))
# 第一代和最后一代路径图
ax3 = fig.add_subplot(2,2,3)
plt.plot(first_result_pos_list[:, 0], first_result_pos_list[:, 1], 'o-b')
plt.plot(last_result_pos_list[:, 0], last_result_pos_list[:, 1], 'o-r')

# 适应度曲线图
ax4 = fig.add_subplot(2,2,4)
plt.plot(fitness_list)
plt.title(u"适应度曲线")


plt.show()  # 显示figure
