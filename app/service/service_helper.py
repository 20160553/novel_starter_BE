from functools import wraps

from core.config import Config
from db.models import *
from repositories import (
    Repository,
    SessionLocal,
    get_session,
)
from schemas.models import *
from service.service import Service, service_dict


def _create_service(db_session) -> Service:
    repo = Repository(db_session)
    
    return Service(repo)


def _inject_service_dependency(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_gen = get_session(SessionLocal)
        db_session = next(session_gen)

        service = _create_service(
            db_session
        )
        try:
            return func(service, *args, **kwargs)
        finally:
            session_gen.close()

    return wrapper


for category, services in service_dict.items():
    for service_name, service in services.items():
        service_func = getattr(Service, service_name)
        service_dict[category][service_name] = _inject_service_dependency(service_func)


__all__ = ["service_dict"]