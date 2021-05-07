import smtplib
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("ACHTUNG!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def find_content(url):

    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    divs = soup.find_all("div", class_="kids_box")
    link = "https://bremen1860.de"
    for div in divs:

        if "Kinderbewegungszentrum" in div.text:
            link += (div.find("a").get('href'))
            return True, link

        # for testing
        # if "Sportgymnastik" in div.text:
        #     link += (div.find("a").get('href'))
        #     return True, link

    return False, link


def isNewContent(count):

    html_content = requests.get("https://bremen1860.de/sportangebot/membersonly_buchung/6/?nocache=1").text
    soup = BeautifulSoup(html_content, "html.parser")
    inputs = soup.find_all("input", class_="radcaltimemo")
    if count < len(inputs):
        return len(inputs), True

    return len(inputs), False


def send_email(link):
    emailList = ['dausmarcel@hotmail.com', 'nirmalanoormann@web.de', 'moniquekunkel@web.de', 'lena.koehler@posteo.de']
    fromaddr = 'diverstools193@gmail.com'
    msg = "\r\n".join([
        "From: user_me@gmail.com",
        "To: user_you@gmail.com",
        "Subject: Bremen 1860 gogo",
        "",
        link
    ])
    username = 'diversetools193@gmail.com'
    password = '#Geheim1*'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    for email in emailList:
        server.sendmail(fromaddr, email, msg)
        print(email)
    server.quit()
    return True


def get_content(url):

    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    divs = soup.find_all("div", class_="caltext")
    link = "https://bremen1860.de"
    text = []
    labels = divs[0].find_all("label")
    for label in labels:
        text.append(label.text)


    return text

def seek():
    count = 0
    size = 0
    firstStart = True
    while True:
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Anwendung läuft " + current_time)
            found, link = find_content("https://bremen1860.de/sportangebot/membersonly")
            print("Gefunden: " + str(found))
            if found:
                size, isNew = isNewContent(size)
                print("Anzahl der Termine: " + str(size))
                if isNew:
                    if firstStart:
                        firstStart = False
                        continue
                    print("Neuer Termin!")
                    send_email(link)
                    time.sleep(300)
            if firstStart:
                firstStart = False
                continue
        except:
            print(str(count) + ". Fehler")
            count += 1

        time.sleep(30)
        if count >= 10:
            break

seek()
# popupmsg("Was ist wenn wir diesen Text sehr lang machen")
# print(get_content("https://bremen1860.de/sportangebot/membersonly_buchung/9/?nocache=1"))