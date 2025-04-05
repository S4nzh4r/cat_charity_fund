from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Extra, Field, validator

from app.services.constants import CREATE_DATE, CLOSE_DATE


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(CharityProjectBase):

    @validator('*')
    def field_cannot_be_null(cls, value: Union[str, int]):
        if value is None:
            raise ValueError(
                'Поля в запросе не могут быть None!'
            )
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = 0
    fully_invested: bool
    create_date: datetime = Field(..., example=CREATE_DATE)
    close_date: Optional[datetime] = Field(None, example=CLOSE_DATE)

    class Config:
        orm_mode = True
