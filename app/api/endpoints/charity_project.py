from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_full_amount_befor_edit_project,
    check_invested_amount,
    check_name_duplicate,
    check_the_project_is_closed,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.new_project import invested_new_project

router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    """Обработка запроса на создание проекта."""

    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    await invested_new_project(new_charity_project, session)
    return new_charity_project


@router.get(
    "/", response_model=List[CharityProjectDB], response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Обработка запроса на получение списка всех проектов."""

    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    """Обработка запроса на изменение проекта."""

    charity_project = await check_charity_project_exists(project_id, session)
    await check_the_project_is_closed(project_id, session)
    if obj_in.full_amount:
        await check_full_amount_befor_edit_project(project_id, obj_in, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    """Обработка запроса на удаление проекта."""

    charity_project = await check_charity_project_exists(project_id, session)
    await check_invested_amount(project_id, session)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project
