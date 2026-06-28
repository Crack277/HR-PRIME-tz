import os
from pathlib import Path
import pandas as pd
from typing import List

from src.models import Company

def export_companies_to_excel(companies_data: List[Company], filename: str = "companies.xlsx") -> str:
        """
        Экспорт компаний с их вакансиями в Excel
        """
        
        # Формируем данные для Excel
        rows = []
        for company in companies_data:
            vacancies = company.vacancies
            
            if vacancies:
                for vacancy in vacancies:
                    rows.append({
                        "ID компании": company.id,
                        "Компания": company.name,
                        "Всего вакансий": company.vacancies_count,
                        "Название вакансии": vacancy.title,
                        "Опыт": vacancy.experience,
                        "Зарплата": vacancy.salary,
                        "Город": vacancy.city
                    })
        
        # Создаем DataFrame
        df = pd.DataFrame(rows)
        
        base_dir = Path(__file__).parent.parent.parent
        output_dir = base_dir / "exports"
        output_dir.mkdir(exist_ok=True)
    
        # Путь к файлу (папка + имя файла) 👈 ВАЖНО!
        filepath = output_dir / filename
        
        # Сохраняем в Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Лист с деталями
            df.to_excel(writer, sheet_name="Вакансии", index=False)
            
            # Лист со сводкой
            summary = []
            for company in companies_data:
                summary.append({
                    "ID": company.id,
                    "Компания": company.name,
                    "Количество вакансий": company.vacancies_count
                })
            df_summary = pd.DataFrame(summary)
            df_summary.to_excel(writer, sheet_name="Топ компаний", index=False)
            
        
        return filepath