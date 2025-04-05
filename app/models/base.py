from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.orm import validates


class BaseModel:
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    @validates('full_amount')
    def check_gt_zero(self, key, value):
        if value <= 0:
            raise ValueError('Поле full_amount должно быть больше 0!')
        return value
