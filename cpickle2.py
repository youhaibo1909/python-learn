# -*- coding: utf-8 -*-
import cPickle

data = range(100)

#将数据序列化成文件
cPickle.dump(data,open("t.pkl","wb"))
load_data = cPickle.load(open("t.pkl","rb")) 
print (load_data)

#将数据序列化成字符串
data_string = cPickle.dumps(data)
print (data_string)
data = cPickle.loads(data_string)
print (data)
