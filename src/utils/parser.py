import requests
import asyncio
from bs4 import BeautifulSoup

from src.api.schemas.vacancy import VacancySchema
from src.static.regions import RUSSIAN_REGIONS
from src.config import settings


async def get_vacancies_partial_regions(
    search: str = "",
    per_page: int = 20, # Больше не получается, хотя в api написано (минимум - 20, а максимум - 50)
    headers: dict = settings.parser.header
):
    """
    Получаем вакансии по регионам (area, из static/regions.py)
    """
    all_vacancies = []

    for region in RUSSIAN_REGIONS:
        id = region["id"]

        vacancies = await get_vacancies_by_region(
            area=id,
            search=search,
            per_page=per_page,
            headers=headers,
        )

        all_vacancies.extend(vacancies)

        await asyncio.sleep(2) # подобрать значение при котором не банят

    return all_vacancies


async def get_vacancies_by_region(
    area: int,
    search: str = "",
    per_page: int = 20,
    url: str = settings.parser.url, 
    headers: dict = settings.parser.header
):
    """
    Получаем вакансии из конкретного региона (area)
    """
    vacancies = []
    page = 0
    MAX_PAGES = 40

    while True:

        if page >= MAX_PAGES:
            break

        params = {
            "text": search,
            "area": area,
            "per_page": per_page,
            "page": page,
        }

        response = requests.get(
            url=url, 
            headers=headers, 
            params=params,  
            timeout=10,
            allow_redirects=True,
        )

        if response.status_code == 404:
            break

        response.raise_for_status()
        response.encoding = response.apparent_encoding
            
        soup = BeautifulSoup(response.text, "html.parser")
        vacancy_descriptions = soup.find_all("div", class_="vacancy-info--ieHKDTkezpEj0Gsx")


        for item in vacancy_descriptions:

            # Название вакансии
            name_elem = item.find("span", {"data-qa": "serp-item__title-text"})
            name = name_elem.text.strip() if name_elem else "Не указано"

            experience_elem = item.find("span", {"data-qa": "vacancy-serp__vacancy-work-experience-between1And3"})
            experience = experience_elem.text.strip() if experience_elem else "Не указано"

            # Заработная плата
            salary_elem = item.find("span", class_="magritte-text___pbpft_5-3-6 " \
            "magritte-text_style-primary___AQ7MW_5-3-6 magritte-text_typography-label-1-regular___pi3R-_5-3-6")
            salary = salary_elem.text.strip() if salary_elem else "Не указано"

            # Компания
            company_elem = item.find("span", {"data-qa": "vacancy-serp__vacancy-employer-text"})
            company = company_elem.text.strip() if company_elem else "Не указано"

            # Город
            city_elem = item.find("span", {"data-qa": "vacancy-serp__vacancy-address"})
            city = city_elem.text.strip() if city_elem else "Не указано"

            vacancy = VacancySchema(
                title=name,
                experience=experience,
                salary=salary,
                company=company,
                city=city
            )
            vacancies.append(vacancy)

        page += 1
        await asyncio.sleep(1) # подобрать значение при котором не банят
        
    return vacancies