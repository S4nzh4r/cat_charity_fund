from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.crud.base import CRUDBase


ModelType = TypeVar('ModelType', bound=Base)


async def check_obj_amount(
        db_obj: ModelType,
        session: AsyncSession,
        crud_obj: CRUDBase
) -> None:
    """Функция для проверки не достигла ли требоваемая сумма."""
    if db_obj.full_amount - db_obj.invested_amount == 0:
        await crud_obj.close_object(db_obj, session)


async def to_invest(
        session: AsyncSession,
        db_obj: ModelType,
        crud_obj_1: CRUDBase,
        crud_obj_2: CRUDBase
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
            invested_amount = invested_amount + (
                obj.full_amount - obj.invested_amount
            )
            # Вычисляем остаток для проверки достигла ли
            # сумма инвестов требоваемой суммы
            remain = db_obj.full_amount - invested_amount
            if remain <= 0:  # Если да
                # Вычисляем сумму инвеста от списка not_fully_invested.
                obj.invested_amount = obj.invested_amount + (
                    invested_amount - (remain * -1) - db_obj.invested_amount
                )
                # Вычисляем сумму инвеста для нашего только созданного обьекта.
                db_obj.invested_amount = invested_amount - (remain * -1)

                # Проверка на full_amount для второго обьекта.
                await check_obj_amount(obj, session, crud_obj_2)

                # Закрываем наш обьект.
                db_obj = await crud_obj_1.close_object(
                    db_obj=db_obj, session=session, the_end=True
                )
                break

            # Новая сумма инвеста после операций для второго обьекта.
            obj.invested_amount = obj.invested_amount + (
                invested_amount - db_obj.invested_amount
            )
            # Проверка на full_amount для второго обьекта.
            await check_obj_amount(obj, session, crud_obj_2)

            # Новая сумма инвеста после получения доната или наоборот.
            db_obj.invested_amount = invested_amount
    return db_obj
