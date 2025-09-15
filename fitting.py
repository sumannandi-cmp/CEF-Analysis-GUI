import numpy as np
import tkinter as tk
from tkinter import Toplevel, Frame, Button,filedialog
import threading
from lmfit import Model, Parameters, minimize


class CEFFit:
    @classmethod
    def guess(cls,app):
        window = tk.Toplevel(app)
        window.geometry('400x500')
        window.attributes('-topmost', 'true')
        tk.Label(window, text='Initial Guess').grid(row=0, column=1, pady=5)
        tk.Label(window, text='Bounds').grid(row=0, column=2, padx=10)
        selected = ['B_20','B_22','B_40','B_42','B_44','B_60','B_62','B_64','B_66','l_1','l_2','l_3']

        new_var=[]
        k=1
        for label_text in selected:
            tk.Label(window, text=label_text).grid(row=k,column=0,pady=5)

            var = tk.StringVar(value=app.n15[2*(k-1)].get())

            new_var.append(var)
            tk.Entry(window, textvariable=var).grid(row=k, column=1,padx=10)

            var = tk.StringVar(value=app.n15[2*k-1].get())

            new_var.append(var)
            tk.Entry(window, textvariable=var).grid(row=k, column=2, padx=10)
            k=k+1
        app.n15=new_var
        tk.Button(window, text='Ok', command=window.destroy).grid(row=14, column=1,pady=10)
    
    @classmethod
    def start_fitting(cls,app):
        app.status_label.config(text="Fitting in progress...",foreground="red")
        app.fit_button.config(state='disabled')  # optional: disable button
        threading.Thread(target=cls.fit_thread, args=(app,), daemon=True).start()
    
    @classmethod
    def fit_thread(cls,app):
        try:
            cls.fit(app)
            app.after(0, cls.plot_fit(app))
        except Exception as e:
            print("Fitting error:", e)
            app.status_label.config(text="Fitting failed!")
    
    @classmethod
    def plot_fit(cls,app):
        app.status_label.config(text="Fitting complete.",foreground="green")
        app.fit_button.config(state='normal')
    
    @classmethod
    def fit(cls,app):

        #selected_params=[params[i] for i,var in enumerate(app.n12) if var.get()]

        def inv_chi_x(T,n1,n2,n3,n4,n5,n6,n7,n8,n9,l1,l2,l3):
            m = []
            n = [n1,n2,n3,n4,n5,n6,n7,n8,n9]
            for i in T:
                #m.append(i)
                m.append(app.chi(n,i,10 ** (-9),app.Jx,'chivsT') - l1)
            return m
        def inv_chi_y(T,n1,n2,n3,n4,n5,n6,n7,n8,n9,l1,l2,l3):
            m = []
            n = [n1, n2, n3, n4, n5, n6, n7, n8, n9]
            for i in T:
                m.append(app.chi(n,i,10 ** (-9),app.Jy,'chivsT') - l2)
            return m
        def inv_chi_z(T,n1,n2,n3,n4,n5,n6,n7,n8,n9,l1,l2,l3):
            m = []
            n = [n1, n2, n3, n4, n5, n6, n7, n8, n9]
            for i in T:
                m.append(app.chi(n,i,10 ** (-9),app.Jz,'chivsT') - l3)
            return m
        def CMag(T,n1,n2,n3,n4,n5,n6,n7,n8,n9,l1,l2,l3):
            m = []
            n = [n1, n2, n3, n4, n5, n6, n7, n8, n9]
            for i in T:
                m.append(app.chi(n,i,0,app.Jz,'Cp'))
            return m


        '''x_data1 = data[:, 0][0:]
        y_data1 = data[:, 1][0:]
        x_data2 = data[:, 2][0:]
        y_data2 = data[:, 3][0:]
        x_data3 = data[:, 4][0:]
        y_data3 = data[:, 5][0:]
        data = np.genfromtxt('Cmag++.txt', skip_header=0)
        x_data4 = data[:, 1][0:]
        y_data4 = data[:, 0][0:]'''
        
        param_names = ['n1', 'n2', 'n3', 'n4', 'n5','n6','n7','n8','n9', 'l1', 'l2', 'l3']
        params = Parameters()
        for i in range (9):
            if app.n12[i].get():
                params.add(param_names[i], value=float(app.n15[2*i].get()), min=float(app.n15[2*i+1].get().split(',')[0]), max=float(app.n15[2*i+1].get().split(',')[1]))
            else:
                params.add(param_names[i],value=0,vary=False)
        params.add('l1', value=0, vary=False)
        params.add('l2', value=0, vary=False)
        params.add('l3', value=0, vary=False)

        def objective_function(params, *args):
            param_values = [params[name] for name in param_names]
            i=0
            residuals=[]
            if app.n13[0].get():
                residuals.append(np.array(inv_chi_x(args[i], *param_values))-np.array(args[i+1]))
                i=i+2
            if app.n13[1].get():
                residuals.append(np.array(inv_chi_y(args[i], *param_values)) - np.array(args[i + 1]))
                i = i + 2
            if app.n13[2].get():
                residuals.append(np.array(inv_chi_z(args[i], *param_values)) - np.array(args[i + 1]))
                i = i + 2
            if app.n13[3].get():
                residuals.append(np.array(CMag(args[i], *param_values)) - np.array(args[i + 1]))
            return np.concatenate(residuals)

        args=[]
        if app.n13[0].get():
            indices = np.where((app.da[:, 0] >= float(app.n14[0].get().split(',')[0])) & (app.da[:, 0] <= float(app.n14[0].get().split(',')[1])))
            x_data1=app.da[:,0][indices]
            y_data1=app.da[:,1][indices]
            params['l1'].set(value=float(app.n15[18].get()), vary=True, min=float(app.n15[19].get().split(',')[0]), max=float(app.n15[19].get().split(',')[1]))
            args.extend([x_data1, y_data1])
        if app.n13[1].get():
            indices = np.where((app.db[:, 0] >= float(app.n14[1].get().split(',')[0])) & (app.db[:, 0] <= float(app.n14[1].get().split(',')[1])))
            x_data2 = app.db[:, 0][indices]
            y_data2 = app.db[:, 1][indices]
            params['l2'].set(value=float(app.n15[20].get()), vary=True, min=float(app.n15[21].get().split(',')[0]), max=float(app.n15[21].get().split(',')[1]))
            args.extend([x_data2, y_data2])
        if app.n13[2].get():
            indices = np.where((app.dc[:, 0] >= float(app.n14[2].get().split(',')[0])) & (app.dc[:, 0] <= float(app.n14[2].get().split(',')[1])))
            x_data3 = app.dc[:, 0][indices]
            y_data3 = app.dc[:, 1][indices]
            params['l3'].set(value=float(app.n15[22].get()), vary=True, min=float(app.n15[23].get().split(',')[0]), max=float(app.n15[23].get().split(',')[1]))
            args.extend([x_data3, y_data3])
        if app.n13[3].get():
            indices = np.where((app.d[:, 0] >= float(app.n14[3].get().split(',')[0])) & (app.d[:, 0] <= float(app.n14[3].get().split(',')[1])))
            x_data4 = app.d[:, 0][indices]
            y_data4 = app.d[:, 1][indices]
            args.extend([x_data4, y_data4])
        result = minimize(objective_function, params,args=tuple(args))
        values=list(result.params.values())
        for i in range(9):
            app.n2[i].set(f"{values[i].value:.5f}")
        for i in range(3):
            app.n8[i].set(f"{values[9+i].value:.2f}")