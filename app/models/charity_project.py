from sqlalchemy import Column, String, Text
from sqlalchemy.orm import validates

from app.core.db import Base
from app.models.base import BaseModel


class CharityProject(BaseModel, Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    @validates('name', 'description')
    def check_min_string_length(self, key: str, value: str):
        if len(value) < 1:
            raise ValueError('Длина должна быть как минимум 1 символ.')
        return value
