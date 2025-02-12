#!/pm_env/bin/python3
import tkinter as tk
import consts

from prettytable import PrettyTable
from sqlalchemy import *
from tkinter import scrolledtext

from pm_db import Database, PasswordEntry

class PwdGUI():
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title("Password Manager")
        self.__root.minsize(600, 400)
        self.__root.maxsize(600, 400)
        self.__root.geometry("600x400")

        self.__left_frame = tk.Frame(self.__root, width=200, height=400, bg="light blue")
        self.__left_frame.grid_rowconfigure([0,1,2,3,4,5,6,7,8,9], uniform="uniform", weight=1)
        self.__left_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.__right_frame = tk.Frame(self.__root, width=400, height=400, bg="light green")
        self.__right_frame.grid(row=0, column=1, sticky=tk.NSEW)

        self.__back_btn = tk.Button(self.__left_frame, text="back", command=self.show_all)

        self.__db = Database()
        self.__db.connect(consts.PM_DB_URL)

    def __create_table(self, passwords):
        self.__table_text = tk.Text(self.__right_frame, width=consts.TABLE_WIDTH, height=consts.TABLE_HEIGHT)
        table = PrettyTable()
        table._min_table_width = consts.TABLE_WIDTH
        table._max_table_width = consts.TABLE_WIDTH

        table.field_names = ["association", "username", "password"]
        for pwd in passwords:
            table.add_row([pwd["association"], pwd["username"], pwd["password"]])

        self.__table_text.insert(1.0, table)
        self.__table_text.place(relx=0.5, rely=0.5, anchor="center")
        self.__table_text.configure(state="disabled")

    def __search(self):
        passwords = self.__db.show_select(self.__search_entry.get())
        self.__create_table(passwords)
        self.__back_btn.grid(row=9, column=0)
        #self.__back_btn.place(relx=0.5, rely=0.95, anchor="center")

    def search_pwd(self):
        self.__search_entry = tk.Entry(self.__left_frame)
        self.__search_btn = tk.Button(self.__left_frame, text="Search", command=self.__search)

        self.__search_entry.grid(row=0, column=0)
        self.__search_btn.grid(row=1, column=0)
        #self.__search_entry.place(relx=0.5, rely=0.1, anchor="center")
        #self.__search_btn.place(relx=0.5, rely=0.175, anchor="center")

    def add_pwd(self):
        pass

    def update_pwd(self):
        pass

    def delete_pwd(self):
        delete_btn = tk.Button(self.__left_frame, text="Delete Pwd")


    def show_all(self):
        passwords = self.__db.show_all()
        self.__create_table(passwords)
        self.__back_btn.grid_forget()

    def mainloop(self):
        self.__root.mainloop()



def main():
    gui = PwdGUI()
    gui.search_pwd()
    gui.show_all()
    gui.mainloop()

if __name__ == "__main__":
    main()