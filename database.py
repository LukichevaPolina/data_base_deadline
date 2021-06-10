import psycopg2
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text, create_engine
from sqlalchemy.orm import mapper, relation, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

auth = {'user': 'postgres', 'password': 'pshenokek16'}
Base = declarative_base()


class Database:
    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://{}:{}@localhost/lab2'.format(auth['user'],
                                                                                        auth['password'], echo=True))

    def delete_db(self):
        return

    def select_from_db(self):
        return

    def clear(self):
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


bot_db = Database()