# -*- coding:utf-8 -*-
import os,sys
import pickle

adspath_name= os.path.abspath('D:\linux')
def file_dir():
    for root, dirs, files in os.walk(adspath_name):
        print(root) #当前目录路径
        print(dirs) #当前路径下所有子目录
        print(files) #当前路径下所有非目录子文件

def file_name(file_dir):
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            pre_dir = root.split(file_dir)[1]  #去除前导目录
            print (pre_dir)
            file_list.append(os.path.join(pre_dir, file))
    return file_list

def save_to_file(filename, file_list):
    #序列化保存到文件
    with open(filename, 'wb') as f:
        pickle.dump(file_list, f)

def read_from_file(filename):
    # 反序列化
    with open(filename, 'rb') as f:
        filename = pickle.load(f)
    return filename


file_list = file_name(adspath_name)
print (len(file_list), file_list)

