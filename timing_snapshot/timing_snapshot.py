# -*- coding: UTF-8 -*-
import socket
import time
import json

settings = {
        'hostip': '10.0.0.100',
        'port':10001,
    }

def send_mesg(settings):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((settings['hostip'], settings['port']))
    msg = {"123": "hello"}
    mesg_info = json.dumps(msg).encode('utf-8')  # 将字典转换成字符串
    s.send(mesg_info)
    #time.sleep(1)
    s.close()

send_mesg(settings)