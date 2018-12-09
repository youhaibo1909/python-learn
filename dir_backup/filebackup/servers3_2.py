#-*- coding: UTF-8 -*-
import select
import socket
import os, sys
import Queue
import struct
import json
import hashlib
import platform

settings = {
        'hostip': '0.0.0.0',
        'port':10002,
        'to_dir':'./to_dir'
    }

message_queues = {}
file_head_info_list = {}


def get_head_info(recv_socket):
    head_len_container = recv_socket.recv(4)   
    
def judge_is_new_connect(recv_socket):   
    #print('judge_is_new_connect', recv_socket, file_head_info_list)
    if recv_socket in file_head_info_list:
        return False
    return True

def get_filename(filename):
    filename_dict = {'filename':filename}
    file_head = json.dumps(filename_dict)  # 将字典转换成字符串
    return file_head.encode('utf-8') 
  
def get_filename_len(filename):
    filename_dict = {'filename':filename}
    filename_len = len(json.dumps(filename_dict).encode('utf-8'))  # 将字典转换成字符串
    return filename_len

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

def start_recv_file_server(settings):
    #创建套接字并设置该套接字为非阻塞模式
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(0)
    
    #绑定套接字
    server_address = ( settings['hostip'], settings['port'] )
    print (sys.stderr,'starting up on %s port %s'% server_address)
    server.bind(server_address)
    
    #将该socket变成服务模式
    #backlog等于5，表示内核已经接到了连接请求，但服务器还没有调用accept进行处理的连接个数最大为5
    #这个值不能无限大，因为要在内核中维护连接队列
    server.listen(5)
    
    #初始化读取数据的监听列表,最开始时希望从server这个套接字上读取数据
    inputs = [server]
    
    #初始化写入数据的监听列表，最开始并没有客户端连接进来，所以列表为空
    outputs = []
    
    
    while inputs:
        #print ( sys.stderr,'waiting for the next event....' )
        #调用select监听所有监听列表中的套接字，并将准备好的套接字加入到对应的列表中
        readable,writable,exceptional = select.select(inputs,outputs,inputs)
        '''
                    如果server这个套接字可读，则说明有新链接到来
                    此时在server套接字上调用accept,生成一个与客户端通讯的套接字
                    并将与客户端通讯的套接字加入inputs列表，下一次可以通过select检查连接是否可读
                    然后在发往客户端数据。 select系统调用是用来让我们的程序监视多个文件句柄(file descrīptor)的状态变化的。程序会停在select这里等待，
                    直到被监视的文件句柄有某一个或多个发生了状态改变

                    若可读的套接字不是server套接字,有两种情况:一种是有数据到来，另一种是链接断开
                    如果有数据到来,先接收数据,然后将收到的数据填入往客户端的缓存区中的对应位置，最后
                    将于客户端通讯的套接字加入到写数据的监听列表:
                    如果套接字可读.但没有接收到数据，则说明客户端已经断开。这时需要关闭与客户端连接的套接字
                    进行资源清理
        '''
        for s in readable: 
            if s is server:
                connection,client_address = s.accept()
                connection.setblocking(0)#设置非阻塞
                inputs.append(connection)
                #message_queues[connection] = Queue.Queue()
                print ('--->start connection from: [%s]' % str(client_address) )
            else:
                if judge_is_new_connect(s):
                    head_len_container = s.recv(4)  #接收struct.pack的头长度。
                    if head_len_container:
                        head_info_len = struct.unpack('i', head_len_container)[0]  # 解析出报头的字符串大小
                        while True:
                            head_info = ''
                            try:
                                recv_str = s.recv(head_info_len)  # 接收长度为head_len的报头内容的信息
                                print ('recv file info is:%s' % recv_str)
                            except:
                                #print ('recv file head is err.')
                                continue
                                
                            head_info = head_info + recv_str
                            if head_info_len <= len(head_info):
                                break;
                        head_info = json.loads(head_info.decode('utf-8'))
                        
                        file_head_info_list[s]= head_info
                        #print ('start recv newfile, head_info is:', head_info)
                        
                        if s not in outputs:
                            outputs.append(s)
                            
                        if not os.path.exists(settings['to_dir']):
                            create_dir(settings['to_dir'])
                        
                        
                        adbfilename = head_info['filename'].replace('\\','/')
                        fn = adbfilename.split('/')[-1]
                        pathname = adbfilename.split(fn)[0] 
                        if pathname:
                            create_dir(settings['to_dir']+pathname)
                        #f = open('recv_file.mkv', 'wb')
                        f = open(settings['to_dir']+'/'+pathname+'/'+fn, 'wb')
                        f_myhash = hashlib.md5()
                        f_len = 0
                        f_count = 0
                    else:
                        print (sys.stderr,'closing..',client_address)
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        f.close()
                else:
                    #print ('this is not new connnect...')
                    data = s.recv(1448)
                    if data:
                        #print ('filename is ', json.loads(filename.decode('utf-8'))['filename'] )
                        #接收文件
                        f.write(data)
                        f_myhash.update(data)
                    
                        f_len = f_len + len(data)
                        #print (f_len, head_info['filesize_bytes'], f_len, len(data))
                        if f_len >= head_info['filesize_bytes']: #接收完成
                            recv_md5sum = f_myhash.hexdigest()
                            #print ('recv md5sum is [%s]' % recv_md5sum)
                            #print ('orig md5sum is [%s]' % head_info['md5sum'])
                            if recv_md5sum == head_info['md5sum']: 
                                s.send(struct.pack('i',0)) #当文件传输的md5sum校验对的时候，代表文件传输正确
                                print ('[%s] Receive complete, md5sum is ok.' % (head_info['filename']) )
                            else:
                                s.send(struct.pack('i',1))
                                #print ('is not ok..')
                        else:
                            f_count = f_count+1448
                            if f_count % 1448 == 5:
                                s.send(struct.pack('i',1))
                                #print ('555555555555')
                    else:
                        print ("++>closed.[%s]\n" % str(client_address))
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        f.close()

        #处理可写的套接字
        '''
                    在发送缓冲区中取出响应的数据，发往客户端。
                    如果没有数据需要写，则将套接字从发送队列中移除，select中不再监视
        '''
        for s in writable: 
            print ('send filename to client.')
            if s in file_head_info_list:
                file_head_info_msg = file_head_info_list[s]
                file_head = get_filename(file_head_info_msg['filename'])
                print ('Respond to client requests:  filename[%s].' % file_head_info_msg['filename'])
                s.send(file_head)
                outputs.remove(s)

        #处理异常情况
        for s in exceptional:
            for s in exceptional: 
                print (sys.stderr,'exception condition on' )
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                #del message_queues[s]
            
            
            
start_recv_file_server(settings)

        