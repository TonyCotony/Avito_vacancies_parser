from sqlalchemy import MetaData, Table, Column, String, Integer, Date

from db.models import Base, engine


def create_db():
    Base.metadata.create_all(engine)
    #
    metadata = MetaData()

    vacancy = Table('vacancy', metadata,
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('job_title', String),
                    Column('link', String, unique=True),
                    Column('address', String),
                    Column('terms', String),
                    Column('salary', String),
                    Column('description', String),
                    Column('entry_date', Date)
                    )
    #
    metadata.create_all(engine)
    Base.metadata.create_all(engine)

    return print('schemas imported')


if __name__ == '__main__':
    create_db()
