# from app.core.db import AsyncSessionLocal
from typing import Dict, List, Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_id_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получаем id существующего проекта из базы данных."""

        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == charity_project_name)
        )
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id

    async def get_charity_project_by_id(
        self,
        charity_project_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        """Получаем проект по id."""

        db_charity_project = await session.execute(
            select(CharityProject).where(CharityProject.id == charity_project_id)
        )
        db_charity_project = db_charity_project.scalars().first()
        return db_charity_project

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> List:
        """Получаем список проектов, отсортированный по времени закрытия."""

        close_projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    CharityProject.description,
                    CharityProject.create_date,
                    CharityProject.close_date,
                ]
            ).where(CharityProject.fully_invested)
        )
        sort_close_prolect = sorted(
            close_projects.all(),
            key=lambda project: project.close_date - project.create_date,
        )
        return sort_close_prolect


charity_project_crud = CRUDCharityProject(CharityProject)
