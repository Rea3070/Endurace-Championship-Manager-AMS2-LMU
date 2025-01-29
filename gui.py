import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import defaultdict
import imsa_points_calculator
import imsa_cumulative_standings

import time

def process_json(file_path, param):
    imsa_points_calculator.main(file_path)
    if param == "add":
        imsa_cumulative_standings.main(param)
    elif param == "sub":
        imsa_cumulative_standings.main(param)


def open_fileAdd():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        process_json(file_path, "add")

def open_filesub():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        process_json(file_path, "sub")



def main():
    root = tk.Tk()
    root.title("IMSA Race Manager")
    
    root.geometry('300x200') 
    tk.Label(root, text="Select a race results JSON file to add").pack(pady=25)
    tk.Button(root, text="Add Race", width=20,command=open_fileAdd).pack(pady=5)
    tk.Button(root, text="Undo Race",fg='white',bg='red', width=20,command=open_filesub).pack(pady=5)
    tk.Button(root, text="Exit",  width=10,command=root.quit).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
