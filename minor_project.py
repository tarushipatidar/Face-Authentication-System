import sys
import tkinter as tk
from tkinter import Message, Text
import datetime as dt
import cv2
import os
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
from tkcalendar import DateEntry
import time
import smtplib
import psycopg2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pdb

subjects = [
    "OOSE",
    "Cloud_Computing",
    "E-Commerce",
    "Internet_and_Web_Technology"
]

dicti = {
    "OOSE": 'tarushipatidar123@gmail.com',
    "Cloud_Computing": "tarushipatidar123@gmail.com",
    "E-Commerce": "tarushipatidar123@gmail.com",
    "Internet_and_Web_Technology": "tarushipatidar123@gmail.com"
}


def newStudent():

    def clear1():
        txt1.delete(0, 'end')

    def clear2():
        txt2.delete(0, 'end')

    def clear3():
        txt3.delete(0, 'end')

    def takeimage():
        name = (txt1.get())
        email = (txt2.get())
        phone = (txt3.get())
        expiration_date = txt4.get()
        conn = psycopg2.connect(database = "gym_auth", user = "postgres", password = "postgres", host= 'localhost', port = 5432)
        cur = conn.cursor()
        cur.execute("SELECT nextval('people_id_seq')")
        next_id = str(cur.fetchone()[0] + 1)
        if(name and email and phone):
            cam = cv2.VideoCapture(0)
            face_haar_cascade = cv2.CascadeClassifier('/home/Tarushi.Patidar/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml')
            sampleNum = 0
            while(True):
                ret, img = cam.read()
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_haar_cascade.detectMultiScale(gray_img, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite("/home/Tarushi.Patidar/Downloads/face_regonition_attandance/image/"+'_'.join(name.split()) +"."+next_id +'.' +str(sampleNum) + ".jpeg", gray_img[y:y+h, x:x+w])
                    cv2.imshow('frame', img)
                if(cv2.waitKey(100) & 0xFF == ord('q')):
                    break
                elif(sampleNum > 60):
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Image saved for "+ name

            

            sql = "INSERT INTO people(name, email, phone, expiration_date) VALUES(%s, %s, %s, %s)"
            val = (name, email, phone, expiration_date)

            cur.execute(sql, val)

            conn.commit()
            cur.close()
            conn.close()

            row = [name, email, phone, expiration_date]
            with open('/home/Tarushi.Patidar/Downloads/face_regonition_attandance/data.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message1.configure(text=res)
        else:
            res = ''
            if not name:
                res += "Name can't be blank\n"
            if not email:
                res += "Email can't be blank\n"
            if not phone:
                res += "Phone can't be blank"
            message1.configure(text=res)

    def trainimage():
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_haar_cascade = cv2.CascadeClassifier('/home/Tarushi.Patidar/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml')
        faces, Id = getImageandLabel("/home/Tarushi.Patidar/Downloads/face_regonition_attandance/image")
        face_recognizer.train(faces, np.array(Id))
        face_recognizer.save("/home/Tarushi.Patidar/Downloads/face_regonition_attandance/Trainner.yml")
        res = "Image Trained"
        message1.configure(text=res)

    def getImageandLabel(path):
        imagePath = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        Ids = []
        for imgpath in imagePath:
            pilimage = Image.open(imgpath).convert('L')
            imagenp = np.array(pilimage, 'uint8')
            Id = int(os.path.split(imgpath)[-1].split(".")[1])
            faces.append(imagenp)
            Ids.append(Id)
        return faces, Ids

    window = tk.Toplevel()
    window.title("Face Recognition")
    window.geometry('13666x7688')
    window.configure(background='#E8F1E8')
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    message = tk.Label(window, text="Face Recognition Authentication System", bg="darkslategray", fg='White', width=100, height=3, font=('times', 30, 'italic bold underline'))
    message.place(x=0, y=0)

    back = tk.Button(window, text="Back", command=window.destroy, bg="silver", fg='black', activebackground="chocolate" ,width=5, height=1, font=('times', 15, 'bold'))
    back.place(x=0, y=0)

    lb1 = tk.Label(window, text="Enter Name", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb1.place(x=500, y=200)

    txt1 = tk.Entry(window, width=20, fg="Black", bg='White', font=('times', 25, 'bold'))
    txt1.place(x=850, y=200)

    lb2 = tk.Label(window, text="Enter Email", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb2.place(x=500, y=300)

    txt2 = tk.Entry(window, width=20, fg="Black", bg='White', font=('times', 25, 'bold'))
    txt2.place(x=850, y=300)

    lb3 = tk.Label(window, text="Enter Phone", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb3.place(x=500, y=400)

    txt3 = tk.Entry(window, width=20, fg="Black", bg='White', font=('times', 25, 'bold'))
    txt3.place(x=850, y=400)

    lb4 = tk.Label(window, text="Expiration Date", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb4.place(x=500, y=500)

    txt4 = DateEntry(window, width=31, background='darkblue', foreground='white', borderwidth=2)
    txt4.place(x=850, y=500)

    lb5 = tk.Label(window, text="Message", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb5.place(x=500, y=800)

    message1 = tk.Label(window, text="", bg="White", fg='black',activebackground="white" , width=58, height=5, font=('times', 15, 'bold'))
    message1.place(x=850, y=800)

    clearbutton = tk.Button(window, text="Clear", command=clear1, bg="silver", fg='black', activebackground="silver" , width=7, height=1, font=('times', 15, 'bold'))
    clearbutton.place(x=1250, y=200)
    clearbutton2 = tk.Button(window, text="Clear", command=clear2, bg="silver", fg='black',activebackground="silver" , width=7, height=1, font=('times', 15, 'bold'))
    clearbutton2.place(x=1250, y=300)
    clearbutton3 = tk.Button(window, text="Clear", command=clear3, bg="silver", fg='black',activebackground="silver" , width=7, height=1, font=('times', 15, 'bold'))
    clearbutton3.place(x=1250, y=400)
    Quit = tk.Button(window, text="Quit", command=root.destroy, bg="silver", fg='black',activebackground="chocolate" , width=7, height=1, font=('times', 15, 'bold'))
    Quit.place(x=1750, y=0)

    takeimg = tk.Button(window, text="Take Picture", command=takeimage, bg="silver", fg='black', activebackground="silver" , width=20, height=2, font=('times', 15, 'bold'))
    takeimg.place(x=850, y=600)
    trainimg = tk.Button(window, text="Train The Model", command=trainimage, bg="silver", fg='black', activebackground="silver" , width=20, height=2, font=('times', 15, 'bold'))
    trainimg.place(x=850, y=700)


def takeAttendance():

    def send_mail(filename, sub, todaysdate):
        email_user = 'tarushipatidar123@gmail.com'
        email_password = "vcundigrafqbdjhd"
        email_send = dicti[sub]
        subject = 'Attendance System'

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = 'Hi there, sending this email for '+sub+' subject on '+todaysdate+'!'
        msg.attach(MIMEText(body, 'plain'))

        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= "+filename)

        msg.attach(part)
        text = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)

        server.sendmail(email_user, email_send, text)
        server.quit()

    def trackImage():
        face_recognizer = cv2.face_LBPHFaceRecognizer.create()
        face_recognizer.read("/home/Tarushi.Patidar/Downloads/face_regonition_attandance/Trainner.yml")
        face_haar_cascade = cv2.CascadeClassifier('/home/Tarushi.Patidar/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml')
        df = pd.read_csv("/home/Tarushi.Patidar/Downloads/face_regonition_attandance/data.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        colname = ['Name', 'Email', 'Phone', 'Expiration Date']
        Attendance = pd.DataFrame(columns=colname)
        conn = psycopg2.connect(database = "gym_auth", user = "postgres", password = "postgres", host= 'localhost', port = 5432)
        cur = conn.cursor()
        while True:
            ret, img = cam.read()
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_haar_cascade.detectMultiScale(gray_img, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                Id, conf = face_recognizer.predict(gray_img[y:y+h, x:x+w])
                if conf < 35:
                    cur.execute("SELECT name, email, phone, expiration_date FROM people WHERE id = %s", (Id,))
                    result = cur.fetchone()
                    
                    if result is not None:
                        name, email, phone, expiration_date = result
                    else:
                        name, email, phone, expiration_date = '', '', '', None

                    current_date = datetime.datetime.now().date()

                    if expiration_date >= current_date:
                        status = '(Approved)'
                    else:
                        status = '(Expired)'

                    Attendance.loc[len(Attendance)] = [name, email, phone, expiration_date]
                else:
                    Id = 'Unknown'
                    name = ''
                    status = ''


                if Id != 'Unknown':
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    cur.execute("""
                        SELECT EXISTS (
                            SELECT 1 FROM people_auth 
                            WHERE person_id = %s AND DATE(checkin_date) = CURRENT_DATE
                        );
                    """, (Id,))
                    record_exists = cur.fetchone()[0]

                    if not record_exists:
                        sql = "INSERT INTO people_auth(person_id, checkin_date) VALUES(%s, %s)"
                        val = (Id, date)
                        cur.execute(sql, val)
                cv2.putText(img, name + ' ' + status, (x, y+h), font, 1, (255, 255, 255), 2)
            cv2.imshow('img', img)
            if(cv2.waitKey(1) == ord('q')):
                break
        
        conn.commit()
        cur.close()
        conn.close()
    
        res = 'Saved person data'
        message2.configure(text=res)
        cam.release()
        cv2.destroyAllWindows()


    window2 = tk.Toplevel()
    window2.title("Face Recognition")
    window2.geometry('13666x7688')
    window2.configure(background='#E8F1E8')
    window2.grid_rowconfigure(0, weight=1)
    window2.grid_columnconfigure(0, weight=1)

    message = tk.Label(window2, text="Face Recognition Authentication System", bg="darkslategray", fg='White', width=100, height=3, font=('times', 30, 'italic bold underline'))
    message.place(x=0, y=0)

    back = tk.Button(window2, text="Back", command=window2.destroy, bg="silver", fg='black', activebackground="chocolate", width=5, height=1, font=('times', 15, 'bold'))
    back.place(x=0, y=0)

    lb4 = tk.Label(window2, text="Status", width=20, height=2, fg="black", bg='sandybrown', font=('times', 15, 'italic bold underline'))
    lb4.place(x=450, y=400)

    message2 = tk.Label(window2, text="", bg="White", fg='black', activebackground="White", width=58, height=2, font=('times', 15, 'bold'))
    message2.place(x=800, y=400)

    trackimg = tk.Button(window2, text="Start Authentication", command=trackImage, bg="silver", fg='black', activebackground="silver" , width=20, height=2, font=('times', 15, 'bold'))
    trackimg.place(x=800, y=300)
    Quit = tk.Button(window2, text="Quit", command=root.destroy, bg="silver", fg='black', activebackground="chocolate", width=7, height=1, font=('times', 15, 'bold'))
    Quit.place(x=1750, y=0)


root = tk.Tk()
root.title("Face Recognition")
root.geometry('13666x7688')
dialog_title = 'Quit'
dialog_text = 'Are you Sure'
root.configure(background='#E8F1E8')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

message = tk.Label(root, text="Face Recognition Authentication System", bg="darkslategray", fg='White', width=100, height=3, font=('times', 30, 'italic bold underline'))
message.place(x=0, y=0)

newStu = tk.Button(root, text="Add Person Detail", command=newStudent, bg="silver", fg='black', activebackground="silver", width=20, height=2, font=('times', 15, 'bold'))
newStu.place(x=400, y=350)
takeAttendance = tk.Button(root, text="Authenticate People", command=takeAttendance, bg="silver", fg='black', activebackground="silver", width=20, height=2, font=('times', 15, 'bold'))
takeAttendance.place(x=1200, y=350)
Quit = tk.Button(root, text="Quit", command=root.destroy, bg="silver", fg='black', activebackground="chocolate", width=10, height=1, font=('times', 15, 'bold'))
Quit.place(x=850, y=500)

root.mainloop()

