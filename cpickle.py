import cPickle

data = range(100)
cPickle.dump(data,open("t.pkl","wb"))

load_data = cPickle.load(open("t.pkl","rb")) 

print (load_data)