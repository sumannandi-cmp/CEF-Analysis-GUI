import numpy as np
import tkinter as tk
from tkinter import Toplevel, Frame, Button,filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os
from scipy.optimize import fsolve,bisect


class Plotter:
    @classmethod
    def plot_Cp(cls,app):
        app.window1 = Toplevel(app)
        app.window1.geometry('600x500')
        app.window1.attributes('-topmost', 'true')
        toolbarFrame = Frame(app.window1)
        toolbarFrame.pack(side='bottom', fill='both', expand=True)
        figure = plt.figure(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(figure, app.window1)
        NavigationToolbar2Tk(canvas, toolbarFrame).pack(side='left', fill='x', expand=True)
        axes = figure.add_subplot()
        T = np.arange(float(app.n11[1].get()),float(app.n11[2].get())+float(app.n11[3].get()),float(app.n11[3].get()))
        B=float(app.n11[0].get())
        n = [float(app.n2[r].get()) for r in range(9)]
        if float(app.n9[1].get()) == 1:
            axes.plot(app.d[:, 0],app.d[:, 1], 'o', label='Exp')
        app.labels = ['T (K) \t\t cp (J/molK)']
        if float(app.n9[0].get()) == 1:
            chi_values =app.chi(n,T,B,app.Jz,'Cp')
            axes.plot(T, chi_values, lw=2, label='Theory')
            axes.set_xlabel('T (K)')
            axes.set_ylabel('C (J/molK)')
            app.merged_data = np.column_stack((T,chi_values))

        axes.legend()
        figure.tight_layout()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
        tk.Button(toolbarFrame, text='Export', command=lambda: cls.save_data(app)).pack(side='right', padx=10, pady=5)
    
    @classmethod
    def plot_EH(cls,app):
        app.window1 = Toplevel(app)
        app.window1.geometry('600x500')
        app.window1.attributes('-topmost', 'true')
        toolbarFrame = Frame(app.window1)
        toolbarFrame.pack(side='bottom', fill='both', expand=True)
        figure = plt.figure(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(figure, app.window1)
        NavigationToolbar2Tk(canvas, toolbarFrame).pack(side='left', fill='x', expand=True)
        axes = figure.add_subplot()
        B=np.arange(0,float(app.n16[1].get())+1,1)
        n = [float(app.n2[r].get()) for r in range(9)]
        dim=int(2*float(app.n.get())+1)
        e=np.zeros((len(B),dim))
        dir=[app.Jx,app.Jy,app.Jz]
        for i in range (len(B)):
            e[i]=app.chi(n,2,B[i],dir[app.source1.current()],R='eigen',M=0)[0]
        app.labels=['B (T)']
        for i in range (dim):
            axes.plot(B,e[:,i],lw=1,c='b')
            app.labels.append(f'E_{i} (K)')
        axes.set_xlabel('H (T)')
        axes.set_ylabel('Energy (K)')
        figure.tight_layout()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
        app.merged_data=np.hstack((B.reshape(-1, 1), e))
        tk.Button(toolbarFrame, text='Export', command=lambda: cls.save_data(app)).pack(side='right', padx=10, pady=5)
    
    @classmethod
    def plot_chi(cls,app):
        app.window1 = Toplevel(app)
        app.window1.geometry('600x500')
        app.window1.attributes('-topmost', 'true')
        toolbarFrame = Frame(app.window1)
        toolbarFrame.pack(side='bottom', fill='both', expand=True)
        figure = plt.figure(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(figure, app.window1)
        NavigationToolbar2Tk(canvas, toolbarFrame).pack(side='left', fill='x', expand=True)
        axes = figure.add_subplot()
        n=[float(app.n2[r].get()) for r in range(9)]
        T = np.arange(float(app.n11[5].get()),float(app.n11[6].get())+float(app.n11[7].get()),float(app.n11[7].get()))
        dir=[app.Jx,app.Jy,app.Jz]
        dir1=['a','b','c']
        dir2 = [app.da, app.db, app.dc]
        for i in range(3):
            if float(app.n3[i+3].get())==1:
                axes.plot(dir2[i][:,0],dir2[i][:,1],'o',label=f'H||{dir1[i]} Exp')
        chi_columns = []
        app.labels = ['T (K)']
        for i in range(3):
            if float(app.n3[i].get())==1:
                chi_values=app.chi(n,T, float(app.n11[4].get())+10 ** (-9),dir[i],'chivsT')-float(app.n8[i].get())
                axes.plot(T,chi_values , lw=2,label=f'H||{dir1[i]} Theory')
                axes.set_xlabel('T (K)')
                axes.set_ylabel(r'$\chi$ (mol/emu)')
                chi_columns.append(chi_values)
                app.labels.append(f'invchi_H||{dir1[i]} (mol/emu)')
        axes.legend()
        figure.tight_layout()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
        tk.Button(toolbarFrame, text='Export', command=lambda: cls.save_data(app)).pack(side='right', padx=10, pady=5)
        app.merged_data = np.column_stack([T] + chi_columns)
    
    @classmethod
    def plot_MvsH(cls,app):
        app.window1 = Toplevel(app)
        app.window1.geometry('600x500')
        app.window1.attributes('-topmost', 'true')
        toolbarFrame = Frame(app.window1)
        toolbarFrame.pack(side='bottom', fill='both', expand=True)
        figure = plt.figure(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(figure, app.window1)
        NavigationToolbar2Tk(canvas, toolbarFrame).pack(side='left', fill='x', expand=True)
        axes = figure.add_subplot()
        n = [float(app.n2[r].get()) for r in range(9)]
        B = np.arange(float(app.n5[1].get()),float(app.n5[2].get())+float(app.n5[3].get()),float(app.n5[3].get()))
        dir=[app.Jx,app.Jy,app.Jz]
        dir1=['a','b','c']
        dir2 = [app.d1a, app.d1b, app.d1c]
        for i in range(3):
            if float(app.n4[i+3].get())==1:
                axes.plot(dir2[i][:,0],dir2[i][:,1],'o',label=f'H||{dir1[i]} Exp')
        chi_columns = []
        app.labels = ['H (T)']
        for i in range(3):
            if float(app.n4[i].get())==1:
                m = np.zeros(len(B))
                M_i = 0.0
                for k in range(1,len(B)):
                    def app_consistent_eq(M_guess):
                        return M_guess - app.chi(n,float(app.n5[0].get()),B[k],dir[i],'MvsH',M=M_guess*float(app.n8[i].get())*0.5585)
                    '''M_right=M_i+0.01
                    while M_right<3:
                        if app_consistent_eq(M_i)*app_consistent_eq(M_right)<0:
                            m[k]=bisect(app_consistent_eq,M_i,M_right)
                            break
                        else:
                            M_right=M_right+0.01'''
                    while M_i<float(app.n.get())*float(app.n1.get()):
                        root = fsolve(app_consistent_eq,M_i)[0]
                        if root>m[k-1]:
                            m[k]=root
                            break
                        else:
                            M_i=M_i+1
                    M_i=m[k]
                axes.plot(B,m, lw=2,label=f'H||{dir1[i]} Theory')
                axes.set_xlabel('B (T)')
                axes.set_ylabel(r'M ($\mu_B$/fu)')
                chi_columns.append(m)
                app.labels.append(f'M_H||{dir1[i]} (muB/fu)')
        axes.legend()
        figure.tight_layout()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
        tk.Button(toolbarFrame, text='Export', command=lambda: cls.save_data(app)).pack(side='right', padx=10, pady=5)
        app.merged_data = np.column_stack([B] + chi_columns)
    
    @classmethod
    def save_data(cls,app):
        file = filedialog.asksaveasfile(parent=app.window1,
                                        filetypes=[("text file", ".txt")],
                                        defaultextension=".txt")
        if file:
            filepath = os.path.abspath(file.name)
            np.savetxt(filepath, app.merged_data, header='\t\t'.join(app.labels), fmt='%.6e', delimiter='\t')