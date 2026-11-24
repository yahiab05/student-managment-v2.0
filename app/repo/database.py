# app/database.py
import time
from typing import Optional
from sqlalchemy import create_engine, URL
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.repo.configs.db_configurer import DBConfig, DBConfigData

Base = declarative_base()

# Lazily initialised globals (nothing runs at import time)
_engine: Optional[Engine] = None
_SessionLocal: Optional[sessionmaker] = None
_configs: Optional[DBConfigData] = None  # Load configs at module import time


def _build_engine(max_attempts: int = 5, delay: float = 2.0) -> Engine:
    last_error: Optional[Exception] = None
    configurer = DBConfig()

    for _ in range(max_attempts):
        try:
            global _configs
            if configurer.check_config_file_exists():
                _configs = configurer.get_configuration()
                print(f"Database configuration loaded from {configurer.path}.")
            else:
                configurer.create_config_file(host="127.0.0.1", password="StrongPassword123!")
                _configs = configurer.get_configuration()
                print(f"Database configuration created and loaded from {configurer.path}.")
                
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
            print(f"Database connection attempt failed: {e}. Retrying in {delay} seconds...")
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

def get_configs() -> DBConfigData:
    global _configs
    if _configs is None:
        init_db()  # Ensure configs are loaded when initializing the engine
    return _configs


def create_db():
    Base.metadata.create_all(bind=get_engine(), checkfirst=True)