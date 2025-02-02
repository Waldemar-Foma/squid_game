import sys
import tkinter as tk
from tkinter import messagebox


def show_error_message(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка", message)
    sys.exit()
