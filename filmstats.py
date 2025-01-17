import csv
import pandas as pd
from tkinter import *
from tkinter import ttk
import tkinter as tk

import plotly
import plotly.express as px
import plotly.graph_objs as go

df = pd.read_csv("imdb.csv")
#print(type(df["Genre"][0]))
root = tk.Tk()
root.title("Films")


def film_year(): # эта функция показывает график кол-ва фильмов и сериалов выпущенных в выбранный временой промежуток
    year_df = df 
    a = eval(date_st.get())
    b = eval(date_end.get())
    year_df = year_df.loc[(year_df["Date"] >= a) & (year_df['Date']<=b)]
    year_df = year_df.reset_index(drop = True)
    df_res = year_df.groupby([year_df.Date, year_df.Type]).size()   
    try_ = df_res.unstack(level=-1)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x = try_.index, y = try_.Film, name = "Films", ))
    fig.add_trace(go.Bar(x = try_.index, y = try_.Series, name  = "Series"))
    fig.update_layout(yaxis_title="Count", xaxis_title="Year")
    return fig.show()


def get_list(): #получить список фильмов и сериалов с определенным показателем одного из предупреждений (Насилие, алкоголь и тд)
    year_df = df
    input_type = trig_warning.get()
    rating = trig_type.get()
    year_df = year_df.loc[(year_df[input_type] == rating)]
    year_df = year_df.reset_index(drop = True)
    file = open("Recommendations.txt", 'w', encoding="utf-8")
    for i in range (len(year_df)):
       file.write(year_df.loc[i,:].values[0] + " —— " + str(year_df.loc[i,:].values[1]) + f"({year_df.loc[i,:].values[6]})" + '\n')
    label_warn.config(text="Check the program folder")

def input_graph_check():
    start = date_st.get()
    end = date_end.get()
    if start.isdigit() & end.isdigit():
        start = eval(start)
        end = eval(end)
        if (start <= end) & (end < 2024) & (start > 1921):
            film_year()
        else:
            label_warn_gr.config(text="Dates are not within value limits")
    else:
        label_warn_gr.config(text="Incorrect input, numbers only")

#кнопки для дат графа
label_warn = tk.Label(root, text="Input time period from 1922 to 2023")
label_warn.pack()

date_st = tk.Entry(root)
date_st.pack()
date_end = tk.Entry(root)
date_end.pack()

button_get= tk.Button(root, text = "Get chart", command=input_graph_check)
button_get.pack()
label_warn_gr = tk.Label(root, text="")
label_warn_gr.pack()



options = ['None','Mild', 'Moderate', 'Severe']
options_type = ['Nudity', 'Violence', 'Profanity', 'Alcohol', 'Frightening']

#кнопки для фильмов с ограничением по триггер ворнингам
trig_warning = ttk.Combobox(values=options_type, state="readonly" )
trig_warning.pack()
trig_type = ttk.Combobox(values=options, state="readonly")
trig_type.pack()

button_tr= tk.Button(root, text = "Get films & series list", command=get_list)
button_tr.pack()    

label_warn = tk.Label(root, text="")
label_warn.pack()
root.mainloop()

