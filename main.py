#!/pm_env/bin/python3
import tkinter as tk
import consts

from prettytable import PrettyTable
from sqlalchemy import *

from pm_db import Database, PasswordEntry

def main():
    window = tk.Tk()
    window.title("Password Manager")
    window.configure(background="pink")

    window.minsize(600, 500)
    window.maxsize(600, 500)
    window.geometry("600x500")

    database = Database()
    database.connect(consts.PM_DB_URL)
    #database.add_password("tmp_association", "tmp_username", "tmp_password")
    #database.add_password("YAGEO", "fuck head", "crap")
    database.add_password("HHHHHHHHH", "help me", "please")

    passwords = database.show_all()

    #print(passwords)

    table_text = tk.Text(window, bg="light blue")
    table = PrettyTable()

    table.field_names = ["association", "username", "password"]

    for pwd in passwords:
        table.add_row([pwd["association"], pwd["username"], pwd["password"]])
    

    table_text.insert(0.1,table)
    table_text.place(x=300, y=250, anchor="center")


 


    # label = tk.Label(root, text="Label", bg="pink")
    # label.place(x=300, y=250, anchor="center")

    # button = tk.Button(root, text="quit", command=root.destroy)
    # button.place(x=300, y=250, anchor="center")
    

    # frame = tk.Frame(root)
    # frame.grid()
    # tk.Label(frame, text="hello world").grid()
    # tk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)

    window.mainloop()

if __name__ == "__main__":
    main()