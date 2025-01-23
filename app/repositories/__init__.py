from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from core.config import Config
from db.models import (
    Base,
    User,
    Work,
)
from repositories.repositories import (
    UserRepository,
    WorkRepository
)

# 데이터베이스 연결 설정 (MySQL 예시)
engine = create_engine(f"mysql+mysqlconnector://{Config.DB_USER}:{Config.DB_PW}@{Config.DB_HOST}/{Config.DB_NAME}")

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session(session_factory=None):
    """
    Provide a transactional scope for a series of operations.
    This ensures the db_session is cleaned up (closed) after use.
    """
    if session_factory is None:
        session_factory = SessionLocal
    db_session = session_factory()
    try:
        yield db_session
    except Exception as e:
        raise e
    finally:
        db_session.close()


class Repository:
    """
    A convenience class that instantiates all repositories for a given db_session.

    Usage:
        with get_session() as db_session:
            repo = Repository(db_session)
            user = repo.users.add(User(name="Alice", email="alice@example.com"))
            # ...
    """

    def __init__(self, db_session):
        self.db_session = db_session
        self.users = UserRepository(db_session, User)
        self.works = WorkRepository(db_session, Work)

    def drop_all(self):
        """
        Drop all tables in the database.
        """
        Base.metadata.drop_all(engine)

    def commit(self):
        """
        Commit the current transaction.
        """
        self.db_session.commit()

    def refresh(self, model):
        """
        Refresh the given model.
        """
        self.db_session.refresh(model)

    def rollback(self):
        """
        Rollback the current transaction.
        """
        self.db_session.rollback()

    def close(self):
        """
        Close the db_session.
        """
        self.db_session.close()