# -*- coding:utf-8 -*-
import hashlib
import os
import datetime

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

filepath=r'D:\Users\Administrator\eclipse-workspace\nlp\mongodb_abstr.zip'

starttime = datetime.datetime.now()
print (getfilemd5(filepath))
endtime = datetime.datetime.now()
print ('运行时间：%ds'%((endtime-starttime).seconds) )


