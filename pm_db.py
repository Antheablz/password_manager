#!/usr/bin/env python3
import psycopg2
import hashlib, uuid
import os

import sqlalchemy as db
import sqlalchemy_utils as db_utils

from sqlalchemy import *
from sqlalchemy.orm import *

from cryptography.fernet import Fernet
from dotenv import load_dotenv

from consts import DEFAULT_DB_URL, PM_DB_URL, DB_PM, PWD_TABLE_NAME


class Base(DeclarativeBase):
    pass

class PasswordEntry(Base):
    """
    Class used to set up the database table.
    
    Attributes:
        identifier (MappedColumn[Any]): the identifier column in the datatbase
        association (MappedColumn[Any]): the association column in the datatbase
        username (MappedColumn[Any]): the username column in the datatbase
        password (MappedColumn[Any]): the password column in the datatbase
    """
    __tablename__ = PWD_TABLE_NAME

    identifier = mapped_column(Integer, primary_key=True, autoincrement=True)
    association = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False)
    password = mapped_column(String, nullable=False)


class Database:
    """
    Creates and manages a database
    """
    
    def __init__(self):
        self.__session = None
        self.__secret_key = os.environ['MY_SUPER_SECRET_SECRET']
        self.__fernet = Fernet(self.__secret_key)

    def __execute(self, session: Session, query: Query):
        """
        Executes a database query.

        Args:
            session (Session): the open database session
            query (Query): the query to be executed

        Returns:
            Result[Any]: if the query successfully executed or not
        """
        session.begin()
        result = session.execute(query)
        session.commit()
        session.close()

        return result

    def __create_db(self):
        """
        Creates a new database

        Args:
            none
        
        Returns:
            none
        """
        default_engine = db.create_engine(DEFAULT_DB_URL, isolation_level='AUTOCOMMIT')

        session = Session(default_engine)
        query = text(f'CREATE DATABASE {DB_PM}')
        self.__execute(session, query)

        print('New DB Created')

    def __decrypt_password(self, enc_password: str):
        """
        Decrypts a given encrypted password

        Args:
            enc_password (string): an encrypted password
        
        Returns:
            string: the decrypted plaintext string
        """
        dec_password = self.__fernet.decrypt(enc_password).decode()
        return dec_password
    
    def __encrypt_password (self, password: str):
        """
        Encrypts a given plaintext password

        Args:
            password (string): a plaintext password
        
        Returns:
            string: the encrypted  string
        """
        enc_password = self.__fernet.encrypt(password.encode()).decode()
        return enc_password

    def connect(self, db_url: str):
        """
        connects to an existing database

        Args:
            db_url (string): the database url
        
        Returns:
            none
        """
        if db_utils.database_exists(db_url) == False:
            self.__create_db()

        engine = db.create_engine(db_url)
        Base.metadata.create_all(engine)

        self.__session = Session(engine, autobegin=False, expire_on_commit=False)
        print('Connected to DB')

    def add_password(self, association: str, username: str, password: str):
        """
        Adds a password to the database

        Args:
            association (string): what the password is associated with
            username (string): the corresponding username
            password (string): the password to be entered

        Returns:
            none
        """
        # load_dotenv()
        # print(f"original pass: {password}")

        enc_password = self.__encrypt_password(password)

        query = insert(PasswordEntry).values(association=association, username=username, password=enc_password)
        self.__execute(self.__session, query)

    def update_association(self, identifier: int, new_association: str):
        """
        Updates the association records are tied to

        Args:
            identifier (int): the unique record identification number
            new_association (string): the corresponding association to be updated

        Returns:
            none
        """
        query = update(PasswordEntry).where(PasswordEntry.identifier == identifier).values(association=new_association)
        self.__execute(self.__session, query)

    def update_password(self, identifier: int, new_password: str):
        """
        Updates a specific password

        Args:
            identifier (int): the unique record identification number
            new_password (string): the corresponding new password to be updated

        Returns:
            none
        """
        query = update(PasswordEntry).where(PasswordEntry.identifier == identifier).values(password=new_password)
        self.__execute(self.__session, query)

    def update_username(self, identifier: int, new_username: str):
        """
        Updates a specific username

        Args:
            identifier (int): the unique record identification number
            new_username (string): the corresponding new username to be updated

        Returns:
            none
        """
        query = update(PasswordEntry).where(PasswordEntry.identifier == identifier).values(username=new_username)
        self.__execute(self.__session, query)

    def delete_entry(self, identifier: int):
        """
        Deletes a record from the database

        Args:
            identifier (int): the unique record identification number

        Returns:
            none
        """
        query = delete(PasswordEntry).where(PasswordEntry.identifier == identifier)
        self.__execute(self.__session, query)

    def show_all(self):
        """
        Retrieves all records from the database

        Args:
            none

        Returns:
            Sequence[RowMapping]: all the database records
        """
        query = select('*').select_from(PasswordEntry)
        result = self.__execute(self.__session, query).mappings().fetchall()

        return result

    def show_select(self, identifier: str):
        """
        Retrieves a specific record row from the database

        Args:
            identifier (int): the unique record identification number

        Returns:
            Sequence[RowMapping]: the selected row from the database
        """
        query = select('*').select_from(PasswordEntry).where(PasswordEntry.association.contains(identifier))
        result = self.__execute(self.__session, query).mappings().fetchall()

        return result
    
    def show_password(self, identifier: int):
        """
        Retrieves a specific decrypted password from a selected row from the database

        Args:
            identifier (int): the unique record identification number

        Returns:
            Sequence[RowMapping]: the selected decrypted password from the database
        """
        query = select(column('password')).select_from(PasswordEntry).where(PasswordEntry.identifier == identifier)
        result = self.__execute(self.__session, query).mappings().fetchone()
        dec_password = self.__decrypt_password(result['password'])

        return dec_password

    def delete_db(self):
        pass

# def main():
#     database = Database()
#     database.connect(PM_DB_URL)
#     database.add_password("tmp_association", "tmp_name", "tmp_password")
#     #database.add_password("UHGUHGUDH", "ugghhh", "ughhhhhh3")
    
#     # database.update_username(8, "new_username")
#     # database.update_username(1, "new_username")
#     # database.update_username(2, "new_username2")
#     # database.update_username(-3, "new_username")
#     # for i in range(0,51):
#     #     database.delete_entry(i)
   

#     # database.update_password(4, "this_is_a_test!")
#     # database.update_association(3, "JKJKJKJKJ   dddd")
#     database.show_all()
#     #database.show_select(1)

# if __name__ == "__main__":
#     main()


