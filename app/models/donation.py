from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.base import BaseModel


class Donation(BaseModel, Base):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
