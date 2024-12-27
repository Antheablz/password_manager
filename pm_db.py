#!/usr/bin/env python3
import psycopg2
import hashlib, uuid
import sqlalchemy as db
import sqlalchemy_utils as db_utils

from sqlalchemy import *
from sqlalchemy.orm import *

from consts import DEFAULT_DB_URL, PM_DB_URL, DB_PM, PWD_TABLE_NAME


class Base(DeclarativeBase):
     pass

class PasswordEntry(Base):
    __tablename__ = PWD_TABLE_NAME

    identifier = mapped_column(Integer, primary_key=True, autoincrement=True)
    association = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False,)
    password = mapped_column(String, nullable=False)


class Database:
    def __init__(self):
        self.__session = None

    def __execute(self, session: Session, query: Query):
        session.begin()
        result = session.execute(query)
        session.commit()
        session.close()

        return result

    def __create_db(self):
        default_engine = db.create_engine(DEFAULT_DB_URL, isolation_level='AUTOCOMMIT')

        session = Session(default_engine)
        query = text(f'CREATE DATABASE {DB_PM}')
        self.__execute(session, query)

        print('New DB Created')

    def connect(self, db_url: str):
        if db_utils.database_exists(db_url) == False:
            self.__create_db()

        engine = db.create_engine(db_url)
        Base.metadata.create_all(engine)

        self.__session = Session(engine, autobegin=False, expire_on_commit=False)
        print('Connected to DB')

    def add_password(self, association: str, username: str, password: str):
        query = insert(PasswordEntry).values(association=association, username=username, password=password)
        self.__execute(self.__session, query)

    def update_association(self, identifier: int, new_association: str):
        query = update(PasswordEntry).where(PasswordEntry.identifier == identifier).values(association=new_association)
        self.__execute(self.__session, query)

    def update_password(self, identifier: int, new_password: str):
        query = update(PasswordEntry).where(PasswordEntry.identifier == identifier).values(password=new_password)
        self.__execute(self.__session, query)

    def update_username(self, identifier: int, new_username: str):
        query = update(PasswordEntry).where(PasswordEntry.identifier == identifier).values(username=new_username)
        self.__execute(self.__session, query)

    def delete_entry(self, identifier: int):
        query = delete(PasswordEntry).where(PasswordEntry.identifier == identifier)
        self.__execute(self.__session, query)

    def show_all(self):
        query = select('*').select_from(PasswordEntry)
        result = self.__execute(self.__session, query).mappings().fetchall()

        return result

    def show_select(self, identifier: int):
        query = select('*').select_from(PasswordEntry).where(PasswordEntry.identifier == identifier)
        result = self.__execute(self.__session, query).mappings().fetchone()

        return result

    def delete_db(self):
        pass

# def main():
#     database = Database()
#     database.connect(PM_DB_URL)
#     #database.add_password("tmp_association", "tmp_name", "tmp_password")
#     #database.add_password("UHGUHGUDH", "ugghhh", "ughhhhhh3")
    
#     # database.update_username(8, "new_username")
#     # database.update_username(1, "new_username")
#     # database.update_username(2, "new_username2")
#     # database.update_username(-3, "new_username")
#     # database.delete_entry(1)
#     # database.update_password(4, "this_is_a_test!")
#     # database.update_association(3, "JKJKJKJKJ   dddd")
#     database.show_all()
#     #database.show_select(1)

# if __name__ == "__main__":
#     main()


