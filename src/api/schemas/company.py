
from pydantic import BaseModel


class CompanySchema(BaseModel):
    name: str
    vacancies_count: int