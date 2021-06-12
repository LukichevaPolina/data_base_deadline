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
                                Column('Task ID', Integer, primary_key=True, autoincrement=True),
                                Column('Task', String),
                                Column('Group', String))

        self.teachers_table = Table('Teachers', self.metadata,
                                 Column('Discipline', String, ForeignKey('Deadlines.Discipline')),
                                 Column('Teacher', String, primary_key=True),
                                 Column('Mail', String))

        self.groups_table = Table('Groups', self.metadata,
                              Column('ID', Integer, primary_key=True, autoincrement=True),
                              Column('Group', String, ForeignKey('Deadlines.Task ID')),
                              Column('Mail', String),
                              Column('Number of tasks', String))

        self.tables = {'deadlines_table': self.deadlines_table,
                        'teachers_table': self.teachers_table,
                        'groups_table': self.groups_table}
        self.metadata.create_all(self.engine)

    def get_tables(self):
        return ['deadline_table', 'teachers_table', 'groups_table']

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

    def delete_by_field(self, name_table: str):
        return

    def delete_data(self, ):
        for table in self.tables.values():
            for fields in self.tables
        return
