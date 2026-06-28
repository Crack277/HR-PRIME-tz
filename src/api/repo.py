from typing import Dict, List, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.schemas import PaginationSchema, VacancyResponse, VacancySchema
from src.models import Vacancy, Company

class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_companies_by_vacancies(self, pagination: PaginationSchema) -> List[Company]:
        """
        Получение компаний с вакансиями (сортировка по убыванию вакансий)
        """
        stmt = (
            select(Company)
            .options(selectinload(Company.vacancies))
            .order_by(Company.vacancies_count.desc())
            .offset(pagination.offset)
            .limit(pagination.per_page)
        )
        result = await self.session.execute(stmt)
        companies = result.scalars().all()

        return list(companies)

    async def get_vacancies(self) -> Tuple[List[Vacancy], int]:
        """
        Получаем все вакансии и их количество
        """
        stmt = select(Vacancy).order_by(Vacancy.id)
        result = await self.session.execute(stmt)
        vacancies = result.scalars().all()

        return list(vacancies), len(list(vacancies))

    async def save_vacancies(self, vacancies: List[VacancySchema]) -> VacancyResponse:
        """
        Сохранение вакансий с автоматическим созданием компаний
        """
        saved_vacancies = 0
        saved_companies = 0
        company_cache = {} # Используем 'кэш' для того, чтобы не перегружать бд запросами

        for value in vacancies:
            company_name = value.company
            
            company, is_new = await self.get_or_create_company(company_name, company_cache)

            if is_new:
                saved_companies += 1
            
            vacancy = Vacancy(
                title=value.title,
                experience=value.experience,
                salary=value.salary,
                city=value.city,
                company_id=company.id
            )
            
            self.session.add(vacancy)
            saved_vacancies += 1
            company.vacancies_count += 1
        
        await self.session.commit()
        
        response = VacancyResponse(
            saved_vacancies=saved_vacancies,
            saved_companies=saved_companies
        )

        return response

    async def get_or_create_company(
        self, 
        company_name: str, 
        cache: Dict[str, Company]
    ) -> Tuple[Company, bool]:
        """
        Получение или создание компании
        """
        if company_name in cache:
            return cache[company_name], False
        
        stmt = select(Company).where(Company.name == company_name)
        result = await self.session.execute(stmt)
        company = result.scalar_one_or_none()
        
        is_new = False
        if not company:
            company = Company(name=company_name, vacancies_count=0)
            self.session.add(company)
            await self.session.flush()
            is_new = True
        
        cache[company_name] = company
        return company, is_new