import psycopg2
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Date, text, create_engine
from sqlalchemy.orm import mapper, relation, sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database



class Database:
    def __init__(self, login, password):
        self.Base = declarative_base()
        self.engine = create_engine('postgresql+psycopg2://{}:{}@localhost/lab2'.format(login, password, echo=True))
        self.engine.connect()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.metadata = MetaData()
        self.deadlines_table = Table('Deadlines', self.metadata,
                                Column('Discipline', String),
                                Column('Deadline', Date),
                                Column('Task ID', Integer, primary_key=True, autoincrement=True))

        self.discipline_table = Table('Disciplines', self.metadata,
                                 Column('Discipline', String, primary_key=True),
                                 Column('Teacher', String))

        self.task_table = Table('Tasks', self.metadata,
                           Column('ID', Integer, ForeignKey('Deadlines.Task ID')),
                           Column('Task', String),
                           Column('Group', String))

        self.tables = {'deadlines_table': self.deadlines_table,
                  'discipline_table': self.discipline_table,
                  'task_table': self.task_table}
        self.metadata.create_all(self.engine)

    def get_tables(self):
        return ['deadline_table', 'discription_table', 'task_table']

    def create_db(self, login, password, name):
        engine = create_engine('postgresql://{}:{}@localhost/{}'.format(login, password, name, echo=True))
        if not database_exists(engine.url):
            create_database(engine.url)
            return 0
        return 1

    def delete_db(self):
        self.deadlines_table.drop()

    def select_from_db(self):
        return

    def clear(self, name_table: str, full_del: bool):
        if full_del:
            for tab in self.tables.values():
                print(type(tab))
                tab.drop(self.engine)
        else:
            self.tables[name_table].drop(self.engine)

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
