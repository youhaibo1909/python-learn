#-*- coding: UTF-8 -*-
import socket,os,struct
import json
import time

settings = {
        'hostip': '192.168.0.50',
        'port':10001,
    }



def get_head_info(filename):
    filesize_bytes = os.path.getsize(filename) # 得到文件的大小,字节
    #print (filesize_bytes)
    head = {
        'filename': filename,
        'filesize_bytes': filesize_bytes,
    }
    head_info = json.dumps(head)  # 将字典转换成字符串
    head_info_len = struct.pack('i', len(head_info)) #  将字符串的长度打包
    return head_info, head_info_len

def get_filename_len(filename):
    filename_info = json.dumps({'filename': filename})
    filename_len = len(filename_info)
    #print (filename_info ,filename_len)
    return filename_len

def get_file_size(filename):
    return os.path.getsize(filename) # 得到文件的大小,字节

def send_file(send_filename, settings):
    if not os.path.exists(send_filename):
        return 1  #文件不存在
    
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    s.connect(( settings['hostip'], settings['port'] ))
    
    head_info, head_info_len = get_head_info(send_filename)
    s.send(head_info_len)  # 发送head_info的长度
    s.send(head_info.encode('utf-8'))  #发送头信息先dumps，然后encode
    
    filename_len = get_filename_len(send_filename)
    recv_filename = s.recv(filename_len)
    recv_head_info = json.loads(recv_filename.decode('utf-8'))
    if recv_head_info['filename'] != send_filename:
        return 2
    print ('recv filename is:', recv_head_info, type(recv_head_info))   
    
    filesize_bytes = get_file_size(send_filename) # 得到文件的大小,字节
    head_info_len = filesize_bytes
    f = open(send_filename, 'rb') 
    while True:
        data = f.read(1024)
        s.send(data)
        s.recv(4)
        head_info_len = head_info_len - 1024 
        if head_info_len < 0:
            break;
    s.close()
    return 0
       
fn = '0007Python1.mkv' 
ret = send_file(fn, settings)
if ret == 0:
    print ('[%s] transmission is ok!, ret is:%d'% (fn, ret))
else:
    print ('[%s] transmission is not ok!, ret is:%d'% (fn, ret))

