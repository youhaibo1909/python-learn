# -*- conding:utf-8 -*-
import os

def test():
    print (os.getcwd())
    content = 'hello'
    
    filename = "testfile.txt"
    
    if os.path.exists(filename) :
        with open(filename) as f:    #设置文件对象
            content = f.read()
    else:
        with open(filename,'w') as f:    #设置文件对象
            f.write('1')
    print(content)
    