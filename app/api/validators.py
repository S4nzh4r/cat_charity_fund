from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_charity_prj_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    charity_prj = await charity_project_crud.get(
        project_id, session
    )

    if charity_prj is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )

    return charity_prj


async def check_fully_invested(
        charity_prj: CharityProject,
) -> None:
    if charity_prj.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Нельзя редактировать или '
                'удалять польностью инвестированный обьект'
            )
        )


async def check_little_invested(
        charity_prj: CharityProject,
) -> None:
    if charity_prj.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Запрещено удаление проектов, в которые уже внесены средства.'
            )
        )


async def check_full_amount(
        invested_amount: int,
        new_amount: int
) -> None:
    if new_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую сумму меньше уже вложенной!'
        )
