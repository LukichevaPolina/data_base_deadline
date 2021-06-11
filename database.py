import psycopg2
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Date, text, create_engine
from sqlalchemy.orm import mapper, relation, sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


class Database:
    def __init__(self, login, password):
        engine = create_engine('postgresql+psycopg2://{}:{}@localhost/lab2'.format(login, password, echo=True))
        engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        metadata = MetaData()
        deadlines_table = Table('Deadlines', metadata,
                                Column('Discipline', String),
                                Column('Deadline', Date),
                                Column('Task ID', Integer, primary_key=True, autoincrement=True))

        discipline_table = Table('Disciplines', metadata,
                                 Column('Discipline', String, primary_key=True),
                                 Column('Teacher', String))

        task_table = Table('Tasks', metadata,
                           Column('ID', Integer, ForeignKey('Deadlines.Task ID')),
                           Column('Task', String),
                           Column('Group', String))

        metadata.create_all(engine)

    def create_db(self, login, password, name):
        engine = create_engine('postgresql://{}:{}@localhost/{}'.format(login, password, name, echo=True))
        if not database_exists(engine.url):
            create_database(engine.url)
            return 0
        return 1

    def delete_db(self):
        return

    def select_from_db(self):
        return

    def clear(self, full_del: bool):
        if full_del:
            return
        return



    def add_data(self):
        return

    def search(self):
        return

    def update_tuple(self):
        return

    def delete_by_field(self):
        return

    def delete_data(self):
        return
