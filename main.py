#!/pm_env/bin/python3
from tkinter import *
import tkinter as tk
from sqlalchemy import *

def main():
    root = tk.Tk()
    root.title("Password Manager")
    root.configure(background="pink")

    root.minsize(600, 500)
    root.maxsize(600, 500)
    root.geometry("600x500")


    #label = tk.Label(root, text="Centered Label")
    button = tk.Button(root, text="quit", command=root.destroy)
    button.place(x=300, y=250, anchor="center")
    #label.place(x=300, y=250, anchor="center")

    # frame = tk.Frame(root)
    # frame.grid()
    # tk.Label(frame, text="hello world").grid()
    # tk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)

    root.mainloop()

if __name__ == "__main__":
    main()