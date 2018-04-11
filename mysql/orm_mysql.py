import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:123qwe@192.168.50.83/neutron", encoding='utf-8', echo=True)
Base = declarative_base()  # 生成orm基类


class User(Base):
    __tablename__ = 'user'  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))

Base.metadata.create_all(engine)  # 创建表结构

def write_line_to_table_user(name, password):
    Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
    Session = Session_class()  # 生成session实例

    user_obj = User(name=name, password=password)  # 生成你要创建的数据对象
    #print(user_obj.name, user_obj.id)  # 此时还没创建对象呢，不信你打印一下id发现还是None

    Session.add(user_obj)  # 把要创建的数据对象添加到这个session里， 一会统一创建
    #print(user_obj.name, user_obj.id)  # 此时也依然还没创建

    Session.commit()  # 现此才统一提交，创建数据


if __name__ == '__main__':
    for i in (range(100)):
        name = 'cheng'+str(i)
        password = 'pwd'+str(i)
        write_line_to_table_user(name, password)
    print("is ok!")
