"""
SQLAlchemy models for database
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from candig_authz_service.orm import Base
from candig_authz_service.orm.custom_types import GUID, JsonArray, TimeStamp


class Authorization(Base):
    """
    SQLAlchemy class representing a table that stores authz information.
    """
    __tablename__ = "authorization"

    user_id = Column(String(100), primary_key=True)
    issuer = Column(String(100))
    username = Column(String(100))
    project = Column(String(100), nullable=False)
    access_level = Column(Integer, nullable=False)
    created = Column(TimeStamp())
