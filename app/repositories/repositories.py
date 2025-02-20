from db.models import *

from repositories.base import BaseRepository
from schemas.models import UserCreate

class UserRepository(BaseRepository[User]):
    def login(self, user: UserCreate) -> User:
        return (
            self.db_session.query(self.model)
            .filter(
                self.model.username == user.username,
                self.model.password == user.password,
            )
            .one_or_none()
        )

class WorkRepository(BaseRepository[Work]):
    pass
