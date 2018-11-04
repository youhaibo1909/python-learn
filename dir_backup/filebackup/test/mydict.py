

dicx = {'filename': 'f1', 'filename1': 'f2'}

#print (dicx.has_key('filename'))
print (dicx['filename'])

if 1:
    print ('1 is True')
    
transmit_adspath = 'D:\\Users\\Administrator\\eclipse-workspace\\nlp\\data_handle\\1.txt\\'

print (transmit_adspath.rsplit('\\'))
print (transmit_adspath.rstrip("\\"))

testfile = r"D:\Users\Administrator\eclipse-workspace\nlp\data_handle\mydb\__init__.py"


f = open(testfile, 'rb') 
while True:
    data = f.read(1024)
    if not data:
        print ('data is empty.')
    
    
print ('is over.')