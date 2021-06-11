from config import auth
from sqlalchemy import Column, Table, Integer, String, MetaData, Date, ForeignKey, create_engine

engine = create_engine('postgresql://{}:{}@localhost/deadline_db'.format(auth['user'], auth['password']), echo=True)

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

