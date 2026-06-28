from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Company
from src.api.schemas import PaginationSchema
from src.api.repo import Repository
from src.database.database_helper import db_helper
from src.utils import parser, save_to_excel
from src.config import settings


router = APIRouter(prefix=settings.parser.prefix)


@router.post("/companies")
async def get_companies_by_vacancies(
    pagination: PaginationSchema,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    repo = Repository(session=session)
    return await repo.get_companies_by_vacancies(pagination=pagination)


@router.get("/vacancies")
async def get_vacancies(
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    repo = Repository(session=session)
    return await repo.get_vacancies()


@router.post("/vacancies")
async def save_vacancies_to_db(
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    vacancies = await parser.get_vacancies_partial_regions()

    repo = Repository(session)
    result = await repo.save_vacancies(vacancies=vacancies)
    return result


@router.post("/vacancies_excel")
def save_vacancies_to_excel(
    companies_data: List[Company] = Depends(get_companies_by_vacancies)
):
    return save_to_excel.export_companies_to_excel(companies_data=companies_data)