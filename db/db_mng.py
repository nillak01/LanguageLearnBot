from sqlalchemy import (create_engine, Column, Integer,
                         MetaData, Date, insert, delete, text)
from sqlalchemy.orm import declarative_base
import pandas as pd
from environs import Env
import logging

logging.basicConfig(
    level='INFO'
)

logger = logging.getLogger(__name__)
# from config import get_db_url

# Define Table Classes
Base = declarative_base()


class StudentsTable1(Base):
    __tablename__ = 'StudentsTable1'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    event_id = Column(Integer, nullable=False)
    event_date = Column(Date, nullable=False)
    customer_id = Column(Integer, nullable=False)
    is_attend = Column(Integer, nullable=False)
    group_ids = Column(Integer, nullable=False)
    teacher_ids = Column(Integer, nullable=False)
    attendance_id = Column(Integer, nullable=False)


def get_db_url(path: str | None = None) -> str:
    # Создаем эксемпляр класса Env
    env: Env = Env()

    # Пробуем загрузить данные из .env
    try:
        # Добавляем в переменное окружение данные из .env
        env.read_env(path)

        # Возвращаем созданный эксемпляр класса DB_URL
        return str(env('DB_URL'))

    except Exception:
        logger.error("Cant read env")


URL = get_db_url()
print(URL)
# Replace 'your_database_url_here' with your actual database URL
engine = create_engine(URL)


def create_all():
    # Create the tables in the database
    Base.metadata.create_all(engine)


def get_from_db(stmt):
    with engine.connect() as conn:
        return conn.execute(
            stmt
        ).all()


def insert_data(stmt):
    with engine.connect() as conn:
        result = conn.execute(
            insert(StudentsTable1),
            stmt
        )
        conn.commit()


def print_all_tables(engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)

    tables = metadata.tables.keys()

    print("List of tables:")
    for table in tables:
        print(table)


# Drop the table
def delete_table(table: Base):
    with engine.connect() as conn:
        result = conn.execute(
            delete(table)
        )
        conn.commit()


def get_all():
    result = get_from_db(text(
        """select * from "StudentsTable1" st"""
    ))

    return pd.DataFrame(result)


def get_bad_student(n: int = 5):

    result = get_from_db(text(
        """select  st.customer_id,  count(st.customer_id) as count_attend from "StudentsTable1" st
where st.is_attend = 0
group by st.customer_id
order by count_attend  desc """
    ))

    return pd.DataFrame(result).head(n)


def get_bad_group():

    result = get_from_db(text(
        """select group_ids, count_attend * 100 / count_group_ids as percent from (
select  st.group_ids, count_attend, count_group_ids  from (select  st.group_ids,  count(st.group_ids) as count_attend from "StudentsTable1" st
where st.is_attend = 0
group by st.group_ids
order by count_attend  desc) as st
join (select  st.group_ids,  count(st.group_ids) as count_group_ids from "StudentsTable1" st
group by st.group_ids
order by count_group_ids  desc ) st1 on st.group_ids=st1.group_ids) as sss
order by percent desc  """
    ))

    return pd.DataFrame(result)


if __name__ == '__main__':

    # delete_table(StudentsTable1)
    # data = pd.read_excel(path, sheet_name='data')
    # insert_data(data.to_dict('records'))
    print_all_tables(engine)
    print(get_all().head(10))


db = pd.read_csv(r'db\db_simulation.scv')

# db = pd.DataFrame(
#     columns=['Name', 'Surname', 'tg_id','tg_nickname', 'status'])
# db = db._append({'Name': 'Yaroslav', 'Surname': 'No', 'tg_id': 637603487,'tg_nickname': 'nillak0_0', 'status': 'Admin'}, ignore_index=True)
# db.to_csv(r'db\db_simulation.scv')
print('Ok')
print(db)