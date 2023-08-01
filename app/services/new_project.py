from sqlalchemy import not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.services.close import close


async def invested_new_project(
    new_charity_project: CharityProject,
    session: AsyncSession,
):
    """Функция распределения пожертований при создании нового проекта."""

    open_donation = await session.execute(
        select(Donation)
        .where(not_(Donation.fully_invested))
        .order_by(Donation.create_date)
    )
    open_donation = open_donation.scalars().all()
    for donation in open_donation:
        donation_sum = donation.full_amount - donation.invested_amount
        required_amount = (
            new_charity_project.full_amount - new_charity_project.invested_amount
        )
        if required_amount <= donation_sum:
            donation.invested_amount += required_amount
            new_charity_project.invested_amount += required_amount
            close(donation)
            session.add(donation)
            close(new_charity_project)
            break
        else:
            donation.invested_amount += donation_sum
            required_amount -= donation_sum
            new_charity_project.invested_amount += donation_sum
            session.add(donation)
    session.add(new_charity_project)
    await session.commit()
    await session.refresh(new_charity_project)
