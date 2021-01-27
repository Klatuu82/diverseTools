import smtplib
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime


def find_content():

    url = "https://bremen1860.de/sportangebot/membersonly"
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


def send_email(link):
    fromaddr = 'diverstools193@gmail.com'
    toaddrsme = 'dausmarcel@hotmail.com'
    toaddrsshe = 'nirmalanoormann@web.de'
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
    server.sendmail(fromaddr, toaddrsme, msg)
    server.sendmail(fromaddr, toaddrsshe, msg)
    server.quit()
    return True


count = 1
while True:
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Anwendung läuft " + current_time)
        found, link = find_content()
        print("Gefunden: " + str(found))
        print("Link: " + link)
        if found:
            send_email(link)
            break
        time.sleep(30)
    except:
        print(str(count) + ". Fehler")
        count += 1

    if count >= 10:
        break
