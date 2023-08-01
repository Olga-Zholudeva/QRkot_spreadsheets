from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt

from app.core.constants import MAX_LENGHT


class CharityProjectBase(BaseModel):
    """Базовый класс схемы"""

    name: str = Field(..., min_length=1, max_length=MAX_LENGHT)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания проекта."""

    pass


class CharityProjectDB(CharityProjectBase):
    """Схема для получения информации о проекте из БД."""

    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: datetime = Field(None)

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления проекта."""

    name: Optional[str] = Field(None, min_length=1, max_length=MAX_LENGHT)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]
