from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):

    async def get_charity_prj_id_by_name(
        self,
        charity_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        charity_id = await session.execute(
            select(CharityProject).where(
                CharityProject.name == charity_name
            )
        )
        charity_id = charity_id.scalars().first()
        return charity_id


charity_project_crud = CRUDCharityProject(CharityProject)
