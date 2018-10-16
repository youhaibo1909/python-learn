from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


db_engine = create_engine("mysql+pymysql://root:123qwe@192.168.10.5/nova", encoding='utf-8', echo=False)
# get sqlalchemy tables from database
Base = automap_base()
Base.prepare(db_engine, reflect=True)
tables = Base.classes
instances = tables.instances

session = sessionmaker(bind=db_engine)()
query_device = session.query(instances).filter(instances.id == 1)

print(query_device[0].created_at, query_device[0].vm_mode, query_device[0].os_type)