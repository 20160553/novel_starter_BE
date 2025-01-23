from db.models import *

from repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    pass
class WorkRepository(BaseRepository[Work]):
    pass