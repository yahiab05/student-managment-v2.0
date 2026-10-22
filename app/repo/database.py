# app/database.py
import time
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine, URL
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.config import set_host_and_port

Base = declarative_base()

# Lazily initialised globals (nothing runs at import time)
_engine: Optional[Engine] = None
_SessionLocal: Optional[sessionmaker] = None
_configs: Optional[ConfigParser] = None


class DBConfig:
    def __init__(self):
        config_path = (
            Path(__file__).resolve().parents[1]
            / "config"
            / "db.ini"
        )

        config = ConfigParser()
        if not config.read(config_path):
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        db = config["database"]

        self.host, self.port = set_host_and_port()
        if self.host is None or self.port is None:
            raise RuntimeError("Failed to set database host and port.")

        self.name = db["database"]
        self.user = db["user"]
        self.password = db["password"]


def _build_engine(max_attempts: int = 5, delay: float = 2.0) -> Engine:
    last_error: Optional[Exception] = None

    for _ in range(max_attempts):
        try:
            _configs = DBConfig()
            url = URL.create(
                "mysql+pymysql",
                username=_configs.user,
                password=_configs.password,
                host=_configs.host,
                port=_configs.port,
                database=_configs.name,
            )
            engine = create_engine(url, pool_pre_ping=True)

            # create_engine is lazy, so actually verify connectivity
            with engine.connect():
                pass

            return engine
        except Exception as e:
            last_error = e
            time.sleep(delay)

    raise RuntimeError(
        f"Failed to connect to the database after {max_attempts} attempts."
    ) from last_error


def init_db() -> Engine:
    """Create the engine and session factory. Call once at app startup."""
    global _engine, _SessionLocal

    if _engine is None:
        _engine = _build_engine()
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=True, bind=_engine
        )
    return _engine


def get_engine() -> Engine:
    return init_db()


def get_session() -> Session:
    if _SessionLocal is None:
        init_db()
    return _SessionLocal()

def get_configs() -> ConfigParser:
    global _configs
    if _configs is None:
        init_db()  # Ensure configs are loaded when initializing the engine
    return _configs


def create_db():
    Base.metadata.create_all(bind=get_engine(), checkfirst=True)