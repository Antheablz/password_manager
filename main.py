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

        self.__db = Database()
        self.__db.connect(consts.PM_DB_URL)

        #self.__search_btn = tk.Button(self.__root, text="Search", command=self.search_pwd)

    def __create_table(self):
        pass

    def __search(self):
        self.__table_text.destroy()
        self.__search_btn.destroy()

        pwd = self.__db.show_select(self.__search_entry.get())
        self.__search_entry.destroy()

        text = tk.Text(self.__root, width=50, height=500, bg="light blue")

        table = PrettyTable()
        table.field_names = ["association", "username", "password"]
        table.add_row([pwd["association"], pwd["username"], pwd["password"]])
        
        text.insert(1.0, table)
        text.pack(side="right")
        text.configure(state="disabled")

    def search_pwd(self):
        self.__search_entry = tk.Entry(self.__root)
        self.__search_entry.pack()
        self.__search_btn = tk.Button(self.__root, text="Search", command=self.__search)
        self.__search_btn.pack()
        

    def show_all(self):
        passwords = self.__db.show_all()

        self.__table_text = scrolledtext.ScrolledText(self.__root, width=50, height=500, bg="light blue")
        table = PrettyTable()

        table.field_names = ["association", "username", "password"]
        for pwd in passwords:
            table.add_row([pwd["association"], pwd["username"], pwd["password"]])

        self.__table_text.insert(1.0, table)
        self.__table_text.pack(side="right")
        self.__table_text.configure(state="disabled")


    def mainloop(self):
        self.__root.mainloop()



def main():
    gui = PwdGUI()
    gui.show_all()
    gui.search_pwd()
    gui.mainloop()

    # search = tk.Entry(root)
    # search.pack()

    # def tmp_func():
    #     text = search.get()
    #     print(text)

    # search_btn = tk.Button(root, text="Search", command=tmp_func)
    # search_btn.pack()

 

    # label = tk.Label(root, text="Label", bg="pink")
    # label.place(x=300, y=250, anchor="center")

    # button = tk.Button(root, text="quit", command=root.destroy)
    # button.place(x=300, y=250, anchor="center")
    

    # frame = tk.Frame(root)
    # frame.grid()
    # tk.Label(frame, text="hello world").grid()
    # tk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)



if __name__ == "__main__":
    main()