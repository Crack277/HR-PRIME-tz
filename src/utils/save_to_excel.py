import pandas as pd
from pathlib import Path
from typing import List

from src.models import Company

def export_companies_to_excel(companies_data: List[Company], filename: str = "companies.xlsx") -> str:
        """
        Экспорт компаний с их вакансиями в Excel
        """
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
        
        df = pd.DataFrame(rows)
        
        base_dir = Path(__file__).parent.parent.parent
        output_dir = base_dir / "exports"
        output_dir.mkdir(exist_ok=True)
    
        # Путь к файлу (папка + имя файла)
        filepath = output_dir / filename
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            
            df.to_excel(writer, sheet_name="Вакансии", index=False)
            
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