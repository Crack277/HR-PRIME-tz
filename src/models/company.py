from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .vacancy import Vacancy


class Company(Base):
    __tablename__ = "companies" # корректное название (не от класса Base - companys)

    name: Mapped[str]
    vacancies_count: Mapped[int] = mapped_column(default=0)

    vacancies: Mapped[List["Vacancy"]] = relationship(back_populates="company")