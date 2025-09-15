# CEF Analysis GUI

An interactive **Tkinter-based Python application** for simulating and fitting **crystal electric field (CEF) data**.  
The program computes **Schottky heat capacity**, **magnetic susceptibility**, and **magnetization** from **Stevens operators**, and allows **simultaneous fitting with experimental data**.  

Designed for researchers in **condensed matter physics** and **materials science**.  

## 📥 Download

1. Go to the repository:  
   👉 [CEF-Analysis-GUI](https://github.com/sumannandi-cmp/CEF-Analysis-GUI)  

2. Click the green **Code** button and select **Download ZIP**.  

3. Extract the ZIP file to a folder on your computer.  

4. Open a terminal (Command Prompt or PowerShell) in that folder.  

5. Run the application with:
   ```bash
   python app.py
   ```

---

## 📋 Requirements

- Python **3.8+**  
- Numpy, Scipy, Matplotlib
- lmfit
- Tkinter

Install Tkinter and lmfit with:
```bash
pip install tkinter
pip install lmfit
```

---

## 💻 How to Use

1. Start the application with:
```bash
python app.py
```
2. Prepare experimental datasets: `Cp(T)` (Schottky heat capacity), `χ(T)` (susceptibility for three field directions), and `M(H)` (magnetization for three field directions). Import data files from **File → Import**.
To plot experimental data, tick the checkbox in the **Experiment** column of the corresponding frame and click **Plot**.  
4. Select the ion and set initial Stevens operator parameters. Click **Diagonalise** to calculate CEF energy levels and eigenvectors.
5. To simulate a quantity, tick the checkbox in the **Theory** column of the corresponding frame and click **Plot**.
6. For simultaneous fitting, select models, choose nonzero parameters, and set fitting ranges.   
5. Perform fitting for `Cp(T)` and `χ(T)` for three directions individually or simultaneously. Fitted parameters will update automatically in the **CEF Parameters** frame. Use **Guess** if you want to change initial guesses and bounds.
7. To export simulated or fitted data, click **Export** below the plot window.
8. You can save the project with a `.cef` extension and reopen it later to avoid reloading data and parameters multiple times. Use **File → Save** or **File → Open**. 

---


## 🛠️ Features

- ✅ Calculate **CEF energy levels** from Stevens operators. 
- ✅ Calculate **Schottky heat capacity (Cp)**, **magnetic susceptibility (χ)** and **magnetization (M)** from Stevens operators.
- ✅ Import experimetal data as two column files.
- ✅ Fit simulations **simultaneously** to experimental datasets.
- ✅ Export processed data to text files.
- ✅ Simple **Tkinter-based GUI**.

---

## 📬 Contact

For questions, feedback, or bug reports:

- Email: [suman.nandi121998@gmail.com](mailto:suman.nandi121998@gmail.com)
