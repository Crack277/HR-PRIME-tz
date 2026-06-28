from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .company import Company


class Vacancy(Base):
    __tablename__ = "vacancies" # корректное название (не от класса Base - vacancys)

    title: Mapped[str]
    experience: Mapped[str]
    salary: Mapped[str]
    city: Mapped[str]

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False
    )

    company: Mapped["Company"] = relationship(
        back_populates="vacancies",
        foreign_keys=[company_id]
    )