#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", order_by=City.id, back_populates="state")


if os.environ.get("HBNB_TYPE_STORAGE") == "db":
    @property
    def cities(self):
        """returns the list of City instances"""
        from models import storage
        all_cities = storage.all(City)
        instances = []
        for key, val in all_cities.items():
            if val["state_id"] == self.id:
                instances.append(val)
        return instances
