#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2023/09/27 下午8:52
# @Author : shanchangxi
# @File : util_log.py
import time
import logging  # 引入logging模块
from logging import handlers
# from util.util_dir import *

# 第一步，创建一个logger
loggers = logging.getLogger()
loggers.setLevel(logging.INFO)  # Log等级开关

# 第二步，创建一个handler，用于写入日志文件
log_name =  'project_tim_tor.log'
logfile = log_name

time_rotating_file_handler = handlers.TimedRotatingFileHandler(filename=logfile, when='D', encoding='utf-8')
time_rotating_file_handler.setLevel(logging.INFO)  # 输出到file的log等级的开关

# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
time_rotating_file_handler.setFormatter(formatter)

# 第四步，将handler添加到logger里面
loggers.addHandler(time_rotating_file_handler)

# 如果需要同時需要在終端上輸出，定義一個streamHandler
print_handler = logging.StreamHandler()  # 往屏幕上输出
print_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
loggers.addHandler(print_handler)


def Tim_Tor(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        loggers.info(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper





from itertools import product
from multiprocessing import Pool
def Mul_Ess(map_fun,tuple_list):
    with Pool(31) as p:
        P_data = p.map(map_fun, tuple_list)
    return P_data


import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import datetime
cmp_hjnwtx={}

newcolorsNMC = np.array([
    [68,157,237, 255],
    [98,230,234, 255],
    [104,249,82, 255],
    [0,215,46, 255],
    [0,143,27, 255],
    [254,254,63, 255],
    [231,192,48, 255],
    [255,154,41, 255],
    [255,19,27, 255],
    [215,14,21, 255],
    [193,11,18, 255],
    [255,28,236, 255],
    [152,15,177, 255],
    [175,145,237, 255]])/255
cmp_hjnwtx["radar_nmc"] = ListedColormap(newcolorsNMC)

newcolorsNMC = np.array([
    [68,157,237, 255],
    [98,230,234, 255],
    [104,249,82, 255],
    [0,215,46, 255],
    [0,143,27, 255],
    [254,254,63, 255],
    [231,192,48, 255],
    [255,154,41, 255],
    [255,19,27, 255],
    [215,14,21, 255],
    [193,11,18, 255],
    [255,28,236, 255],
    [152,15,177, 255],
    [175,145,237, 255]])/255
cmp_hjnwtx["radar_moc"] = ListedColormap(newcolorsNMC)


newcolorsPRE = np.array([
    [128, 255, 255, 255],
    [35, 182, 254, 255],
    [0, 120, 180, 255],
    [0, 82, 202, 255],
    [0, 16, 220, 255],
    [150, 2, 244, 255],
    [110, 0, 182, 255],
    [77, 0, 130, 255]])/255
cmp_hjnwtx["pre_tqw"] = ListedColormap(newcolorsPRE)

newcolorsWS = np.array([
    [75, 140, 244, 255],
    [0, 89, 235, 255],
    [36, 173, 0, 255],
    [18, 129, 1, 255],
    [3, 64, 4, 255],
    [218, 183, 5, 255],
    [179, 125, 1, 255],
    [155, 70, 16, 255],
    [253, 3, 127, 255],
    [255, 0, 55, 255],
    [233, 0, 3, 255]])/255
cmp_hjnwtx["ws_nmic"] = ListedColormap(newcolorsWS)

import os
def mkDir(path):
    if "." in path:
        os.makedirs(os.path.dirname(path),exist_ok=True)
    else:
        os.makedirs(path, exist_ok=True)

def Radar_Nmc(array_dt,temp = "850"):
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M")
    if len(array_dt.shape)==3:
        for i , img_ch_nel in enumerate(array_dt): 
            plt.imshow(img_ch_nel,vmin=0,vmax=100,cmap=cmp_hjnwtx["radar_nmc"])
            plt.colorbar()
            outpath = f"./radar_nmc/{temp}_{now_str}.png"
            mkDir(outpath)
            plt.savefig(outpath)
            plt.close()
    if len(array_dt.shape)==2:
            plt.imshow(array_dt,vmin=0,vmax=100,cmap=cmp_hjnwtx["radar_nmc"])
            plt.colorbar()
            outpath = f"./radar_nmc/{temp}_{now_str}.png"
            mkDir(outpath)
            plt.savefig(outpath)
            plt.close() 
            