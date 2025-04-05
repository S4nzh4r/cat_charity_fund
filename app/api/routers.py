from fastapi import APIRouter

from app.api.endpoints import charity_prj_router, donation_router, user_router


main_router = APIRouter()
main_router.include_router(
    charity_prj_router, prefix='/charity_project', tags=['Charity Projects']
)
main_router.include_router(
    donation_router, prefix='/donation', tags=['Donations']
)
main_router.include_router(user_router)
