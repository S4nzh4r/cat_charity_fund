from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount, check_fully_invested,
    check_little_invested, check_name_duplicate,
    check_project_exists
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.invest import to_invest


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_prj: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров."""
    await check_name_duplicate(charity_prj.name, session)
    new_charity_prj = await charity_project_crud.create(charity_prj, session)
    new_charity_prj = await to_invest(
        session, new_charity_prj, charity_project_crud, donation_crud
    )
    return new_charity_prj


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
) -> list[CharityProject]:
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров."""
    charity_prj = await check_project_exists(
        project_id, session
    )

    await check_fully_invested(charity_prj)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount is not None:
        await check_full_amount(
            charity_prj.invested_amount,
            obj_in.full_amount
        )

    charity_prj = await charity_project_crud.update(
        charity_prj, obj_in, session
    )

    return charity_prj


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров."""
    charity_prj = await check_project_exists(
        project_id, session
    )
    await check_little_invested(charity_prj)

    await check_fully_invested(charity_prj)

    charity_prj = await charity_project_crud.remove(
        charity_prj, session
    )
    return charity_prj
