from sqlalchemy import not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.services.close import close


async def invested_new_donation(
    new_donation: Donation,
    session: AsyncSession,
):
    """Функция распределения пожертований при создании нового пожертвования."""

    open_projects = await session.execute(
        select(CharityProject)
        .where(not_(Donation.fully_invested))
        .order_by(CharityProject.create_date)
    )
    print(open_projects)
    open_projects = open_projects.scalars().all()
    for project in open_projects:
        required_amount = project.full_amount - project.invested_amount
        invest_sum = new_donation.full_amount - new_donation.invested_amount
        if invest_sum <= required_amount:
            project.invested_amount += invest_sum
            new_donation.invested_amount += invest_sum
            close(project)
            session.add(project)
            close(new_donation)
            break
        else:
            project.invested_amount += required_amount
            invest_sum -= required_amount
            new_donation.invested_amount += required_amount
            session.add(project)
    session.add(new_donation)
    await session.commit()
    await session.refresh(new_donation)
