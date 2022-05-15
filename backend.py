import requests
import cv2
import json
import os
import base64
from datetime import datetime
import sqlite3

url = "http://65.21.94.236:8006/object-to-json"

video_path = "41"


def prepare_for_db(typ, arr):
    with open("buf/1.jpg", "rb") as image_file:
        photo = base64.b64encode(image_file.read())
    time = datetime.now()
    data = datetime.today().strftime('%d-%m-%y')
    # print(data)
    time = time.strftime("%H:%M")
    address = "Анапская 10"
    coardinates = "44.89038980348887, 37.31090108754396"
    prev_datas = [0,0,0,0,0,0,0,0,0,0,0]
    if not os.path.exists("ansver/"+video_path+"/fake"):
            os.makedirs("ansver/"+video_path+"/fake", exist_ok=False)
    for i in range(0,9):
        cv2.imwrite("ansver/"+video_path+"/fake/"+str(i)+".jpg",arr[i])
        with open("buf/2.jpg", "rb") as image_file:
            prev = base64.b64encode(image_file.read())
        prev_datas[i] = prev
    try:
        sqlite_connection = sqlite3.connect('hack.db')
        cursor = sqlite_connection.cursor()
        # print("База данных создана и успешно подключена к SQLite")
        sql_select = "SELECT * FROM data WHERE cam_id = " + video_path + ";";
        a = cursor.execute(sql_select)
        f = []
        for i in a:
            f.append(i)
        # print(len(f))
        # print(data)
        if len(f) == 0:
            sql_insert = "INSERT INTO data(cam_id,type,dat,time,address,location,photos,photo)" + " VALUES('"+video_path+"',"+str(typ)+",'"+str(data)+"','"+str(time)+"','"+str(address)+"','"+coardinates+"',1,'" + "ansver/"+video_path+"/');"
        else:
            sql_insert = "UPDATE data SET type = " + str(typ) + " , time = '" + str(time) + "' , dat = '"+ str(data) + "' WHERE cam_id = " + video_path +";"
        
        cursor.execute(sql_insert)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            # print("Соединение c SQLite закрыто")
        apoadspo = ""

    if not os.path.exists("garbage/"+video_path):
        os.makedirs("ansver/"+video_path, exist_ok=False)
    print("Done")




def rev(arr):
    arr[0] = arr[1]
    arr[1] = arr[2]
    arr[2] = arr[3]
    arr[3] = arr[4]
    arr[4] = arr[5]
    arr[5] = arr[6]
    arr[6] = arr[7]
    arr[7] = arr[8]
    return arr


def get_video():
    sqlite_connection = sqlite3.connect('hack.db')
    cursor = sqlite_connection.cursor()
    # print("База данных создана и успешно подключена к SQLite")
    sql_select = "SELECT type FROM data WHERE cam_id = " + video_path + ";";
    a = cursor.execute(sql_select)
    cap = cv2.VideoCapture("videos/"+video_path+".avi")
    st = 0
    for i in a:
        st = i[0]
    n = 0
    if not os.path.exists("garbage/"+video_path):
        os.makedirs("garbage/"+video_path, exist_ok=False)

    arr = [0,0,0,0,0,0,0,0,0,0]


    while True: 
        ret, frame = cap.read()
        if cv2.cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif frame is None:
            break
        if n % 3 == 0:
            arr = rev(arr)
            arr[9] = frame 
        if n%21 == 0:
            n/=21   
            cv2.imwrite(r'buf/1.jpg',frame)

            cv2.imwrite(r'ansver/'+video_path+'/-1.jpg',frame)
            file = {'file': open('buf/1.jpg', "rb")}
            resp = requests.post(url,files=file)
            resp = json.loads(resp.text)
            l = 5
            for i in resp["result"]:
                l = min(l,i["class"])
                if(i["class"] != st):
                    st = i["class"]
                    next_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    cv2.imwrite(r'garbage/'+video_path+"/"+str(n)+'.jpg',frame)
                    prepare_for_db(typ = l,arr = arr)
                    break
        n+=1
    print("End")


get_video()