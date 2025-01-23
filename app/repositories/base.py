from typing import Any, Generic, List, Optional, Tuple, TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """A generic base repository providing simple CRUD and search operations for a given SQLAlchemy model.

    Attributes:
        db_session (Session): The SQLAlchemy session used to interact with the database.
        model (type[T]): The SQLAlchemy model class this repository manages.
    """

    def __init__(self, db_session: Session, model: type[T]):
        """Initialize the repository with a SQLAlchemy session and a model class.

        Args:
            db_session (Session): A SQLAlchemy Session object.
            model (type[T]): The SQLAlchemy model class this repository will manage.
        """
        self.db_session = db_session
        self.model = model

    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Retrieve an entity by its primary key ID.

        Args:
            entity_id (int): The primary key ID of the entity.

        Returns:
            Optional[T]: The entity instance or None if not found.
        """
        return self.db_session.query(self.model).filter(self.model.id == entity_id).one_or_none()

    def get_all(self) -> List[T]:
        """Retrieve all entities of this model type.

        Returns:
            List[T]: A list of all entity instances.
        """
        return self.db_session.query(self.model).all()

    def add(self, entity: T):
        """Add a new entity to the database.

        Args:
            entity (T): The entity instance to add.
        """
        self.db_session.add(entity)

    def delete(self, entity: T) -> None:
        """Delete an entity from the database.

        Args:
            entity (T): The entity instance to delete.
        """
        self.db_session.delete(entity)

    def search(self, conditions: List[Tuple[str, str, Any]]) -> List[T]:
        """
        Search for entities based on a list of conditions.

        Args:
            conditions (List[Tuple[str, str, Any]]): A list of conditions where each
                condition is a tuple of (field_name, operator, value).

                - field_name (str): The attribute on the model to filter by.
                - operator (str): The comparison operator ("eq", "in", "gt", "lt", "gte", "lte", "like").
                - value (Any): The value to compare against.

        Returns:
            List[T]: A list of entities that match all given conditions.

        Raises:
            ValueError: If a provided field does not exist on the model or an unsupported operator is used.
        """
        q = self.db_session.query(self.model)

        for field_name, op, val in conditions:
            # Check that the field exists on the model
            if not hasattr(self.model, field_name):
                raise ValueError(
                    f"Field '{field_name}' does not exist on the model '{self.model.__name__}'."
                )

            field = getattr(self.model, field_name)

            # Apply the filter based on the operator
            if op == "eq":
                q = q.filter(field == val)
            elif op == "in":
                if not isinstance(val, (list, tuple, set)):
                    raise ValueError("For 'in' operator, the value must be an iterable.")
                q = q.filter(field.in_(val))
            elif op == "gt":
                q = q.filter(field > val)
            elif op == "lt":
                q = q.filter(field < val)
            elif op == "gte":
                q = q.filter(field >= val)
            elif op == "lte":
                q = q.filter(field <= val)
            elif op == "like":
                # Assuming val is a string pattern, e.g. '%lee%'
                q = q.filter(field.like(val))
            else:
                raise ValueError(f"Unsupported operator '{op}'.")

        return q.all()

    def update(self, entity: T, **fields):
        """Update specific fields on an entity.

        Args:
            entity (T): The entity instance to update.
            **fields: Field-value pairs to update on the entity.

        Raises:
            ValueError: If a field does not exist on the model.
        """
        for key, value in fields.items():
            if not hasattr(entity, key):
                raise ValueError(
                    f"Field '{key}' does not exist on '{self.model.__name__}' entities."
                )
            setattr(entity, key, value)