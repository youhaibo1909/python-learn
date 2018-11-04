import os

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
            print (pre_dir)
            print (root, dirs)
            file_list.append(os.path.join(pre_dir, file))
    return file_list

adspath_name = os.path.abspath('./to_dir')
print (get_file_name_list(adspath_name))