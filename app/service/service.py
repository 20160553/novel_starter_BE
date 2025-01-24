from collections import defaultdict
from functools import wraps
from typing import Any, Generator, Union

from pydantic import BaseModel

from db.models import *
from repositories import Repository
from repositories.base import BaseRepository
from schemas.models import *

service_dict = defaultdict(dict)

def session_exception_handler(func):
    """A decorator to handle exceptions in a session context.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.repository.rollback()
            raise e

    return wrapper


def to_db_model(
    db_model_class: type[Base],
    obj: Union[BaseModel, dict],
) -> Base:
    if isinstance(obj, BaseModel):
        obj = obj.model_dump()
        return db_model_class(**obj)
    elif isinstance(obj, dict):
        return db_model_class(**obj)
    elif isinstance(obj, db_model_class):
        return obj
    elif obj is None:
        return
    else:
        raise ValueError(f"Invalid type for obj: {type(obj)}")

def to_response_model(
    response_model_class: type[BaseModel],
    obj: Union[Base, dict],
) -> BaseModel:
    if isinstance(obj, Base):
        obj_dict = {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
        return response_model_class(**obj_dict)
    elif isinstance(obj, dict):
        return response_model_class.model_validate(obj)
    elif isinstance(obj, response_model_class):
        return obj
    elif obj is None:
        return None
    else:
        raise ValueError(f"Invalid type for obj: {type(obj)}")


def _mark_as_service_function(category):
    def _inner(func):
        global service_helper_functions
        service_dict[category][func.__name__] = func
        return func

    return _inner


class Service:
    def __init__(self, repository: Repository):
        self.repository = repository
    # Common
    @session_exception_handler
    def _add_model(
        self,
        repository: BaseRepository,
        db_model_class: type[Base],
        response_model_class: type[BaseModel],
        model: Union[BaseModel, dict],
    ) -> BaseModel:
        model = to_db_model(db_model_class, model)
        repository.add(model)
        self.repository.commit()
        self.repository.refresh(model)
        return to_response_model(response_model_class, model)

    @session_exception_handler
    def _get_model_list(
        self,
        repository: BaseRepository,
        response_model_class: type[BaseModel],
        conditions: list[tuple[str, str, Any]] = None,
    ) -> list[BaseModel]:
        models = repository.search(conditions) if conditions else repository.get_all()
        return [to_response_model(response_model_class, model) for model in models]

    @session_exception_handler
    def _get_model_by_id(
        self,
        repository: BaseRepository,
        db_model_class: type[Base],
        response_model_class: type[BaseModel],
        model_id: int,
    ) -> BaseModel:
        model = repository.get_by_id(model_id)
        if model is None:
            raise ValueError(f"{db_model_class.__name__} with id {model_id} not found")
        return to_response_model(response_model_class, model)

    @session_exception_handler
    def _delete_model(self, repository: BaseRepository, model_id: int):
        model = repository.get_by_id(model_id)
        if model is None:
            return
        repository.delete(model)
        self.repository.commit()

    @session_exception_handler
    def _update_model(
        self,
        repository: BaseRepository,
        db_model_class: type[Base],
        response_model_class: type[BaseModel],
        update_model_class: type[BaseModel],
        model_id: int,
        model_update: Union[BaseModel, dict],
    ) -> BaseModel:
        model = repository.get_by_id(model_id)
        if model is None:
            raise ValueError(f"{db_model_class.__name__} with id {model_id} not found")

        update_d = {}
        src_model = to_response_model(response_model_class, model)
        model_update = (
            model_update.model_dump(exclude_unset=True)
            if isinstance(model_update, BaseModel)
            else model_update
        )
        for key, value in model_update.items():
            if (
                getattr(src_model, key) != value
                and update_model_class.model_fields[key].default != value
            ):
                update_d[key] = value

        repository.update(model, **update_d)
        self.repository.commit()
        self.repository.refresh(model)
        return to_response_model(response_model_class, model)

    # User Service
    @_mark_as_service_function(category="User")
    def add_user(self, user: Union[UserCreate, dict]) -> UserResponse:
        return self._add_model(self.repository.users, User, UserResponse, user)

    @_mark_as_service_function(category="User")
    def get_user_list(
        self,
        id: Union[int, list, None] = None,
        username: Union[str, list, None] = None,
        is_active: Union[bool, list, None] = None,
    ) -> list[UserResponse]:
        conditions = []
        if id:
            conditions.append(("id", "in", id if isinstance(id, list) else [id]))
        if username:
            conditions.append(("username", "in", username if isinstance(username, list) else [username]))
        if is_active:
            conditions.append(
                ("is_active", "in", is_active if isinstance(is_active, list) else [is_active])
            )
        return self._get_model_list(self.repository.users, UserResponse, conditions)

    @_mark_as_service_function(category="User")
    def get_user_by_id(self, id: int) -> UserResponse:
        return self._get_model_by_id(self.repository.users, User, UserResponse, id)

    @_mark_as_service_function(category="User")
    def delete_user(self, id: int) -> None:
        return self._delete_model(self.repository.users, id)

    @_mark_as_service_function(category="User")
    def update_user(self, id: int, update: Union[UserUpdate, dict]) -> UserResponse:
        return self._update_model(self.repository.users, User, UserResponse, UserUpdate, id, update)
    
    @_mark_as_service_function(category="User")
    def get_user_by_username(self, username: str) -> list[UserResponse]:
        conditions = []
        conditions.append(("username", "eq", username))
        return self._get_model_list(self.repository.users, UserResponse, conditions)
    
    @_mark_as_service_function(category="Login")
    def login(self, user: Union[UserCreate, dict]) -> UserResponse:
        result = self.repository.users.login(user)
        
        if result==None:
            return None
        else:
            return to_response_model(UserResponse, result)
        
