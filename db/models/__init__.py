from sqlalchemy import MetaData, create_engine, Table, Column, String, Integer, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import settings

engine = create_engine(f'postgresql+psycopg2://{settings.db.user}:{settings.db.password}@'
                       f'{settings.db.host}/{settings.db.database}')
DBSession = sessionmaker(bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)
session = DBSession()

from .vacancy import Vacancy