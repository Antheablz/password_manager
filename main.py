#!/pm_env/bin/python3
import tkinter as tk
import consts

from sqlalchemy import *
from tkinter import messagebox, ttk

from pm_db import Database

class PwdGUI():
    """
    Creates and manages the password manager's GUI
    """

    def __init__(self):
        button_width = 8
        frame_padding = 20

        self.__root = tk.Tk()
        self.__root.title("Password Manager")

        self.__root.columnconfigure(0)
        self.__root.rowconfigure(0)

        # self.__root.columnconfigure(0, weight=1)
        # self.__root.rowconfigure(0, weight=1)

        self.__top_frame = tk.Frame(self.__root) #frame is just a container
        self.__top_frame.grid(row=0, column=0, padx=frame_padding, pady=frame_padding)
        # self.__bottom_frame.columnconfigure(0, weight=1)
        # self.__bottom_frame.rowconfigure(1, weight=1)

        self.__bottom_frame = tk.Frame(self.__root, highlightbackground="grey", highlightthickness=1, padx=frame_padding, pady=frame_padding) #frame is just a container
        self.__bottom_frame.grid(row=1, column=0, padx=frame_padding, pady=frame_padding)
        # self.__top_frame.columnconfigure(0, weight=1)
        # self.__top_frame.rowconfigure(1, weight=1)


        self.__search_record = tk.Button(self.__bottom_frame, text="Search", width=button_width, command=self.__search_record)
        self.__search_record.grid(row=0, column=1)
        self.__search_entry = tk.Entry(self.__bottom_frame)
        self.__search_entry.grid(row=0, column=2)

        self.__clear_btn = tk.Button(self.__bottom_frame, text="Clear", width=button_width, command=self.__back_home)
        self.__clear_btn.grid(row=0, column=4)

        self.__delete_btn = tk.Button(self.__bottom_frame, text="Delete Pwd", width=button_width, command=self.__delete_record)
        self.__delete_btn.grid(row=0, column=5)

        self.__show_pwd_btn = tk.Button(self.__bottom_frame, text="Show Pwd", width=button_width, command=self.__show_password)
        self.__show_pwd_btn.grid(row=0, column=6)

        self.__add_btn = tk.Button(self.__bottom_frame, text="Add Pwd", width=button_width, command=self.__add_record)
        self.__add_btn.grid(row=4, column=0)
        
        association_text = tk.StringVar()
        association_text.set("Association: ")
        association_label = tk.Label(self.__bottom_frame, textvariable=association_text)
        association_label.grid(row=4, column=1)
        self.__association = tk.Entry(self.__bottom_frame)
        self.__association.grid(row=4, column=2)

        username_text = tk.StringVar()
        username_text.set("Username: ")
        username_label = tk.Label(self.__bottom_frame, textvariable=username_text)
        username_label.grid(row=4, column=3)
        self.__username = tk.Entry(self.__bottom_frame)
        self.__username.grid(row=4, column=4)

        password_text = tk.StringVar()
        password_text.set("Password: ")
        pasword_label = tk.Label(self.__bottom_frame, textvariable=password_text)
        pasword_label.grid(row=4, column=5)
        self.__password = tk.Entry(self.__bottom_frame)
        self.__password.grid(row=4, column=6)

        self.__table_headers = ["identifier", "association", "username", "password (tmp)"]
        self.__tree = ttk.Treeview(self.__top_frame, columns=self.__table_headers, show="headings")

        self.__db = Database()
        self.__db.connect(consts.PM_DB_URL)

        self.__tree.bind("<ButtonRelease-1>", self.__get_record_details)

        self.show_all_records()

        # Sets a fixed window size
        self.__root.update()
        self.__root.minsize(self.__root.winfo_width(), self.__root.winfo_height())
        self.__root.maxsize(self.__root.winfo_width(), self.__root.winfo_height())

    def __refresh_table(self):
        """
        Refreshes elements in the table

        Args:
            none

        Returns:
            none
        """
        for i in self.__tree.get_children():
            self.__tree.delete(i)

    def __back_home(self):
        """
        Callback for a button that clears search results in the table

        Args:
            none

        Returns:
            none
        """
        self.__refresh_table()
        self.show_all_records()

    def __create_table(self, records: Sequence[RowMapping]):
        """
        Creates the table all database records are shown in

        Args:
            records (Sequence[RowMapping]): all of the records that will be listed in the table

        Returns:
            none
        """
        self.__tree.heading(0, text=self.__table_headers[0])
        self.__tree.heading(1, text=self.__table_headers[1])
        self.__tree.heading(2, text=self.__table_headers[2])
        self.__tree.heading(3, text=self.__table_headers[3])

        for rec in records:
            self.__tree.insert("", tk.END, values=(rec["identifier"], rec["association"], rec["username"], rec["password"]))

        self.__tree.pack()

    def __get_record_details(self, event):
        """
        Callback that retrieves a rows record details

        Args:
            event: the mouse event triggering thhis callback

        Returns:
            none
        """
        item = self.__tree.identify_row(event.y)
        item_details = self.__tree.item(item)
        self.__item_identifier = item_details["values"][0]

        # self.__enc_password = item_details["values"][3]
        # print(self.__enc_password)


    def __search_record(self):
        """
        Callback for a button that searches for a specific record

        Args:
            none

        Returns:
            none
        """
        passwords = self.__db.show_select(self.__search_entry.get())
        self.__refresh_table()
        self.__create_table(passwords)
        self.__search_entry.delete(0, "end")

    def __delete_record(self):
        """
        Callback for a button that deletes a specific record row in the table

        Args:
            none

        Returns:
            none
        """
        self.__db.delete_entry(self.__item_identifier)
        self.__refresh_table()
        self.show_all_records()

    def __add_record(self):
        """
        Callback for a button that adds a specific record row in the table

        Args:
            none

        Returns:
            none
        """
        result = self.__db.add_password(self.__association.get(), self.__username.get(), self.__password.get())
        
        if result == -1:
            messagebox.showerror(title="password", message="Error Adding Record")
        
        self.__association.delete(0, "end")
        self.__username.delete(0, "end")
        self.__password.delete(0, "end")

        self.__refresh_table()
        self.show_all_records()

    def __show_password(self):
        """
        Callback for a button that opens a popup revealing a decrypted passsword

        Args:
            none

        Returns:
            none
        """
        dec_password = self.__db.show_password(self.__item_identifier)
        messagebox.showinfo(title="password", message=dec_password)

    def __edit_pwd(self):
        pass

    def show_all_records(self):
        """
        Retrieves all the database records and creates a table to display them in

        Args:
            none

        Returns:
            none
        """
        passwords = self.__db.show_all()
        self.__create_table(passwords)
        

    def mainloop(self):
        """
        Runs the gui mainloop

        Args:
            none

        Returns:
            none
        """
        self.__root.mainloop()


def main():
    gui = PwdGUI()

    gui.mainloop()

if __name__ == "__main__":
    main()