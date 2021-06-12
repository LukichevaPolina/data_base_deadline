import psycopg2
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Date, text, create_engine, event
from sqlalchemy.orm import mapper, relation, sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


class Deadline(object):

    task_id = None

    def __init__(self, discipline, deadline, task, group):
        self.discipline = discipline
        self.deadline = deadline
#        self.task_id = task_id
        self.task = task
        self.group = group

    def __repr__(self):
        return "<Deadline('%s','%s', '%s', '%s')>" % (self.discipline, self.deadline, self.task, self.group)


class Teacher(object):
    def __init__(self, discipline, teacher, mail):
        self.discipline = discipline
        self.teacher = teacher
        self.mail = mail

    def __repr__(self):
        return "<Deadline('%s','%s', '%s')>" % (self.discipline, self.teacher, self.mail)



class Group(object):
    def __init__(self, group, mail, num):
        self.group = group
        self.mail = mail
        #self.num = num

    def __repr__(self):
        return "<Deadline('%s','%s')>" % (self.group, self.mail)


class Database:
    def __init__(self, login, password):
        self.modified_trigger = """
        CREATE TRIGGER update_Deadlines_modified
        AFTER INSERT OR DELETE​ON 'Deadlines'​
        FOR EACH STATEMENT EXECUTE PROCEDURE update_num_deadlines()
        """
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
        self.listen = event.listen(self.Base.metadata, 'after_create', self.create_modified_trigger)
        self.mapper1 = mapper(Deadline, self.tables['deadlines_table'])
        self.mapper2 = mapper(Teacher, self.tables['teachers_table'])
        self.mapper3 = mapper(Group, self.tables['groups_table'])

    def update_num_deadlines(self):
        for i in self.session.query(Deadline).order_by(Deadline.task_id):
            sum = 0
            for gr in self.session.query(Group).order_by(Group.id):
                if gr.group == gr:
                    sum += 1
            Group.num = sum


    def create_modified_trigger(self, connection, **kwargs):
        """
        This is used to add bookkeeping triggers after a table is created. It hooks
        into the SQLAlchemy event system. It expects the target to be an instance of
        MetaData.
        """
        for key in self.tables:
            table = self.tables[key]
            connection.execute(self.modified_trigger.format(table_name=table.name))


    def get_tables(self):
        return ['deadline_table', 'teachers_table', 'groups_table']

    def create_db(self, login, password, name):
        engine = create_engine('postgresql://{}:{}@localhost/{}'.format(login, password, name, echo=True))
        if not database_exists(engine.url):
            create_database(engine.url)
            return 0
        return 1

    def delete_db(self):
        self.engine.drop()

    def select_from_db(self):
        return

    def clear(self, name_table: str, full_del: bool):
        if full_del:
            self.metadata.drop_all(self.engine)
        else:
            self.tables[name_table].drop(self.engine)

    def add_data(self, discipline: str, deadline, task: str, group: str):
        new_task = Deadline(discipline, deadline, task, group)
        self.session.add(new_task)
        flag1, flag2 = 0, 0
        if self.session.query(Deadline.discipline).filter(Deadline.discipline == discipline) == 0:
            flag1 = 1
        if self.session.query(Deadline.group).filter(Deadline.group == group) == 0:
            flag2 = 1
        if flag1 == 1 and flag2 == 1:
            return -3
        elif flag1 == 1:
            return -1
        elif flag2 == 1:
            return -2
        self.session.commit()
        return 0

    def add_teacher(self, discipline, teacher, mail):
        new_teacher = Teacher(discipline, teacher, mail)
        self.session.add(new_teacher)
        self.session.commit()

    def add_group(self, group, mail):
        new_group = Group(group, mail)
        self.session.add(new_group)
        self.session.commit()

    def search(self):
        return

    def update_tuple(self):
        return

    def delete_by_field(self, name_table: str):
        return

    def delete_data(self):
        return


