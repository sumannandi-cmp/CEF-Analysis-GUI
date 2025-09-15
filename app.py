from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, filedialog, messagebox
import os
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from steven import StevensOp
import pickle
import sys
from loader import DataLoader
from plotting import Plotter
from fitting import CEFFit

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('1200x800')
        #self.attributes('-fullscreen',True)
        self.title('CEF')

        main_menu = tk.Menu()
        # File menu
        file = tk.Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='File', menu=file)
        file.add_command(label='Import', compound=tk.LEFT, command=lambda: DataLoader.import_data(self))
        file.add_command(label='Save', compound=tk.LEFT, command=self.save)
        file.add_command(label='Open', compound=tk.LEFT, command=self.open)
        self.config(menu=main_menu)
        
        # Edit menu
        edit = tk.Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='Edit', menu=edit)
        edit.add_command(label='Fontsize', compound=tk.LEFT, command=self.edit_fs)
        self.config(menu=main_menu)
        
        # Data Frame
        tk.Label(self, text='Data Type').place(relx=0.0, rely=0)
        self.n10 = tk.StringVar()
        self.source = ttk.Combobox(self, textvariable=self.n10)
        self.source['values'] = ('C_p', '1/Chi vs T-a', '1/Chi vs T-b', '1/Chi vs T-c', 'M vs H-a', 'M vs H-b', 'M vs H-c')
        self.source.place(relx=0.1, rely=0)
        tk.Button(self, text='Ok', command=lambda: DataLoader.show_data(self)).place(relx=0.1, rely=0.05)
        
        # Data Frame
        self.frame6 = tk.LabelFrame(self, text='Data')
        self.frame6.place(y=80,height=500, width=300)
        # treeview1
        columns = ('first_name', 'last_name')
        self.tv1 = ttk.Treeview(self.frame6, columns=columns, show='headings')
        self.tv1.heading('first_name', text='T')
        self.tv1.heading('last_name', text='M')
        self.tv1.place(relheight=0.9,
                       relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).
        self.tv1.column('first_name', width=20)
        self.tv1.column('last_name', width=20)

        treescrolly = tk.Scrollbar(self.frame6, orient="vertical",
                                   command=self.tv1.yview)  # command means update the yaxis view of the widget
        self.tv1.configure(yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrolly.pack(side="right", fill="y")
        
        # J and g_J Frame
        self.frame5 = tk.LabelFrame(self, text='J and g_J')
        self.frame5.place(x=350, height=100, width=200)
        tk.Label(self.frame5, text='J').grid(row=1, column=0, padx=20, pady=3)
        self.n = tk.StringVar()
        tk.Entry(self.frame5, textvariable=self.n).grid(row=1, column=1)
        tk.Label(self.frame5, text='g').grid(row=2, column=0, padx=20, pady=3)
        self.n1 = tk.StringVar()
        tk.Entry(self.frame5, textvariable=self.n1).grid(row=2,column=1)
        tk.Label(self.frame5, text='Ion').grid(row=0, column=0)
        self.n0 = tk.StringVar()
        source = ttk.Combobox(self.frame5, textvariable=self.n0, width=10)
        source['values'] = ('Ce3+', 'Pr3+', 'Nd3+', 'Pm3+', 'Sm3+', 'Eu3+','Gd3+', 'Tb3+', 'Dy3+', 'Ho3+', 'Er3+', 'Tm3+','Yb3+')
        source.grid(column=1, row=0)
        source.bind("<<ComboboxSelected>>", self.update_entries)
        
        # O_nm Frame
        self.frame4 = tk.LabelFrame(self, text='CEF parameters')
        self.frame4.place(x=350,y=130, height=300, width=200)
        tk.Button(self.frame4, text='Diagonalise', command=self.show_eigen).place(relx=0.3, rely=0.9)
        self.n2=[]
        for i in range(9):
            self.n2.append(tk.StringVar())
        k=0
        for i in range(3):
            for j in range(i+2):
                tk.Label(self.frame4, text=f'B_{2*(i+1)}{2*j}').grid(row=3+k, column=0, padx=20,pady=3)
                tk.Entry(self.frame4, textvariable=self.n2[k],width=15).grid(row=3+k, column=1)
                self.n2[k].set("0.0")
                k=k+1
        
        # C_p Frame
        self.frame1 = tk.LabelFrame(self, text='Schottky Specific Heat')
        self.frame1.place(x=600,height=200, width=200)
        

        tk.Label(self.frame1, text='B(T)').grid(row=0, column=0)
        tk.Label(self.frame1, text='T_min(K)').grid(row=1, column=0,pady=10)
        tk.Label(self.frame1, text='T_max(K)').grid(row=1, column=1)
        tk.Label(self.frame1, text='step(K)').grid(row=1, column=2)
        self.n11 = [tk.StringVar(value='0.0'),tk.StringVar(value='2.0'),tk.StringVar(value='300.0'),tk.StringVar(value='1.0')]
        tk.Entry(self.frame1, textvariable=self.n11[0], width=10).grid(row=0, column=1)
        for i in range (3):
            tk.Entry(self.frame1, textvariable=self.n11[i+1], width=5).grid(row=2, column=i)
        tk.Label(self.frame1, text='Theory').place(relx=0.15, rely=0.5)
        tk.Label(self.frame1, text='Experiment').place(relx=0.55, rely=0.5)
        self.n9=[tk.IntVar(),tk.IntVar()]
        tk.Checkbutton(self.frame1, text='', variable=self.n9[0]).place(relx=0.2, rely=0.6)
        tk.Checkbutton(self.frame1, text='', variable=self.n9[1]).place(relx=0.65, rely=0.6)
        tk.Button(self.frame1, text='Plot', command=lambda: Plotter.plot_Cp(self)).place(relx=0.4, rely=0.8)
        
        # Chi-T Frame
        self.frame2 = tk.LabelFrame(self, text='1/Chi vs T')
        self.frame2.place(x=800,height=250, width=200)
        tk.Label(self.frame2, text='B(T)').grid(row=0, column=1)
        tk.Label(self.frame2, text='T_min(K)').grid(row=1, column=1, pady=5)
        tk.Label(self.frame2, text='T_max(K)').grid(row=1, column=2)
        tk.Label(self.frame2, text='step(K)').grid(row=1, column=3)
        self.n11.extend([tk.StringVar(value='0.0'),tk.StringVar(value='2.0'), tk.StringVar(value='300.0'),
                    tk.StringVar(value='1.0')])
        tk.Entry(self.frame2, textvariable=self.n11[4], width=10).grid(row=0, column=2)
        for i in range (3):
            tk.Entry(self.frame2, textvariable=self.n11[i+5], width=5).grid(row=2, column=i+1)
        tk.Label(self.frame2, text='Theory').grid(row=3, column=1,pady=10)
        tk.Label(self.frame2, text='Experiment').grid(row=3, column=2)
        tk.Label(self.frame2, text='Lambda').grid(row=3, column=3)
        self.n3=[]
        for i in range(6):
            self.n3.append(IntVar())
        tk.Checkbutton(self.frame2, text='', variable=self.n3[0]).grid(row=4, column=1)
        tk.Checkbutton(self.frame2, text='', variable=self.n3[1]).grid(row=5, column=1)
        tk.Checkbutton(self.frame2, text='', variable=self.n3[2]).grid(row=6, column=1)
        tk.Checkbutton(self.frame2, text='a', variable=self.n3[3]).grid(row=4, column=2)
        tk.Checkbutton(self.frame2, text='b', variable=self.n3[4]).grid(row=5, column=2)
        tk.Checkbutton(self.frame2, text='c', variable=self.n3[5]).grid(row=6, column=2)

        self.n8 = []
        for i in range(3):
            self.n8.append(tk.StringVar(value=0.0))
            tk.Entry(self.frame2, textvariable=self.n8[i],width=5).grid(row=4+i, column=3)
        tk.Button(self.frame2, text='Plot', command=lambda: Plotter.plot_chi(self)).grid(row=7, column=2)
        
        # M-H Frame
        self.frame3 = tk.LabelFrame(self, text='M vs H')
        self.frame3.place(x=1000,height=250, width=200)
        tk.Label(self.frame3, text='T(K)').grid(row=0, column=0)
        tk.Label(self.frame3, text='B_min(T)').grid(row=1, column=0, pady=10)
        tk.Label(self.frame3, text='B_max(T)').grid(row=1, column=1)
        tk.Label(self.frame3, text='step(T)').grid(row=1, column=2)
        self.n5 = [tk.StringVar(value='2.0'), tk.StringVar(value='0.0'), tk.StringVar(value='14.0'),
                    tk.StringVar(value='0.2')]
        tk.Entry(self.frame3, textvariable=self.n5[0],width=10).grid(row=0, column=1)
        for i in range (3):
            tk.Entry(self.frame3, textvariable=self.n5[i+1], width=5).grid(row=2, column=i)
        tk.Label(self.frame3, text='Theory').place(relx=0.15, rely=0.4)
        tk.Label(self.frame3, text='Experiment').place(relx=0.5, rely=0.4)
        self.n4 = []
        for i in range(6):
            self.n4.append(IntVar())
        tk.Checkbutton(self.frame3, text='', variable=self.n4[0]).place(relx=0.2, rely=0.5)
        tk.Checkbutton(self.frame3, text='', variable=self.n4[1]).place(relx=0.2, rely=0.6)
        tk.Checkbutton(self.frame3, text='', variable=self.n4[2]).place(relx=0.2, rely=0.7)
        tk.Checkbutton(self.frame3, text='a', variable=self.n4[3]).place(relx=0.6, rely=0.5)
        tk.Checkbutton(self.frame3, text='b', variable=self.n4[4]).place(relx=0.6, rely=0.6)
        tk.Checkbutton(self.frame3, text='c', variable=self.n4[5]).place(relx=0.6, rely=0.7)
        tk.Button(self.frame3, text='Plot', command=lambda: Plotter.plot_MvsH(self)).place(relx=0.4, rely=0.8)
        
        # Fit Frame
        self.frame9 = tk.LabelFrame(self, text='Fit')
        self.frame9.place(x=600, y=250, height=300, width=500)
        tk.Label(self.frame9, text='Data').place(relx=0.01, rely=0.01)
        self.n13 = []
        for i in range(4):
            self.n13.append(IntVar())
        tk.Checkbutton(self.frame9, text='1/Chi vs T-a', variable=self.n13[0]).place(relx=0.0, rely=0.1)
        tk.Checkbutton(self.frame9, text='1/Chi vs T-b', variable=self.n13[1]).place(relx=0.28, rely=0.1)
        tk.Checkbutton(self.frame9, text='1/Chi vs T-c', variable=self.n13[2]).place(relx=0.55, rely=0.1)
        tk.Checkbutton(self.frame9, text='C_p', variable=self.n13[3]).place(relx=0.83, rely=0.1)
        self.n14 = [tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]
        tk.Entry(self.frame9, textvariable=self.n14[0],width=15).place(relx=0.05, rely=0.2)
        tk.Entry(self.frame9, textvariable=self.n14[1], width=15).place(relx=0.3, rely=0.2)
        tk.Entry(self.frame9, textvariable=self.n14[2], width=15).place(relx=0.55, rely=0.2)
        tk.Entry(self.frame9, textvariable=self.n14[3], width=15).place(relx=0.8, rely=0.2)
        tk.Label(self.frame9, text='Parameters').place(relx=0.01, rely=0.3)
        self.n12 = []
        for i in range(9):
            self.n12.append(IntVar())
        k = 0
        for i in range(3):
            for j in range(i + 2):
                tk.Checkbutton(self.frame9, text=f'B_{2 * (i + 1)}{2 * j}', variable=self.n12[k]).place(relx=(0.0 + k/5)%1, rely=0.4+int(k/5)*0.1)
                k = k + 1
        tk.Button(self.frame9, text='Guess', command=lambda: CEFFit.guess(self)).place(relx=0.1, rely=0.6)
        self.fit_button=tk.Button(self.frame9, text='Fit', command=lambda: CEFFit.start_fitting(self))
        self.fit_button.place(relx=0.5, rely=0.9)
        self.status_label = tk.Label(self.frame9, text="")
        self.status_label.place(relx=0.43, rely=0.8)
        
        # Energy-B Frame
        frame5 = tk.LabelFrame(self, text='Energy Values')
        frame5.place(x=350,y=450, height=150, width=200)
        tk.Label(frame5, text='H ||').place(relx=0.1, rely=0.1)
        self.n16 = [tk.StringVar(),tk.StringVar(value="14.0")]
        self.source1 = ttk.Combobox(frame5, textvariable=self.n16[0], width=5)
        self.source1['values'] = ('a','b','c')
        self.source1.place(relx=0.3, rely=0.1)
        tk.Label(frame5, text='H_max').place(relx=0.1, rely=0.4)
        tk.Entry(frame5, textvariable=self.n16[1], width=10).place(relx=0.4, rely=0.4)
        tk.Button(frame5, text='Plot', command=lambda: Plotter.plot_EH(self)).place(relx=0.4, rely=0.7)

        self.d = 0;self.da = 0;self.db = 0;self.dc = 0;self.d1a = 0;self.d1b = 0;self.d1c = 0
        list = ['1.0', '-3.0,3.0', '1.0', '-3.0,3.0', '1.0', '-3.0,3.0', '1.0', '-3.0,3.0', '1.0', '-3.0,3.0', '1.0',
                    '-3.0,3.0', '1.0', '-3.0,3.0', '1.0', '-3.0,3.0', '1.0', '-3.0,3.0','10.0','-100,100','10.0','-100,100','10.0','-100,100']
        self.n15=[]
        for i in range (24):
            self.n15.append(tk.StringVar(value=f'{list[i]}'))

        self.protocol("WM_DELETE_WINDOW", self.on_close)
    def edit_fs(self):
        self.window2 = Toplevel(self)
        self.window2.geometry('300x100')
        self.window2.attributes('-topmost', 'true')
        self.fontsize = tk.StringVar(value=10)
        tk.Entry(self.window2, textvariable=self.fontsize).grid(row=0, column=0,padx=30)
        tk.Button(self.window2, text='ok', command=self.change_fs).grid(row=1, column=0, pady=20)
    def change_fs(self):
        self.window2.destroy()
        plt.rcParams['xtick.labelsize'] = float(self.fontsize.get())
        plt.rcParams['ytick.labelsize'] = float(self.fontsize.get())
        plt.rcParams['axes.labelsize'] = float(self.fontsize.get())
        plt.rcParams['legend.fontsize'] = float(self.fontsize.get())
    def on_close(self):
        plt.close('all')
        self.destroy()
        sys.exit()
    def update_entries(self,event):
        preset_values = {
                'Ce3+': (5 / 2, 6 / 7),
                'Pr3+': (4, 4 / 5),
                'Nd3+': (9 / 2, 8 / 11),
                'Pm3+': (4, 3 / 5),
                'Sm3+': (5 / 2, 2 / 7),
                'Eu3+': (0, 0), 'Gd3+': (7 / 2, 2), 'Tb3+': (6, 3 / 2), 'Dy3+': (15 / 2, 4 / 3), 'Ho3+': (8, 5 / 4),
                'Er3+': (15 / 2, 6 / 5), 'Tm3+': (6, 7 / 6), 'Yb3+': (7 / 2, 8 / 7)}
        selection = self.n0.get()
        if selection in preset_values:
            s, t = preset_values[selection]
            self.n.set(s)
            self.n1.set(t)
            
    def chi(self,n,T,B,dir,R,M=0):
        a1 = 0;a2 = 0;a3 = 0;a4 = 0;a5=0;a6=0
        H=0
#        j,g=preset_values[self.n0.get()]
        try:
            j=float(self.n.get())
        except ValueError:
            num,den=self.n.get().split('/')
            j=float(num)/float(den)
        try:
            g=float(self.n1.get())
        except ValueError:
            num, den = self.n1.get().split('/')
            g = float(num) / float(den)
        r = 0
        for i in range(3):
            for k in range(i + 2):
                H = H + n[r] * StevensOp(j, 2 * (i + 1), 2 * k)
                r = r + 1
        H=H-g*0.67171*(B+M)*dir(j)
#        +440 * M[1] * self.Jy(j) + 4.41 * M[2] * self.Jz(j)
#        H = 0.53 * StevensOp(5 / 2, 4, 0) + 0.53 * 5 * StevensOp(5 / 2, 4, 4) - g * 0.67171 * B * dir(5 / 2)
        eigenValues, eigenVectors = sp.linalg.eigh(H)
        idx = eigenValues.argsort()[::1]
        e = eigenValues[idx]
        #e=np.abs(e-e[0])
        f = eigenVectors[:,idx]

#        f = np.round(f, 7)
#        e = np.round(e, 2)
        for i in range(int(2 * j + 1)):
            a1 = a1 + np.exp(-e[i]/T)
            a2 = a2 +(np.abs(np.vdot(f[:, i], dir(j) @ f[:, i]))**2)*np.exp(-e[i]/T)/T
            #a3 = a3+(np.abs(np.conjugate(f[:, i]).dot(dir(j)).dot(f[:, i])) ** 1) * np.exp(-e[i]/T)
            a3 = a3 + np.vdot(f[:, i], dir(j) @ f[:, i]).real * np.exp(-e[i] / T)
            a4 = a4+ e[i] * np.exp(-e[i] / T)
            a5 = a5+ e[i] * e[i] * np.exp(-e[i] / T)
            for k in range(int(2 * j + 1)):
                if e[i] != e[k]:
                    a6 = a6+(np.abs(np.vdot(f[:, i], dir(j) @ f[:, k]))**2)*(np.exp(-e[i]/T)-np.exp(-e[k]/T))/(e[k]-e[i])
#                    a6 = a6 + (np.abs(np.conjugate(f[:, i]).dot(dir(j)).dot(f[:, k])) ** 2) * (np.exp(-e[k] / T) - np.exp(e[i]/T-2*e[k] / T)) / (e[k] - e[i])
        if R=='chivsT':
            result=a1/(0.375*g*g*(a2+a6))
        if R=='MvsH':
            #a3=np.abs(a3)
            result=g*a3/a1
        if R=='Cp':
            result=8.314 * (a1 * a5 - a4 * a4) / (T * T * a1 * a1)
        if R=='eigen':
            result=e,f
        return result
    def Jz(self,j):
        a = np.zeros((int(2 * j + 1), int(2 * j + 1)))
        for i in range(int(2 * j + 1)):
            a[i, i] = j - i
        return a

    def Jx(self,j):
        a = np.zeros((int(2 * j + 1), int(2 * j + 1)))
        for i in range(int(2 * j)):
            a[i, i + 1] = np.sqrt((i + 1) * (2 * j - i))
        return 0.5 * (a + a.T)

    def Jy(self,j):
        a = np.zeros((int(2 * j + 1), int(2 * j + 1)))
        for i in range(int(2 * j)):
            a[i, i + 1] = np.sqrt((i + 1) * (2 * j - i))
        return -0.5j * (a - a.T)
            
    def show_eigen(self):
        window = Toplevel(self)
        window.geometry('1000x500')
        window.attributes('-topmost', 'true')
        self.frame7 = tk.LabelFrame(window, text='Eigenvalues')
        self.frame7.place(x=0, y=0, height=50, width=1000)
        self.frame8 = tk.LabelFrame(window, text='Eigenvectors')
        self.frame8.place(x=0, y=50, height=500, width=1000)
        n=[float(self.n2[r].get()) for r in range(9)]
        e,f=self.chi(n,2,0,self.Jx,R='eigen',M=0)
        for widget in self.frame7.winfo_children():
            widget.destroy()
        for i, val in enumerate(e - e[0]):
            tk.Label(self.frame7, text=f"{val:.2f}").pack(side='left', padx=2)

        for widget in self.frame8.winfo_children():
            widget.destroy()
        for i, vec in enumerate(f.T):
            vec_str = ', '.join(f"{v:.4f}" for v in vec)
            tk.Label(self.frame8, text=f"v{i + 1} = [{vec_str}]").pack(anchor='w')
    def save(self):
        file = filedialog.asksaveasfilename(defaultextension='.cef',filetypes=[('CEF File', '*.cef'), ('All files', '*.*')])
        if file:
            filepath = os.path.abspath(file)
            with open(filepath, 'wb') as f:
                pickle.dump({
                "entries1": [var.get() for var in self.n2],
                "entries2": [var.get() for var in self.n14],
                "entries3": self.n.get(),"entries4": self.n1.get(),
                "entries5": [var.get() for var in self.n8],
                "entries6": [var.get() for var in self.n15],
                "checks1": [var.get() for var in self.n12],
                "checks2": [var.get() for var in self.n13],
                "combobox1": self.n0.get(),
                "array1": self.d,"array2": self.da,"array3": self.db,"array4": self.dc,
                "array5": self.d1a, "array6": self.d1b,"array7": self.d1c,}, f)

    def open(self):
        file = filedialog.askopenfile(mode='r',filetypes=[('CEF File', '*.cef'), ('All files', '*.*')])
        if file:
            filepath = os.path.abspath(file.name)
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            self.d = data["array1"]
            self.da = data["array2"]
            self.db = data["array3"]
            self.dc = data["array4"]
            self.d1a = data["array5"]
            self.d1b = data["array6"]
            self.d1c = data["array7"]
            self.n0.set(data.get("combobox1", ""))
            self.n.set(data.get("entries3", ""))
            self.n1.set(data.get("entries4", ""))
            for var, value in zip(self.n2,data.get("entries1", [])):
                var.set(value)
            for var, value in zip(self.n14, data.get("entries2", [])):
                var.set(value)
            for var, value in zip(self.n8, data.get("entries5", [])):
                var.set(value)
            for var, value in zip(self.n15, data.get("entries6", [])):
                var.set(value)
            for var, value in zip(self.n12, data.get("checks1", [])):
                var.set(value)
            for var, value in zip(self.n13, data.get("checks2", [])):
                var.set(value)

if __name__ == "__main__":
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10

    app = App()
    app.mainloop()