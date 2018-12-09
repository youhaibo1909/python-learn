#-*- coding: UTF-8 -*-
import socket,struct
import json
import time
import hashlib
import datetime
import sys,os
import pickle
import platform



settings = {
        'hostip': '192.168.0.50',
        'port':10002,
        'from_dir':'D:\\Users\\Administrator\\eclipse-workspace\\nlp\\data_handle', #windows path
        #'from_dir':'G:\\iso\\centos',
        #'from_dir':'/root/linux_socket/filebackup/from_dir', #linux path
        'transmit_record':'transmit_status_file.record'
    }

def get_os_type():
    sysstr = platform.system()
    if(sysstr =="Windows"):
        return 'Windows'
    elif(sysstr == "Linux"):
        return 'Linux'
    else:
        return 'Other'

def getfilemd5(filename):
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

def test_getfilemd5():
    filepath=r'D:\Users\Administrator\eclipse-workspace\nlp\mongodb_abstr.zip'
    starttime = datetime.datetime.now()
    print (getfilemd5(filepath))
    endtime = datetime.datetime.now()
    print ('运行时间：%ds'%((endtime-starttime).seconds) )
    

def get_head_info(current_file_info, settings):
    filename = current_file_info['filename']
    if get_os_type() == 'Windows':
        settings['from_dir'] = settings['from_dir'].rstrip("\\")  #去除末尾的\\
        file_abs_path = settings['from_dir'] + '\\' + filename
    else:
        settings['from_dir'] = settings['from_dir'].rstrip("/")  #去除末尾的\\
        file_abs_path = settings['from_dir'] + '/' + filename
        
    filesize_bytes = os.path.getsize(file_abs_path) # 得到文件的大小,字节
    #print (filesize_bytes)
    head = {
        'filename': filename,
        'filesize_bytes': filesize_bytes,
        'md5sum':current_file_info['md5sum']
    }
    head_info = json.dumps(head)  # 将字典转换成字符串
    head_info_len = struct.pack('i', len(head_info)) #  将字符串的长度打包
    return head_info, head_info_len

def get_filename_len(filename):
    filename_info = json.dumps({'filename': filename})
    filename_len = len(filename_info)
    #print (filename_info ,filename_len)
    return filename_len

def get_file_size(send_filename, settings):
    if get_os_type() == 'Windows':
        settings['from_dir'] = settings['from_dir'].rstrip("\\")  #去除末尾的\\
        file_abs_path = settings['from_dir'] + '\\' + send_filename
    else:
        settings['from_dir'] = settings['from_dir'].rstrip("/")  #去除末尾的\\
        file_abs_path = settings['from_dir'] + '/' + send_filename
    return os.path.getsize(file_abs_path) # 得到文件的大小,字节


def judge_file_exist(send_filename, settings):
    if get_os_type() == 'Windows':
        settings['from_dir'] = settings['from_dir'].rstrip("\\")  #去除末尾的\\
        file_abs_path = settings['from_dir'] + '\\' + send_filename
    else:
        settings['from_dir'] = settings['from_dir'].rstrip("/")  #去除末尾的\\
        file_abs_path = settings['from_dir'] + '/' + send_filename
    return  os.path.exists(file_abs_path)
       
def send_file(current_file_info, settings):
    
    ret = 0
    send_filename = current_file_info['filename']
    if not judge_file_exist(send_filename, settings): #文件不存在立即返回
        return 1
    
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    
    s.connect(( settings['hostip'], settings['port'] ))
    
    head_info, head_info_len = get_head_info(current_file_info, settings)
    s.send(head_info_len)  # 发送head_info的长度
    s.send(head_info.encode('utf-8'))  #发送头信息先dumps，然后encode
    
    filename_len = get_filename_len(send_filename)
    recv_filename = s.recv(filename_len)
    recv_head_info = json.loads(recv_filename.decode('utf-8'))
    if recv_head_info['filename'] != send_filename:
        return 2
    #print ('recv filename is:', recv_head_info, type(recv_head_info))   
    print('-->start--->:')
    filesize_bytes = get_file_size(send_filename, settings) # 得到文件的大小,字节
    head_info_len = filesize_bytes
    
    if get_os_type() == 'Windows':
        settings['from_dir'] = settings['from_dir'].rstrip("\\")  #去除末尾的\\
        file_abs_path = settings['from_dir'] + '\\' + send_filename
    else:
        settings['from_dir'] = settings['from_dir'].rstrip("/")  #去除末尾的\\
        file_abs_path = settings['from_dir'] + '/' + send_filename 
    f = open(file_abs_path, 'rb') 
    f_count = 0
    while True:
        data = f.read(1448)
        if not data: #如果文件为空的情况
            break
        send_len = s.send(data)
    
        f_count = f_count+send_len
        if f_count %  send_len == 5:#每隔5此接收一次返回值
            server_ret_value = s.recv(4)
            #print ('recv-->->1', f_count)
       
        head_info_len = head_info_len - send_len 
        if head_info_len <= 0:
            #if f_count %  5 != 0:
            #print ('recv-->->2', f_count)
            server_ret_value = s.recv(4)  #最后一次接收
            server_ret_value = struct.unpack('i', server_ret_value)[0] 
            #print ('::::',server_ret_value)
            if server_ret_value == 0:
                ret = 0
            else:
                ret = 3
            break;
    s.close()
    return ret


def test_file_dir():
    for root, dirs, files in os.walk(adspath_name):
        print(root) #当前目录路径
        print(dirs) #当前路径下所有子目录
        print(files) #当前路径下所有非目录子文件

def get_file_name_list(adspath_dir):
    '''
        describe:获取相对路径： 相对adspath_dir路径+文件名称
        para：
            adspath_dir： 需要备份的绝对目录
        return:
                            返回相对路径列表（ 相对adspath_dir路径+文件名称）
    '''
    file_list = []
    for root, dirs, files in os.walk(adspath_dir):
        for file in files:
            pre_dir = root.split(adspath_dir)[1]  #去除前导目录
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

def save_to_file_byjson(filename, file_info_list):
    #序列化保存到文件
    with open(filename, 'w') as f:
        f.write(json.dumps(file_info_list))
        
def read_from_file_byjson(filename):
    # 反序列化
    with open(filename, 'r') as f:
        file_info_list = json.load(f)
    return file_info_list  #[{},{},{},...]

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

def get_transmit_status_by_dir(settings):
    adspath_name = os.path.abspath(settings['from_dir'])
    file_list = get_file_name_list(adspath_name)
    #print (len(file_list), file_list)  #需要拷贝的所有的文件的长度，以及文件名称列表
    
    file_head_info_list = []
    for filename in file_list:
        dict_tmp = {}
        dict_tmp['filename'] =  filename
        if get_os_type() == 'Windows':
            dict_tmp['md5sum'] = get_file_md5(adspath_name+'\\'+filename)
            dict_tmp['filesize_bytes'] = os.path.getsize(adspath_name+'\\'+filename)
        else:
            dict_tmp['md5sum'] = get_file_md5(adspath_name+'/'+filename)
            dict_tmp['filesize_bytes'] = os.path.getsize(adspath_name+'/'+filename)

        dict_tmp['file_is_already_transmit'] = False
        dict_tmp['file_is_already_update'] = False
        file_head_info_list.append(dict_tmp)
       
    return  file_head_info_list
    #save_to_file('save.log', file_head_info_list)
    #save_to_file_byjson(settings['transmit_record'], file_head_info_list)
    #read_from_file_byjson('save_json.log') 

def judge_file_already_transmit(current_file_info, transmit_file_info_lists):
    '''
        describe：
                            如果有文件新增。都需要重新传输。
        para：
            current_file_info：实时遍历当前文件夹中的某一个文件 ，是否为新增文件
            transmit_file_info_lists： 已经传输完成的文件 列表。
        return:
            False: 文件没有传输
            True: 文件已经传输
    '''
    if not transmit_file_info_lists:  #transmit_file_info_lists 为空
        return False
    
    for transmit_file_info in transmit_file_info_lists:
        if transmit_file_info['filename'] == current_file_info['filename']:
            if transmit_file_info['md5sum'] == current_file_info['md5sum']:
                return True
    return False

def update_transmit_file_info_lists(current_file_info, transmit_file_info_lists):
    '''
        describe：
                            每传输一个文件，就更新已经传输文件的状态,并写入settings['transmit_record']
                            防止在传输文件中途出现异常情况，导致已经传输的问题未记录。
        para：
            current_file_info：实时遍历当前文件夹中的某一个文件 
            transmit_file_info_lists： 已经传输完成的文件 列表。
    '''    
    flag = 0
    for transmit_file_info in transmit_file_info_lists:
        if transmit_file_info['filename'] == current_file_info['filename']:    
            if transmit_file_info['md5sum'] != current_file_info['md5sum']:
                transmit_file_info['md5sum'] = current_file_info['md5sum']
                transmit_file_info['file_is_already_update'] = True
                transmit_file_info['file_is_already_transmit'] =  True
                break
        flag = flag + 1
    
        
    if flag ==  len(transmit_file_info_lists):     
        current_file_info['file_is_already_transmit'] =  True
        transmit_file_info_lists.append(current_file_info)
                
    #保存已经传输文件的状态
    save_to_file_byjson(settings['transmit_record'], transmit_file_info_lists)        


def main_start():
    current_file_info_lists = get_transmit_status_by_dir(settings)  #遍历备份目录下面的所有文件，记录相关参数
    transmit_file_info_lists = []
    if os.path.exists(settings['transmit_record']):
        transmit_file_info_lists = read_from_file_byjson(settings['transmit_record'])
    #print (current_file_info_lists)
    #print (transmit_file_info_lists)
    for current_file_info in current_file_info_lists:
        if not judge_file_already_transmit(current_file_info, transmit_file_info_lists): #文件没有传输
            #print (current_file_info['filename'])  #为相对路径+文件名称
            fn = current_file_info['filename']
            ret = send_file(current_file_info, settings)  #传输文件
            if ret == 0:
                print ('-->transmission is ok! [%s] , ret is:%d \n'% (fn, ret))
                update_transmit_file_info_lists(current_file_info, transmit_file_info_lists)    
            else:
                print ('++>transmission is not ok![%s] , ret is:%d \n'% (fn, ret))
            
main_start()


