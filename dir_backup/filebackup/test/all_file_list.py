# -*- coding:utf-8 -*-
import os,sys
import pickle
import json
import hashlib

transmit_adspath = 'D:/Users/Administrator/eclipse-workspace/nlp/data_handle'



def test_file_dir():
    for root, dirs, files in os.walk(adspath_name):
        print(root) #当前目录路径
        print(dirs) #当前路径下所有子目录
        print(files) #当前路径下所有非目录子文件

def get_file_name_list(file_dir):
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            pre_dir = root.split(file_dir)[1]  #去除前导目录
            #print (pre_dir)
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

def save_to_file_byjson(filename, file_list):
    #序列化保存到文件
    with open(filename, 'w') as f:
        f.write(json.dumps(file_list))
        
def read_from_file_byjson(filename):
    # 反序列化
    with open(filename, 'r') as f:
        filename = json.load(f)
    return filename

def get_file_md5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def get_transmit_status_by_dir(transmit_status_record_info_file, transmit_adspath):
    adspath_name = os.path.abspath(transmit_adspath)
    file_list = get_file_name_list(adspath_name)
    print (len(file_list), file_list)
    
    file_head_info_list = []
    for filename in file_list:
        dict_tmp = {}
        dict_tmp['filename'] =  filename
        dict_tmp['md5sum'] = get_file_md5(adspath_name+'/'+filename)
        dict_tmp['filesize_bytes'] = os.path.getsize(adspath_name+'/'+filename)
        dict_tmp['file_is_already_transmit'] = False
        dict_tmp['file_is_already_update'] = False
        file_head_info_list.append(dict_tmp)
        
    #save_to_file('save.log', file_head_info_list)
    save_to_file_byjson(transmit_status_record_info_file, file_head_info_list)
    #read_from_file_byjson('save_json.log') 


def create_dir(path):
 # 去除首位空格
    path=path.strip()
    path=path.rstrip("/")
    if not os.path.exists(path):
        os.makedirs(path) 
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False
    
to_dir = 'to_dir'
if not os.path.exists(to_dir):
    create_dir(to_dir)
    
transmit_status_filename = 'transmit_status_file.record'
get_transmit_status_by_dir(transmit_status_filename, transmit_adspath)
file_info = read_from_file_byjson(transmit_status_filename)
print (file_info)
for i in file_info:
    fn = i['filename'].split('\\')[-1]
    pathname = i['filename'].split(fn)[0]  
    pathname = pathname.replace('\\','/')
    if pathname:
        create_dir(to_dir+pathname)
     
     
    print (fn, pathname)
    f = open(to_dir+'/'+pathname+'/'+fn,'w')
    f.close()
    