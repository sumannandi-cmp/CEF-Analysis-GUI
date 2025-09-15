import numpy as np
import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class DataLoader:
    @classmethod
    def import_data(cls, app):
        app.window = Toplevel(app)
        app.window.geometry('300x100')
        app.window.attributes('-topmost', 'true')
        tk.Label(app.window, text='Data Source').grid(row=0, column=0, padx=20, pady=5)
        app.n6 = tk.StringVar()
        source = ttk.Combobox(app.window, textvariable=app.n6)
        source['values'] = ('Schottky Specific Heat', '1/Chi vs T', 'M vs H')
        source.grid(column=1, row=0)
        tk.Label(app.window, text='H ||').grid(row=1, column=0, padx=20, pady=5)
        app.n7 = tk.StringVar()
        source = ttk.Combobox(app.window, textvariable=app.n7)
        source['values'] = ('a', 'b', 'c')
        source.grid(column=1, row=1)
        tk.Button(app.window, text='ok', command=lambda: cls.destro(app)).grid(row=2, column=1)
    
    @classmethod
    def destro(cls, app):
        app.window.destroy()
        file = filedialog.askopenfile(mode='r',filetypes=[('Text File', '*.dat'), ('Text File', '*.txt'), ('All files', '*.*')])
        if file:
            filepath = os.path.abspath(file.name)
            if app.n6.get()=='Schottky Specific Heat':
                app.d = np.genfromtxt(str(filepath), dtype=float, delimiter='\t')
                app.n14[3].set(f"{min(app.d[:,0]):.2f},{max(app.d[:,0]):.2f}")
            if app.n6.get()=='1/Chi vs T':
                if app.n7.get()=='a':
                    app.da = np.genfromtxt(str(filepath), dtype=float, delimiter='\t')
                    app.n14[0].set(f"{min(app.da[:, 0]):.2f},{max(app.da[:, 0]):.2f}")
                if app.n7.get()=='b':
                    app.db = np.genfromtxt(str(filepath), dtype=float, delimiter='\t')
                    app.n14[1].set(f"{min(app.db[:, 0]):.2f},{max(app.db[:, 0]):.2f}")
                if app.n7.get()=='c':
                    app.dc = np.genfromtxt(str(filepath), dtype=float, delimiter='\t')
                    app.n14[2].set(f"{min(app.dc[:, 0]):.2f},{max(app.dc[:, 0]):.2f}")
            if app.n6.get()=='M vs H':
                if app.n7.get()=='a':
                    app.d1a = np.genfromtxt(str(filepath), dtype=float, delimiter='\t')
                if app.n7.get()=='b':
                    app.d1b = np.genfromtxt(str(filepath), dtype=float, delimiter='\t')
                if app.n7.get()=='c':
                    app.d1c = np.genfromtxt(str(filepath), dtype=float, delimiter='\t')
    
    @classmethod
    def show_data(cls, app):
        for item in app.tv1.get_children():
            app.tv1.delete(item)
        t=['C_p','1/Chi vs T-a','1/Chi vs T-b','1/Chi vs T-c','M vs H-a','M vs H-b','M vs H-c']
        dat=[app.d,app.da,app.db,app.dc,app.d1a,app.d1b,app.d1c]
        data = dat[int(app.source.current())].tolist()
        for row in data:
            app.tv1.insert("", "end", values=row)