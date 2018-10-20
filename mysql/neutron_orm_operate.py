# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import socket
import os
import time


def get_local_ip_and_hostname():
    hostname = socket.gethostname()
    hostip = socket.gethostbyname(hostname)
    return (hostname, hostip)


def get_local_mac():
    flag = 0
    mac_addr = ""
    try:
        for line in os.popen("ipconfig /all"):
            if 'Red Hat VirtIO Ethernet Adapter' in line:
                flag = 1
                continue
            if flag == 1:
                mac_addr = line.split(':')[1]
                break
    except:
        print("file/func: vm_handle.py/get_local_mac except.")

    mac_addr = mac_addr.split(' ')[1].split('\n')[0]
    mac_addr = mac_addr.replace('-', ':')
    return mac_addr


def get_tables(link):
    try:
        db_engine = create_engine(link, encoding='utf-8', echo=False)
        Base = automap_base()
        Base.prepare(db_engine, reflect=True)
        tables = Base.classes
    except:
        print("file/func: vm_handle.py/get_tables except.")
        return "", ""

    return db_engine, tables


def query_port_id_baseon_mac(db_engine, tables, local_mac_addr):
    port_id = ""
    try:
        instances = tables.ports
        session = sessionmaker(bind=db_engine)()
        query_device = session.query(instances).filter(instances.mac_address == local_mac_addr).first()
        session.close()

        port_id = query_device.id
    except:
        print("file/func: vm_handle.py/query_port_id_baseon_mac except.")
    return port_id


def query_old_ip_baseon_mac(db_engine, tables, local_mac_addr):
    port_id = ""
    old_ip = ""
    try:
        instances = tables.ports
        session = sessionmaker(bind=db_engine)()
        query_device = session.query(instances).filter(instances.mac_address == local_mac_addr).first()
        port_id = query_device.id

        instances = tables.ipallocations
        query_device = session.query(instances).filter(instances.port_id == port_id).first()
        old_ip = query_device.ip_address

        session.close()
    except:
        print("file/func: vm_handle.py/query_port_id_baseon_mac except.")

    return port_id, old_ip


def update_ip_for_mac(db_engine, tables, port_id, ip_addr, old_ip):
    '''
    更新neutron的ipallocations  ipamallocations表格
    :param db_engine:
    :param tables:
    :param port_id:
    :param ip_addr:
    :return:
    '''
    try:
        instances = tables.ipallocations
        session = sessionmaker(bind=db_engine)()
        port_instances = session.query(instances).filter(instances.port_id == port_id).first()
        port_instances.ip_address = ip_addr
        session.commit()
        session.close()

        instances = tables.ipamallocations
        session = sessionmaker(bind=db_engine)()
        instances = session.query(instances).filter(instances.ip_address == old_ip).first()
        instances.ip_address = ip_addr
        session.commit()
        session.close()
    except:
        print("file/func: vm_handle.py/update_ip_for_mac except.")


host_ip = "172.18.0.33"
link = "mysql+pymysql://{user}:{passwd}@{host}/{db}".format(user="root", passwd="123qwe", host=host_ip, db="neutron")

'''
等待虚拟机获取ip地址：1s 4s 9s
'''
for i in range(3):
    local_name, local_ip = get_local_ip_and_hostname()
    if (local_ip.split('.')[0] == '169' and local_ip.split('.')[1] == '254') or \
            (local_ip.split('.')[0] == '127' and local_ip.split('.')[1] == '0') or \
            local_ip == '':
        sleep_time = (i + 1) * (i + 1)
        time.sleep(sleep_time)
    else:
        break
print('get local_name is:  %s, local_ip is: %s' % (local_name, local_ip))

'''
虚拟机获取mac地址
'''
local_mac_addr = get_local_mac()
if local_mac_addr == "":
    print('dont get  local mac address. exit')
    exit(0)
else:
    print('local mac address is:', local_mac_addr)

'''
根据虚拟机获取mac地址,查询虚拟机端口id,  根据端口id修改ip地址，dashboard上面显示就更新了。
'''
db_engine, tables = get_tables(link)
if db_engine and tables:
    print(local_mac_addr)
    # port_id, old_ip = query_old_ip_baseon_mac(db_engine, tables, "fa:16:3e:5d:24:84")
    port_id, old_ip = query_old_ip_baseon_mac(db_engine, tables, local_mac_addr)
    print('get port id is: %s , old ip address is:%s' % (port_id, old_ip))
    if port_id == "" or old_ip == "":
        print('dont get port_id. exit')
        exit(0)

    update_ip_for_mac(db_engine, tables, port_id, local_ip, old_ip)
    # update_ip_for_mac(db_engine, tables, port_id, '172.16.0.123', old_ip)
else:
    print('mysql connect is except.  exit')
    exit(0)




