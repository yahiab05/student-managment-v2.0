from configparser import ConfigParser
from os import environ
from pathlib import Path

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import declarative_base, sessionmaker

class DBConfig:
    def __init__(self):

        config_path = (
            Path(__file__).resolve().parents[2]
            / "config"
            / "db.ini"
        )

        config = ConfigParser()
        if not config.read(config_path):
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        db = config["database"]

        self.host = db["host"]
        self.port = db.getint("port")
        self.name = db["database"]
        self.user = db["user"]
        self.password = db["password"]
        
Base = declarative_base()

while True:
    try:
        settings = DBConfig()

        url = URL.create(
            "mysql+pymysql",
            username=settings.user,
            password=settings.password,
            host=settings.host,
            port=settings.port,
            database=settings.name
        )
        engine = create_engine(url)
        break
    except Exception as e:
        print(e)
        import time
        time.sleep(2)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

def create_db():
    Base.metadata.create_all(bind=engine, checkfirst=True)
