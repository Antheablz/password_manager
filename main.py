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

def search_pwd(database: Database, search_var: tk.Entry):
    #result = database.show_select(search_var)
    print(search_var.get())
    print("TESTING")

def main():
    root = tk.Tk()
    root.title("Password Manager")
    root.configure(background="pink")

    root.minsize(600, 400)
    root.maxsize(600, 400)
    root.geometry("600x500")

    database = Database()
    database.connect(consts.PM_DB_URL)
    #database.add_password("tmp_association", "tmp_username", "tmp_password")
    #database.add_password("YAGEO", "fuck head", "crap")
    #database.add_password("HHHHHHHHH", "help me", "please")
    passwords = database.show_all()


    #table_text = tk.Text(window, bg="light blue")
    table_text = scrolledtext.ScrolledText(root, width=50, height=500, bg="light blue")
    table = PrettyTable()
    #table.padding_width = 2

    table.field_names = ["association", "username", "password"]

    for pwd in passwords:
        table.add_row([pwd["association"], pwd["username"], pwd["password"]])

    table_text.insert(1.0, table)
    #table_text.grid(row=0, column=2)
    table_text.pack(side="right")
    table_text.configure(state="disabled")


    search = tk.Entry(root)
    search.pack()

    def tmp_func():
        text = search.get()
        print(text)

    search_btn = tk.Button(root, text="Search", command=tmp_func)
    search_btn.pack()

 

    # label = tk.Label(root, text="Label", bg="pink")
    # label.place(x=300, y=250, anchor="center")

    # button = tk.Button(root, text="quit", command=root.destroy)
    # button.place(x=300, y=250, anchor="center")
    

    # frame = tk.Frame(root)
    # frame.grid()
    # tk.Label(frame, text="hello world").grid()
    # tk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)

    root.mainloop()

if __name__ == "__main__":
    main()