from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.models import Donation, User
from app.schemas.donation import DonationAllDB, DonationCreate, DonationUserDB
from app.services.invest import to_invest

router = APIRouter()


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Donation:
    donation_db = await donation_crud.create(
        donation, session, user
    )

    donation_db = await to_invest(
        session, donation_db, donation_crud, charity_project_crud
    )

    return donation_db


@router.get(
    '/my',
    response_model=list[DonationUserDB],
    response_model_exclude_none=True
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> list[Donation]:
    """Получает список всех донатов для текущего пользователя."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations


@router.get(
    '/',
    response_model=list[DonationAllDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
) -> list[Donation]:
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations
