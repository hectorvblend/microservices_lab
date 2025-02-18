# Import necessary modules and packages
from functools import wraps
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from src.connectors.db_connect import BASE, ENGINE

# Define a class for basic CRUD operations
class BaseCRUD:
    """
    A base class providing basic CRUD operations for SQLAlchemy models.
    To use this as the second parent class, do as follows:
    Example: class MyTable(Base, BaseCRUD)
    Then, these methods can be used along with built-in SQLAlchemy methods.
    A session is created and closed at the end of each method call.
    If exceptions occur, the session is rolled back.
    """

    @staticmethod
    def get_session():
        """Create a session to interact with the database."""
        Session = sessionmaker(bind=ENGINE)
        return Session()

    @classmethod
    def insert_one(cls, **kwargs):
        """
        Insert one record into the table represented by cls.
        Example usage: User.insert_one(id=1, name="rk", age=30)
        """
        session = cls.get_session()
        try:
            instance = cls(**kwargs)
            session.add(instance)
            session.commit()
            return instance
        except IntegrityError as e:
            print(e)
            session.rollback()
            return None
        finally:
            session.close()

    @classmethod
    def insert_many(cls, data):
        """
        Insert multiple records into the table represented by cls.
        Example usage: User.insert_many([{"id":1, "name":"rk", "age":30}, {"id":2, "name":"rk", "age":30}])
        """
        session = cls.get_session()
        try:
            instances = [cls(**item) for item in data]
            session.add_all(instances)
            session.commit()
            return instances
        except IntegrityError:
            session.rollback()
            return None
        finally:
            session.close()

    @classmethod
    def custom_filter(cls, where_dict=None, columns=None, limit=None, offset=None) -> list[dict]:
        """
        Perform a custom filter operation with specified conditions, columns, limit, and offset.
        Example usage: User.custom_filter(where_dict={"id": 2}, columns=["name", "age"], limit=3, offset=1)
        """
        session = cls.get_session()
        try:
            query = session.query(cls)
            if where_dict:
                query = query.filter_by(**where_dict)
            if columns:
                columns_to_select = [getattr(cls, col) for col in columns]
                query = query.with_entities(*columns_to_select)
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            results = query.all()
            if columns:
                data = [dict(zip(columns, result)) for result in results]
            else:
                data = [
                    {column.name: getattr(result, column.name) for column in cls.__table__.columns}
                    for result in results
                ]

            return data
        finally:
            session.close()


    @classmethod
    def get_all_records(cls):
        """
        Retrieve all records with all columns.
        """
        return cls.custom_filter()

    @classmethod
    def check_existence(cls, **kwargs):
        """
        Check the existence of a record based on the provided filter criteria.
        Returns True if the row is available; otherwise, False.
        """
        session = cls.get_session()
        try:
            return session.query(cls).filter_by(**kwargs).first() is not None
        finally:
            session.close()

    @classmethod
    def update_by_filter(cls, filter_criteria: dict, update_values: dict):
        """
        Update rows based on the provided filter criteria and update values.
        Example usage: User.update_by_filter({"id":2}, {"name":"rk3"})
        """
        session = cls.get_session()
        try:
            num_updated = session.query(cls).filter_by(**filter_criteria).update(update_values)
            session.commit()
            return num_updated
        except IntegrityError:
            session.rollback()
            return 0
        finally:
            session.close()

    @classmethod
    def delete_by_filter(cls, filter_criteria):
        """
        Delete rows based on the provided filter criteria.
        Example usage: User.delete_by_filter({"id":3})
        """
        session = cls.get_session()
        try:
            num_deleted = session.query(cls).filter_by(**filter_criteria).delete()
            session.commit()
            return num_deleted
        except IntegrityError:
            session.rollback()
            return 0
        finally:
            session.close()

    def to_dict(self) -> dict:
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

    @classmethod
    def with_session(cls, func):
        """
        A decorator to wrap a function with a session context.
        The decorated function will receive a session as a keyword argument.
        If the function raises an exception, the session will be rolled back.
        If the function returns successfully, the session will be committed.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = cls.get_session()
            try:
                if args and isinstance(args[0], cls):
                    result = func(*args, session=session, **kwargs)
                else:
                    result = func(*args, **kwargs, session=session)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                raise
            finally:
                session.close()
        return wrapper

    @staticmethod
    def __create_all_schemas__():
        '''Create table'''
        BASE.metadata.create_all(ENGINE)