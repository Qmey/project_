import tkinter as tk
import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import ImageTk as itk
from PIL import Image
import subprocess


subprocess.run(['python', 'GUI.py'])

plt.style.use('ggplot')
window = tk.Tk()
window.title('Application')
window.configure(bg='#ffffff')

play_img = Image.open(r'C:\Users\Yerlan\PycharmProjects\Project\images\start.png')
logo = Image.open(r'C:\Users\Yerlan\PycharmProjects\Project\images\logo.png')
avatar = Image.open(r'C:\Users\Yerlan\PycharmProjects\Project\images\man.png')

logo_sz = logo.resize((300, 200))
play_img_sz = play_img.resize((300, 300))
avatar_img_sz = avatar.resize((200, 200))
play_fin_img = itk.PhotoImage(play_img_sz)
logo_fin_img = itk.PhotoImage(logo_sz)
avatar_fin_img = itk.PhotoImage(avatar_img_sz)

dataset_path = r'C:/Users/Yerlan/PycharmProjects/Project/Sample dataset/customers0.csv'

def excelprep(choice, path):
    df = pd.read_csv(dataset_path, encoding="utf-8", sep=';')
    for row in zip(df.CustomerId.unique()):
        xlxwriter = pd.ExcelWriter(path / str(str(row[0]) + 'customer_data.xlsx'),
                                   engine='xlsxwriter')  # define wb with writer fn
        workbook = xlxwriter.book
        worksheet1 = workbook.add_worksheet('Customer')

        formating = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'black'})
        worksheet1.set_column('A:A', 20)
        worksheet1.write('A1', 'Customer ID:', formating)
        worksheet1.write('B1', row[0])
        worksheet1.write('A2', 'Last Name:', formating)
        worksheet1.write('B2', df.loc[df['CustomerId'] == row[0], 'Last_Name'].unique()[0])
        worksheet1.write('A3', 'Date Of Birth:', formating)
        worksheet1.write('B3', df.loc[df['CustomerId'] == row[0], 'Age'].unique()[0])

        df[df.CustomerId == row[0]].to_excel(xlxwriter, sheet_name='Data', index=False)  # Adding data to sheet in excel
        worksheet2 = xlxwriter.sheets['Data']

        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({'categories': '=Data!$C$2:$C$3', 'values': '=Data!$D$2:$D$3'})
        worksheet2.insert_chart('A5', chart)
        xlxwriter.save()

def get_user_data(user_inputted):
    if user_inputted.isdecimal():
        user_input = int(user_inputted.strip())
        df = pd.read_csv(dataset_path, encoding="utf-8", sep=';')
        testing_occurence = df.loc[df['CustomerId'] == user_input]
        if len(testing_occurence) == 0:
            return ['There is no customer with this ID-number']
        else:
            CustomerID = user_input
            Last_name = df.loc[df['CustomerId'] == user_input, 'Last_Name'].unique()[0]
            CreditScore = df.loc[df['CustomerId'] == user_input, 'CreditScore'].unique()[0]
            Gender = df.loc[df['CustomerId'] == user_input, 'Gender'].unique()[0]
            Age = df.loc[df['CustomerId'] == user_input, 'Age'].unique()[0]
            arr_list = df.loc[df['CustomerId'] == user_input, 'arrayu'].unique()[0]
            return [CustomerID, Last_name, CreditScore, Gender, Age, arr_list]
    else:
        return ['There is no customer with this ID-number']

def openNewWindow():
    newWindow = tk.Toplevel(window)
    user_inputted = userinput.get()
    output_result = get_user_data(user_inputted)
    if len(output_result) > 1:
        newWindow.title(user_inputted + " detailed information")
        newWindow.geometry("430x450")
        tk.Label(newWindow, image=avatar_fin_img).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(newWindow, text="Customer ID:", font=('Helvetica', 18, 'bold'), foreground='blue').grid(row=1, column=0, padx=5, pady=5)
        tk.Label(newWindow, text=user_inputted, font=('Helvetica', 18)).grid(row=1, column=2, padx=5, pady=5)
        tk.Label(newWindow, text="Last Name:", font=('Helvetica', 18, 'bold'), foreground='blue').grid(row=2, column=0, padx=5, pady=5)
        tk.Label(newWindow, text=output_result[1], font=('Helvetica', 18)).grid(row=2, column=2, padx=5, pady=5)
        tk.Label(newWindow, text="Credit Score:", font=('Helvetica', 18, 'bold'), foreground='blue').grid(row=3, column=0, padx=5, pady=5)
        tk.Label(newWindow, text=output_result[2], font=('Helvetica', 18)).grid(row=3, column=2, padx=5, pady=5)
        tk.Label(newWindow, text="Gender:", font=('Helvetica', 18, 'bold'), foreground='blue').grid(row=4, column=0, padx=5, pady=5)
        tk.Label(newWindow, text=output_result[3], font=('Helvetica', 18)).grid(row=4, column=2, padx=5, pady=5)
        tk.Label(newWindow, text="Date of birth:", font=('Helvetica', 18, 'bold'), foreground='blue').grid(row=5, column=0, padx=5, pady=5)
        tk.Label(newWindow, text=output_result[4], font=('Helvetica', 18)).grid(row=5, column=2, padx=5, pady=5)

        button_plt = tk.Button(newWindow, text="Display credit health", width=15, height=1, fg="black", command=plotWindow)
        button_plt.config(font=('Helvetica', 18, 'bold'), borderwidth='1', highlightthickness=2, pady=2)
        button_plt.grid(row=7, column=0, padx=5, pady=5)
        button_plt = tk.Button(newWindow, text="Display spend history", width=15, height=1, fg="black", command=plotWindow_series)
        button_plt.config(font=('Helvetica', 18, 'bold'), borderwidth='1', highlightthickness=2, pady=2)
        button_plt.grid(row=7, column=2, padx=5, pady=5)
    else:
        newWindow.title("Error")
        newWindow.geometry("150x100")
        tk.Label(newWindow, text="Nothing found").pack()

def plotWindow():
    pltWindow = tk.Toplevel(window)
    pltWindow.title("Bar Chart Credit Score")
    pltWindow.geometry("500x500")
    user_inputted = userinput.get()
    output_result = get_user_data(user_inputted)
    x = [0, 2, 4]
    y = [0, output_result[2], 0]
    fig, ax = plt.subplots(1, 1)
    ax.bar(x, y, color='blue', alpha=0.7)
    ax.set_title(f'Contact:{output_result[1]}, Credit score is: {output_result[2]}', fontsize=20)
    ax.axhline(y=690, color='green', linestyle='--', label='Sufficient', linewidth=3)
    ax.axhline(y=300, color='red', linestyle='--', label='Unsufficient', linewidth=3)
    ax.set_ylabel('Credit score', fontsize=10)
    ax.legend(prop={'size': 14})
    ax.axes.xaxis.set_ticks([])
    canvas = FigureCanvasTkAgg(fig, master=pltWindow)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, pltWindow)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def plotWindow_series():
    pltWindow = tk.Toplevel(window)
    pltWindow.title("Expenditures per Period")
    pltWindow.geometry("500x500")
    user_inputted = userinput.get()
    output_result = get_user_data(user_inputted)
    x = ['2019', '2020', '2021', '2022']
    y = output_result[5].split(',')
    y_int = [int(i) for i in y]
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, y_int, color='blue', marker='o', linestyle='-', linewidth=2)
    ax.set_title(f'Expenditures of Customer: {output_result[1]}', fontsize=20)
    ax.set_ylabel('Total Spend', fontsize=10)
    ax.set_xlabel('Period', fontsize=10)
    canvas = FigureCanvasTkAgg(fig, master=pltWindow)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, pltWindow)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

frame = tk.Frame(window)
frame.grid(row=0, column=0)

tk.Label(frame, image=logo_fin_img).grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame, text="Welcome to Credit Scoring", font=('Helvetica', 20, 'bold')).grid(row=1, column=0, padx=5, pady=5)
tk.Label(frame, text="Enter Customer ID", font=('Helvetica', 18)).grid(row=2, column=0, padx=5, pady=5)

userinput = tk.Entry(frame, font=('Helvetica', 20))
userinput.grid(row=3, column=0, padx=5, pady=5)

button_login = tk.Button(frame, text="Search", command=openNewWindow, font=('Helvetica', 18, 'bold'))
button_login.grid(row=4, column=0, padx=5, pady=5)

window.mainloop()
