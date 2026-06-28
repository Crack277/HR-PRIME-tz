
from pydantic import BaseModel


class VacancySchema(BaseModel):
    title: str
    experience: str
    salary: str
    company: str
    city: str


class VacancyResponse(BaseModel):
    saved_vacancies: int
    saved_companies: int


class PaginationSchema(BaseModel):
    page: int = 1
    per_page: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page