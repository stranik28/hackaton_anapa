from time import sleep
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from PIL import Image
import sqlite3
import requests
import base64
import json
import numpy as np
import time
import matplotlib.pyplot as plt
import cv2
import io




url = "http://65.21.94.236:8006/object-to-img"
url2 = "http://65.21.94.236:8006/object-to-json"

# streamlit run main.py

def get_row(id):
    answ = []
    sqlite_connection = sqlite3.connect('hack.db')
    cursor = sqlite_connection.cursor()
    print("База данных создана и успешно подключена к SQLite")
    sql_select = "SELECT * FROM data WHERE cam_id = " + str(id) + ";";
    a = cursor.execute(sql_select)
    for i in a:
        answ = i
    print(answ)
    return answ

def get_rows():
    print("Hello")
    answ = []
    sqlite_connection = sqlite3.connect('hack.db')
    cursor = sqlite_connection.cursor()
    print("База данных создана и успешно подключена к SQLite~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    sql_select = "SELECT * FROM data;"
    a = cursor.execute(sql_select)
    for i in a:
            print(str(i) + " ")
            answ.append(i)
    return answ


with st.sidebar:
  options = ["Welcome Page","dashboard","cams","reports", "map"]
  selected = option_menu(
    menu_title = "Main menu",
    options = options,
  )

def dash_page():
    st.title("Dashboard")
    select_arr = ["Стадия наполенния", "Наполенена",
                  "Негабаритный мусор","Рядом дворник"]
    artists = st.multiselect("Выберите статусы камер", select_arr)
    # ids = [1, 2, 3, 4]
    # times = [10, 20, 30, 40]
    # dates = ['01-08-2020', '01-08-2020', '01-08-2020', '01-08-2020']
    # statuss = ['Стадия наполенния', 'Наполнена', 'Много негаборитного мусора', "Стадия наполнения" ]
    print(len(artists))
    status = []
    times = []
    ids = []
    addresses = []
    dates = []
    if len(artists) > 0:
        for i in get_rows():
            statuss = i[2]
            if statuss == 5:
                statuss = "Стадия наполенния"
            elif statuss == 1:
                statuss = "Наполенена"
            elif statuss == 2:
                statuss = "Замусорено"
            elif statuss == 4:
                statuss = "Рядом дворник"
            else:
                statuss = "Негабаритный мусор"
            print(artists)
            print(statuss)
            if statuss == artists[0] :
                addresses.append(i[5])
                ids.append(i[1])
                times.append(i[4])
                dates.append(i[3])
                status.append(statuss)
    else:
        for i in get_rows():
            statuss = i[2]
            addresses.append(i[5])
            ids.append(i[1])
            times.append(i[4])
            dates.append(i[3])
            if statuss == 5:
                status.append("Стадия наполенния")
            elif statuss == 1:
                status.append("Наполенена")
            elif statuss == 2:
                status.append("Замусорено")
            elif statuss == 4:
                status.append("Рядом дворник")
            else:
                status.append("Негабаритный мусор")

    # addresses = ['Address', 'Giros 10', 'Kolina 12', 'John 10']
    df = pd.DataFrame({
    'Camera number ': ids,
    'Time': times,
    'Date': dates,
    'Status': status,
    'Address': addresses
    })
    st.write(df)

def cams():
    placeholder = st.empty()
    select_arr = []
    for i in range(0,100):
        select_arr.append(i)
    artists = st.selectbox("Выберете номер камеры для просмотра отчета", select_arr)
    st.title(f"Информация по {artists} камере")
    a = 0
    datas = get_row(artists)
    timee = datas[4]
    date = datas[3]
    address = datas[5]
    status = datas[2]
    file = {'file': open('ansver/'+str(artists)+'/-1.jpg', "rb")}
    resp = requests.post(url,files=file)
    with io.open("ansver/"+str(artists)+"/1.jpg", 'wb') as file:
        file.write(resp.content)
    photo = Image.open('ansver/'+str(artists)+'/1.jpg')
    st.write(f"**Текущий статус камеры:** *{status}* ")
    st.write(f"**Последнее время обновления:** *{timee}* ")
    st.write(f"**Адресс:** *{address}* ")
    img_file = open('ansver/'+str(artists)+'/1.jpg', 'wb')
    img_file.write(resp.content)
    img_file.close()
    st.image(photo, caption =f"*{date}*")

def reports():
    select_arr = ["Круговая диаграма"]
    artists = st.selectbox("Выбирете тип отчета", select_arr)
    if artists == "Круговая диаграма":
        labels = "Стадия наполенния", "Наполнена","Много негаборитного мусора","Вынос мусора"
        sizes = [100, 30, 45, 10]
        explode = (0, 0, 0, 0.1)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)

    

def map():
    df = pd.DataFrame(
    np.random.randn(70, 2) / [230, 230] + [44.89038980, 37.31090108],
    columns=['lat', 'lon'])
    st.map(df)



if selected == "Welcome Page":
  st.title(f"Пожалуйста выберете раздел 👈")
elif selected == "dashboard":
  dash_page()
elif selected == "cams":
  cams()
elif selected == "map":
    map()
else:
  reports()

