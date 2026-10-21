from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

password = environ.get("MYSQL_PWD", "yahia")
user = environ.get("MYSQL_USER", "root")
ip = environ.get("MYSQL_HOST", "192.168.1.5")
port = environ.get("MYSQL_PORT", "3306")
db = environ.get("MYSQL_DATABASE", "students1")

environ.setdefault("MYSQL_PWD", password)
environ.setdefault("MYSQL_USER", user)
environ.setdefault("MYSQL_DATABASE", db)
environ.setdefault("MYSQL_HOST", ip)
environ.setdefault("MYSQL_PORT", port)

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{ip}:{port}/{db}",
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db():
    Base.metadata.create_all(bind=engine, checkfirst=True)
