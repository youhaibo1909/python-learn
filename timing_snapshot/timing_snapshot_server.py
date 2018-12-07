# -*- coding: UTF-8 -*-

import threading
import time
import socket
import select
import json
import Queue
import signal


class Job(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
        self.settings =  {
                            'hostip': '0.0.0.0',
                            'port': 10001,
                        }
        self.message_queues = {}
        self.message_queues['connection'] = Queue.Queue()
        self.timer = threading.Timer(5.0, self.get_msg_info, ["Hawk"])
        self.timer.start()

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            #print (time.time())
            self.start_recv_file_server(self.settings)

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False

    def get_msg_info(self, msg_info):
        print (msg_info)
        while not self.message_queues['connection'].empty():
            print(self.message_queues['connection'].get())
        self.timer = threading.Timer(2.0, self.get_msg_info, ["Hawk"])
        self.timer.start()


    def start_recv_file_server(self, settings):
        print ('---->start server..')
        # 创建套接字并设置该套接字为非阻塞模式
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.setblocking(0)
        # 绑定套接字
        server_address = (self.settings['hostip'], self.settings['port'])
        server.bind(server_address)
        server.listen(5)

        inputs = [server]
        outputs = []
        while inputs:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for s in readable:
                if s is server:
                    connection, client_address = s.accept()
                    connection.setblocking(0)  # 设置非阻塞
                    inputs.append(connection)
                    print('--->start connection from: [%s]' % str(client_address))
                else:
                    data = s.recv(1024)
                    if data:
                        print ("recv type: %s, content:%s" % (type(data.decode('utf-8')), data.decode('utf-8'))  )
                        data_struct = json.loads( data.decode('utf-8') )
                        self.message_queues['connection'].put(data_struct)
                        print ("all msg info:", )
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
            for s in writable:
                if s in outputs:
                    outputs.remove(s)
                print ("send ok")
                #s.send("ok")
            # 处理异常情况
            for s in exceptional:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()





if __name__ == "__main__":
    '''
    a = Job()
    a.start()
    time.sleep(3)
    a.pause()
    time.sleep(3)
    a.resume()
    time.sleep(3)
    a.pause()
    time.sleep(2)
    a.stop()
    '''
    create_timing_snapshot = Job()
    create_timing_snapshot.start()
    print ('ending')