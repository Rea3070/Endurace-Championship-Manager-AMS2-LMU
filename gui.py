import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import *
from tkinter.ttk import *
from collections import defaultdict
import imsa_points_calculator
import imsa_cumulative_standings

import time

def process_json(file_path, param, game):
    print(game)
    imsa_points_calculator.main(file_path, game)
    if param == "add":
        imsa_cumulative_standings.main(param,game)
    elif param == "sub":
        imsa_cumulative_standings.main(param,game)


def open_fileAdd(game):
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        process_json(file_path, "add", game)

def open_filesub(game):
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        process_json(file_path, "sub",game)


def main():
    root = tk.Tk()
    root.title("Endurance Race Manager")
    root.geometry('400x200') 


    frame = tk.Frame(root)
    frame.pack(side=tk.RIGHT, pady=10,padx=15)

    v = StringVar(root, "imsa") 
    values = {"IMSA" : "imsa", 
        "WEC" : "wec", 
        "WEC 8HR Race" : "wec_8hr", 
        "Le Mans" : "leman"} 

    for (text, value) in values.items(): 
        Radiobutton(frame, text=text, variable=v, value=value).pack( fill='x', ipady=5)

    frame2 = tk.Frame(root)
    frame2.pack( pady=10)

    tk.Label(frame2, text="Select a race results JSON file to add").pack(pady=25)
    tk.Button(frame2, text="Add Race", width=20,command=lambda: open_fileAdd(v.get())).pack(pady=5)
    tk.Button(frame2, text="Undo Race",fg='white',bg='red', width=20,command=lambda: open_filesub(v.get())).pack(pady=5)
    tk.Button(frame2, text="Exit",  width=10,command=root.quit).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()



#Python -m PyInstaller --noconsole --onefile --icon="Icons\Icon-copy.ico" gui.py