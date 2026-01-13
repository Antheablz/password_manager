#!/pm_env/bin/python3
import tkinter as tk
import consts

from prettytable import PrettyTable
from sqlalchemy import *
from tkinter import scrolledtext, ttk

from pm_db import Database, PasswordEntry

class PwdGUI():
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title("Password Manager")

        self.__root.columnconfigure(0, weight=1)
        # self.__root.columnconfigure(1, weight=2)
        self.__root.rowconfigure(0, weight=1)

        self.__top_frame = tk.Frame(self.__root) #frame is just a container
        # self.__left_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.__top_frame.grid(row=0, column=0)
        self.__top_frame.columnconfigure(0, weight=1)
        self.__top_frame.rowconfigure(1, weight=1)

        self.__bottom_frame = tk.Frame(self.__root) #frame is just a container
        # self.__right_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.__bottom_frame.grid(row=1, column=0)
        self.__bottom_frame.columnconfigure(0, weight=1)
        self.__bottom_frame.rowconfigure(1, weight=1)


        self.__search_btn = tk.Button(self.__top_frame, text="Search", command=self.__search)
        self.__search_btn.grid(row=0, column=1)
        self.__search_entry = tk.Entry(self.__top_frame)
        self.__search_entry.grid(row=0, column=2)

        self.__home_btn = tk.Button(self.__top_frame, text="Clear", command=self.__back_home)
        self.__home_btn.grid(row=0, column=4)

        self.__delete_btn = tk.Button(self.__top_frame, text="Delete Pwd")
        self.__delete_btn.grid(row=0, column=5)


        self.__add_btn = tk.Button(self.__top_frame, text="Add Pwd", command=self.__add_record)
        self.__add_btn.grid(row=4, column=0)
        
        association_text = tk.StringVar()
        association_text.set("Association: ")
        association_label = tk.Label(self.__top_frame, textvariable=association_text)
        association_label.grid(row=4, column=1)
        self.__association = tk.Entry(self.__top_frame)
        self.__association.grid(row=4, column=2)

        username_text = tk.StringVar()
        username_text.set("Username: ")
        username_label = tk.Label(self.__top_frame, textvariable=username_text)
        username_label.grid(row=4, column=3)
        self.__username = tk.Entry(self.__top_frame)
        self.__username.grid(row=4, column=4)

        password_text = tk.StringVar()
        password_text.set("Password: ")
        pasword_label = tk.Label(self.__top_frame, textvariable=password_text)
        pasword_label.grid(row=4, column=5)
        self.__password = tk.Entry(self.__top_frame)
        self.__password.grid(row=4, column=6)



        self.__table_headers = ["identifier", "association", "username", "header_4"]
        self.__tree = ttk.Treeview(self.__bottom_frame, columns=self.__table_headers, show="headings")


        self.__db = Database()
        self.__db.connect(consts.PM_DB_URL)

        self.show_all()

    def __refresh_table(self):
        for i in self.__tree.get_children():
            self.__tree.delete(i)

    def __back_home(self):
        self.__refresh_table()
        self.show_all()

    def __create_table(self, passwords):
        self.__tree.heading(0, text=self.__table_headers[0])
        self.__tree.heading(1, text=self.__table_headers[1])
        self.__tree.heading(2, text=self.__table_headers[2])

        for pwd in passwords:
            self.__tree.insert("", tk.END, values=(pwd["identifier"], pwd["association"], pwd["username"]))

        self.__tree.pack()


    def __search(self):
        passwords = self.__db.show_select(self.__search_entry.get())
        self.__refresh_table()
        self.__create_table(passwords)
        self.__search_entry.delete(0, "end")

    def __add_record(self):
        
        self.__db.add_password(self.__association.get(), self.__username.get(), self.__password.get())
        self.__association.delete(0, "end")
        self.__username.delete(0, "end")
        self.__password.delete(0, "end")

        self.__refresh_table()
        self.show_all()

    def __delete_record(self):
        pass

    def edit_pwd(self):
        pass

    def show_all(self):
        passwords = self.__db.show_all()
        self.__create_table(passwords)
        

    def mainloop(self):
        self.__root.mainloop()


def main():
    gui = PwdGUI()

    gui.mainloop()

if __name__ == "__main__":
    main()