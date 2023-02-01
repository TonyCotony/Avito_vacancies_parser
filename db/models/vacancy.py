import datetime

from sqlalchemy import Column, Integer, String, Date

from db.models import Base


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String)
    link = Column(String, unique=True)
    address = Column(String)
    terms = Column(String)
    salary = Column(String)
    description = Column(String)
    entry_date = Column(Date)

    def __init__(self, all_info: dict):
        self.job_title = all_info['title']
        self.link = all_info['link']
        self.address = all_info['address']
        self.terms = all_info['terms']
        self.salary = all_info['salary']
        self.description = all_info['description']
        self.entry_date = datetime.date.today()

    def __repr__(self):
        info: str = f"Название: {self.job_title}\n" \
                    f"Условия: {self.terms}\n" \
                    f"Частичное описание: {self.description[:200]}\n" \
                    f"Адрес: {self.terms}" \
                    f"Заработная плата: {self.salary}" \
                    f"Ссылка: {self.link}"
        return info
