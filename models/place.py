#!/usr/bin/python3
""" Place Module for HBNB project """
# from models.amenity import Amenity
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, String, ForeignKey, Integer, Float, collate
import os
from models.review import Review


place_amenity = Table("association", Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey("places.id"), nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    user = relationship("User", back_populates="places")
    cities = relationship("City", back_populates="places")
    reviews = relationship("Review", back_populates="place")
    amenities = relationship("Amenity",
                             secondary=place_amenity, viewonly=False)

    if os.environ.get("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """returns the list of Reviw instances"""
            from models import storage
            all_reviews = storage.all(Review)
            instances = []
            for key, val in all_reviews.items():
                if val["place_id"] == self.id:
                    instances.append(val)
            return instances

        @property
        def amenities(self):
            """returns the list of Reviw instances"""
            from models import storage
            from models.amenity import Amenity
            all_amenities = storage.all(Amenity)
            instances = []
            for key, val in all_amenities.items():
                if val["id"] in self.amenity_ids:
                    instances.append(val)
            return instances

        @amenities.setter
        def amenities(self, obj):
            if (obj.__name__ == "Amenity"):
                self.amenity_ids.append(obj.id)
