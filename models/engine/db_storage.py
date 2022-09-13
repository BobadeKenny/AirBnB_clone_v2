#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """This class manages storage of hbnb models in MySQL"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a new db storage"""
        HBNB_MYSQL_USER = os.environ.get("HBNB_MYSQL_USER", "hbnb_dev")
        HBNB_MYSQL_PWD = os.environ.get("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = os.environ.get("HBNB_MYSQL_HOST", "localhost")
        HBNB_MYSQL_DB = os.environ.get("HBNB_MYSQL_DB", "hbnb_dev_db")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}"
                                      .format(
                                        HBNB_MYSQL_USER,
                                        HBNB_MYSQL_PWD,
                                        HBNB_MYSQL_HOST,
                                        HBNB_MYSQL_DB), pool_pre_ping=True)
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returnsall objects depending of the class name"""
        if cls:
            instances = {}
            for instance in self.__session.query(cls).all():
                key = "{}.{}".format(cls.__name__, instance.id)
                instances[key] = instance
            return instances
        else:
            instances = {}
            for instance in self.__session.query(User, State, City, Amenity,
                                                 Place, Review).all():
                key = "{}.{}".format(instance.__name__, instance.id)
                instances[key] = instance
            return instances

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
