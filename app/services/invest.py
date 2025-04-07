from typing import TypeVar, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.crud import CRUDCharityProject, CRUDDonation
from app.crud.base import CRUDBase


ModelType = TypeVar('ModelType', bound=Base)


async def check_obj_amount(
        db_obj: ModelType,
        session: AsyncSession,
        crud_obj: CRUDBase
) -> None:
    """Функция для проверки не достигла ли требоваемая сумма."""
    if db_obj.invested_amount == db_obj.full_amount:
        await crud_obj.close_object(db_obj, session)


async def to_invest(
        session: AsyncSession,
        db_obj: ModelType,
        crud_obj_1: Union[CRUDCharityProject, CRUDDonation],
        crud_obj_2: Union[CRUDCharityProject, CRUDDonation]
) -> ModelType:
    """Функция для распределения свободных
    донатов после создания одного из двух проектов."""

    # Получаем список не закрытых проектов или пожертвований.
    not_fully_invested = await crud_obj_2.get_all_not_fully_invested(
        session=session
    )

    invested_amount = db_obj.invested_amount
    if not_fully_invested:
        for obj in not_fully_invested:
            # Добавляем к сумме инвеста от пожертвования или проекта.
            invested_amount += (
                obj.full_amount - obj.invested_amount
            )
            # Вычисляем остаток для проверки достигла ли
            # сумма инвестов требоваемой суммы
            remain = db_obj.full_amount - invested_amount
            if remain <= 0:  # Если да
                # Вычисляем сумму инвеста от списка not_fully_invested.
                # Например затраты от донатов для проекта.
                obj.invested_amount = obj.full_amount + remain

                # Вычисляем сумму инвеста для нашего только созданного обьекта.
                db_obj.invested_amount = invested_amount + remain

                # Проверка на full_amount для второго обьекта.
                await check_obj_amount(obj, session, crud_obj_2)

                # Закрываем наш обьект.
                db_obj = await crud_obj_1.close_object(
                    db_obj=db_obj, session=session, the_end=True
                )
                break

            # Если нужная сумма не набролась...
            # значит мы потратили все средства от донатов или
            # наоборот закрыли проект из списка not_fully_invested.
            obj.invested_amount = obj.full_amount

            await crud_obj_2.close_object(obj, session)

            # Новая сумма инвеста после получения доната или наоборот.
            db_obj.invested_amount = invested_amount
    return db_obj
