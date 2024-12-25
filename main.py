#!/pm_env/bin/python3

import tkinter as tk
from sqlalchemy import *

def main():
    root = tk.Tk()
    root.title("Password Manager")
    root.configure(background="pink")

    root.minsize(400, 300)
    root.maxsize(600, 500)
    root.geometry("400x300")

    root.mainloop()

if __name__ == "__main__":
    main()