from sqlalchemy import Column, String, Text

from app.core.constants import MAX_LENGHT
from app.models.base import CharityProjectDonationBaseModel


class CharityProject(CharityProjectDonationBaseModel):
    """Модель проекта."""

    name = Column(String(MAX_LENGHT), unique=True, nullable=False)
    description = Column(Text, nullable=False)
