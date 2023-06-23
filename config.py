# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser(description='Configuration file')
arg_lists = []


def add_argument_group(name):
    arg = parser.add_argument_group(name)
    arg_lists.append(arg)
    return arg


# Data
data_arg = add_argument_group('Data')
data_arg.add_argument('--city_num', type=int, default=34, help='city num')  # 城市数量
data_arg.add_argument('--pos_dimension', type=int, default=2, help='city num')  # 坐标维度
data_arg.add_argument('--individual_num', type=int, default=50, help='individual num')  # 个体数
data_arg.add_argument('--gen_num', type=int, default=1500, help='generation num')  # 迭代轮数
data_arg.add_argument('--mutate_prob', type=float, default=0.25, help='probability of mutate')  # 变异概率11111111111
data_arg.add_argument('--cross_prob', type=float, default=0.25, help='probability of crossover')#交叉概率cross_prob1111
# 暂停时间pause_time
data_arg.add_argument('--pause_time', type=float, default=1, help='pause time in seconds between generations')
# 显示间隔display_interval
data_arg.add_argument('--display_interval', type=int, default=100, help='interval of displaying the program')

def get_config():
    config, unparsed = parser.parse_known_args()
    return config


def print_config():
    config = get_config()
    print('\n')
    print('使用默认参数:')
    print('城市数量:%d' % config.city_num)
    print('坐标维度:%d' % config.pos_dimension)
    print('个体数量:%d' % config.individual_num)
    print('迭代代数:%d' % config.gen_num)
    print('变异概率:%.2f' % config.mutate_prob)
    print('交叉概率:%.2f' % config.cross_prob)
    # print('显示间隔（代）:%d' % display_interval)
    # print('暂停时间(秒):%.1f' % pause_time)

