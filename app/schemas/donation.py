from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.services.constants import CREATE_DATE, CLOSE_DATE


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationUserDB(DonationBase):
    id: int
    create_date: datetime = Field(..., example=CREATE_DATE)

    class Config:
        orm_mode = True


class DonationAllDB(DonationUserDB):
    user_id: Optional[int]
    invested_amount: int = 0
    fully_invested: bool
    close_date: Optional[datetime] = Field(None, example=CLOSE_DATE)
