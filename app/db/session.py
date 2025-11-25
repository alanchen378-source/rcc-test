from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import load_env_config

Base = declarative_base()

def _build_database_url() -> str:
    cfg = load_env_config().get("database", {})
    driver = cfg.get("driver", "postgresql")
    user = cfg.get("user", "")
    password = cfg.get("password", "")
    host = cfg.get("host", "localhost")
    port = cfg.get("port", 5432)
    name = cfg.get("name", "postgres")
    return f"{driver}://{user}:{password}@{host}:{port}/{name}"


db_cfg = load_env_config().get("database", {})
engine = create_engine(
    _build_database_url(), pool_size=db_cfg.get("pool_size", 10), future=True
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
