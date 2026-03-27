from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from os import environ

Base = declarative_base()

password = "yahia"
user = "root"
ip = "192.168.1.5"
port = "3306"
db = "students1"

environ["MYSQL_PWD"] = password
environ["MYSQL_USER"] = user
environ["MYSQL_DATABASE"] = db
environ["MYSQL_HOST"] = ip
environ["MYSQL_PORT"] = port

while True:
    try:
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{ip}:{port}/{db}")
        break
    except Exception as e:
        print(e)
        import time
        time.sleep(2)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db():
    Base.metadata.create_all(bind=engine, checkfirst=True)
