import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import requests
import tkinter as tk
from tkinter import *
import ctypes
import smtplib
import mysql.connector
from selenium import webdriver
import chromedriver_binary
import urllib 
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen  #news accessing youtub videos
from google_images_download import google_images_download    #image retrival
from ecapture import ecapture as ec   #take photo
from win10toast import ToastNotifier     #reminder
from datetime import datetime  #reminder
import pyjokes
import winshell
import bcrypt



pos = N

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


#database connection 
def conn():
   mydb=mysql.connector.connect(host="localhost",user="root",password="",database="burpy")
   if(mydb):
       print("connection success")
   else:
        print("connection failed")
   mycursor=mydb.cursor();
   mydb.commit()


#database insert
def insert(u_id,action,query):
    mydb=mysql.connector.connect(host="localhost",user="root",password="",database="burpy1")
    mycursor=mydb.cursor()
    s = "Insert into action (u_id,action_name,voice_text) values (%s,%s,%s)"
    t = (u_id,action,query)
    mycursor.execute(s,t)
    mydb.commit()
    



def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour=int(datetime.now().hour)
    if hour>=4 and hour<12:
        speak("good morning")
    elif hour>=12 and hour<18:
        speak("good afternoon")
    elif hour >=18 and hour <22:
        speak("good evening")
    else:
        speak("its sleep time , may be we should meet at morning!")
    speak("sir , its burpy at your service")
    speak("how can i help you?")

def info() :
    mydb=mysql.connector.connect(host="localhost",user="root",password="",database="burpy1")
    mycursor=mydb.cursor()
    a="select * from detail where u_id = %s"
    x=(setid,)
    mycursor.execute(a,x)
    inf = mycursor.fetchone()
    InsertText(inf)

def takeCommand():
    r=sr.Recognizer() 
    with sr.Microphone() as source:
        #print("Listenning..")
        r.pause_threshold=1
        audio = r.listen(source)
    try:
        print("recognizing...")
        query = r.recognize_google(audio,language='en-in')
        print(f"user said :{query}\n")
        a = "\nUser said : "+query +"\n" 
        InsertText(a);
    except Exception as e:
        print(e)
        speak("i cant recognize , please , say that again ")
        query = takeCommand()
    return query

def validate_time(alarm_time):
    if len(alarm_time) != 11:
        return "Invalid time format! Please try again..."
    else:
        if int(alarm_time[0:2]) > 12:
            return "Invalid HOUR format! Please try again..."
        elif int(alarm_time[3:5]) > 59:
            return "Invalid MINUTE format! Please try again..."
        elif int(alarm_time[6:8]) > 59:
            return "Invalid SECOND format! Please try again..."
        else:
            return "ok"

def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('yakshsoni10@gmail.com','9737136362')
    server.sendmail('yakshsoni10@gmail.com',to,content)
    server.close()

def InsertText(text):
    output.insert(tk.INSERT,text)

def click():                   #once click on NAME button
    entered_text = textentry.get()   #stored data in text box
    definition = "Hello " +str(entered_text)+ " I'm Burpy your virtual assistant\npress Mic and ask for anything"
    output.insert(END,definition)

    # output.insert(END,definition)
    speak(definition)
    nameButton = Button(window, text= "Enter your Name", width = 20, command = click, fg = "#272324", bg= "#A9A9A9",state="disabled").grid(row=3, column=0 ,sticky=pos,pady=10)
def refresh():                   #once click on ASK button
    definition = "I'm listening.."
    InsertText(definition)
    speak(definition)
    main()


def convertTuple(tup):
    str =  ''.join(tup)
    return str

def login_user():
    global setid
    username_info = username.get()
    password_info = password.get().encode('utf-8')
    pwd = b'$2b$12$1PRMKFSp6DzvGFROcEyf0.'
    
    mydb=mysql.connector.connect(host="localhost",user="root",password="",database="burpy1")
    mycursor=mydb.cursor()
    a = "Select password from user_login where u_name = %s"
    x = (username_info,)
    mycursor.execute(a,x)
    passd = convertTuple(mycursor.fetchone())
    
    #print(passd)
    pw = str(bcrypt.hashpw(password_info,pwd))
    pwf = pw[2:-1]
    #print(pwf)
    if pwf == passd :
        print("compared")
        s = "Select u_name,password from user_login"
        mycursor.execute(s)
        unmpwd = mycursor.fetchall()
        #print(unmpwd)
        for result in unmpwd :
        
            if result == (username_info,pwf) :
                s = "Select u_id from user_login where (u_name,password)=(%s,%s)"
                t = (username_info,pwf)
                mycursor.execute(s,t)
                fetch = mycursor.fetchone()
                setid = fetch[0]
                print(setid)
                Label(screen1, text = "Login success , now open", fg = "#adf542" ,bg="black",font = ("calibri", 13)).pack()
                Button(text = "Open",height = "2", width = "30", command = main_window).pack()
                close_win()
                break
        
   
def close_win():
    screen1.destroy()


def encrypt_pwd(pwd):
    return bcrypt.hashpw(pwd,b'$2b$12$1PRMKFSp6DzvGFROcEyf0.')

def register_user():

  username_info = username.get()
  contact_info = contact.get()
  address_info = address.get()
  email_info = email.get()
  global password_info 
  password_info =  encrypt_pwd(password.get().encode('utf-8'))

  mydb=mysql.connector.connect(host="localhost",user="root",password="",database="burpy1")
  mycursor=mydb.cursor()
  q = "Insert into user_login (u_name,password) values (%s,%s)"
  r = (username_info,password_info)
  mycursor.execute(q,r)
  mydb.commit()
  s = "Insert into detail (address,contact,u_email) values (%s,%s,%s)"
  t = (address_info,contact_info,email_info)
  mycursor.execute(s,t)
  mydb.commit()
  username_entry.delete(0, END)
  contact_entry.delete(0, END)
  address_entry.delete(0, END)
  email_entry.delete(0, END)
  password_entry.delete(0, END)

  Label(screen1, text = "Registration Success", fg = "#adf542" ,bg="black",font = ("calibri", 11)).pack()
  Label(screen1, text = "\nNow Login", fg = "#adf542" ,bg="black",font = ("calibri", 13)).pack()
  close_win()
  
  

def register():
  global screen1
  screen1 = Toplevel(screen)
  screen1.title("Register")
  screen1.configure(bg="black")
  screen1.geometry("300x420")
  
  global username
  global password
  global contact
  global email
  global address
  global username_entry
  global contact_entry
  global email_entry
  global address_entry
  global password_entry
  username = StringVar()
  contact = StringVar()
  address = StringVar()
  email = StringVar()
  password = StringVar()

  Label(screen1, text = "Please enter details below",fg="white",bg="#000000").pack()
  Label(screen1, text = "",bg="black").pack()
  Label(screen1, text = "Username * ",fg="white",bg="#000000").pack()
  username_entry = Entry(screen1, textvariable = username)
  username_entry.pack()
  Label(screen1, text = "Contact * ",fg="white",bg="#000000").pack()
  contact_entry = Entry(screen1, textvariable = contact)
  contact_entry.pack()
  Label(screen1, text = "Address * ",fg="white",bg="#000000").pack()
  address_entry = Entry(screen1, textvariable = address)
  address_entry.pack()
  Label(screen1, text = "E-mail * ",fg="white",bg="#000000").pack()
  email_entry = Entry(screen1, textvariable = email)
  email_entry.pack()
  Label(screen1, text = "Password * ",fg="white",bg="#000000").pack()
  password_entry =  Entry(screen1, textvariable = password,show="*")
  password_entry.pack()
  Label(screen1, text = "",bg="black").pack()
  Button(screen1, text = "Register", width = 10, height = 1, command = register_user).pack()


def login():
  global screen1
  global username
  global password
  global username_entry
  global password_entry
  screen1 = Toplevel(screen)
  screen1.configure(bg="#000000")
  screen1.title("Login")
  screen1.geometry("300x250")
  username = StringVar()
  password = StringVar()

  Label(screen1, text = "Please enter details below",fg="white",bg="#000000").pack()
  Label(screen1, text = "",bg="black").pack()
  Label(screen1, text = "Username * ",fg="white",bg="#000000").pack()
  username_entry = Entry(screen1, textvariable = username)
  username_entry.pack()
  Label(screen1, text = "Password * ",fg="white",bg="#000000").pack()
  password_entry =  Entry(screen1, textvariable = password,show="*")
  password_entry.pack()
  Label(screen1, text = "",bg="black").pack()
  Button(screen1, text = "Login", width = 10, height = 1, command = login_user,fg="#000000",bg="white").pack()

def main_screen():
  global screen
  screen = Tk()
  screen.geometry("300x250")
  screen.configure(bg="#000000")
  screen.title("Burpy")
  Label(text = "Burpy", bg = "#000000",fg="white", width = "300", height = "2", font = ("Calibri", 13)).pack()
  Label(text = "",bg="black").pack()
  Button(text = "Login", height = "2", width = "30", command = login,fg="#000000",bg="white").pack()
  Label(text = "",bg="black").pack()
  Button(text = "Register",height = "2", width = "30", command = register,fg="#000000",bg="white").pack()

  screen.mainloop()

def main():
    output.delete('1.0',END)

    query = takeCommand().lower()
    while (query!='none'):
    

        if 'wikipedia' in query:
            action = "wikipedia"
            insert(setid,action,query)
            speak("searching wikipidea")
            query = query.replace("wikipedia","").replace("according","").replace("to","")
            results = wikipedia.summary(query,sentences=2)
            InsertText(results)
            speak("According to wikipedia")
            #print(results)
            speak(results)
            break

        elif 'on youtube' in query:
            action = "on youtube"
            insert(setid,action,query)
            b="Which video?"
            InsertText(b)
            speak("Which video?")
            search_keyword=takeCommand().replace(" ","+")
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
            video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            driver=webdriver.Chrome()
            driver.get("http://www.youtube.com/watch?v="+video_id[0])
            break
        
        elif 'open google' in query:
            action = "open google"
            insert(setid,action,query)
            driver=webdriver.Chrome()
            driver.get("http://www.google.com")
            break

        elif 'open youtube' in query:
            action = "open youtube"
            insert(setid,action,query)
            driver=webdriver.Chrome()
            driver.get("http://www.youtube.com")
            break

        elif 'play music' in query:
            action = "play music"
            insert(setid,action,query)
            music_dir='C:\\Users\\asus\\Music'
            songs=os.listdir(music_dir)
            os.startfile(os.path.join(music_dir,songs[random.randint(1,112)]))
            break
        elif 'image' in query:
            action = "image search"
            insert(setid,action,query)
            speak("Which image?")
            search_image=takeCommand()
            arguments = {"keywords": search_image, 
                 "format": "jpg", 
                 "limit":4, 
                 "print_urls":True, 
                 "size": "medium", 
                 "aspect_ratio":"panoramic"} 
            response = google_images_download.googleimagesdownload()
            response.download(arguments)
            break
        elif "show my information" in query :
            info()
            break
        elif "take a photo" in query:
            action = "take a photo"
            insert(setid,action,query)
            ec.capture(0,"Burpy Camera","img.jpg")
            break

        elif 'time' in query:
            action = "current time"
            insert(setid,action,query)
            strTime=datetime.now().strftime("%H:%M:%S")
            a="time is"+strTime
            InsertText(a)
            #print(strTime)
            speak(f"sir ,the time is : {strTime}")
            break



        elif 'corona' in query:
            action = "corona information"
            insert(setid,action,query)
            print("Which country ?")
            speak("which country ?")
            InsertText("Which country?")
            country = takeCommand()
            url = 'https://www.worldometers.info/coronavirus/country/' + country.lower() + '/'
            page = requests.get(url)
            soup_page = soup(page.content, 'lxml')
            totalcases = soup_page.findAll('div', attrs =  {'class': 'maincounter-number'})
            total_cases = []
            for total in totalcases:
                total_cases.append(total.find('span').text)
            total = 'Total Coronavirus Cases: ' + total_cases[0] + '\n'
            deaths = 'Total Deaths: ' + total_cases[1] + '\n'
            recovered = 'Total Recovered: ' + total_cases[2] + '\n'
            updates = country + ' Updates: ' + '\n'
            print(updates)
            print(total)
            print(deaths)
            print(recovered)
            speak(updates)
            speak(total)
            speak(deaths)
            speak(recovered)
            InsertText(updates)
            InsertText(total)
            InsertText(deaths)
            InsertText(recovered)
         
            break

        elif "reminder" in query:
            action = "reminder"
            insert(setid,action,query)
            a= "What shall I remind you about?"
            print(a)
            speak(a)
            InsertText(a)
            text = takeCommand()

            while True:
                alarm_time = input("Enter time in 'HH:MM:SS AM/PM' format: ")
                InsertText(alarm_time);
    
                validate = validate_time(alarm_time.lower())
                if validate != "ok":
                    print(validate)
                else:
                    ab = f"Setting alarm for {alarm_time}..."
                    print(ab)
                    speak(ab)
                    InsertText(ab)
                    break

            alarm_hour = alarm_time[0:2]
            alarm_min = alarm_time[3:5]
            alarm_sec = alarm_time[6:8]
            alarm_period = alarm_time[9:].upper()

            while True:
                now = datetime.now()

                current_hour = now.strftime("%I")
                current_min = now.strftime("%M")
                current_sec = now.strftime("%S")
                current_period = now.strftime("%p")

                if alarm_period == current_period:
                    if alarm_hour == current_hour:
                        if alarm_min == current_min:
                            if alarm_sec == current_sec:
                                toast = ToastNotifier()
                                toast.show_toast("Reminder",text,duration=20)
                                break

            break

        elif 'open word' in query:
            action = "open word"
            insert(setid,action,query)
            speak("opening")
            op="openning  word"
            InsertText(op)
            codePath="C:\\Program Files\\Microsoft Office\\Office16\\WINWORD.EXE"
            os.startfile(codePath)
            break

        elif 'email' in query:
                action = "send email"
                insert(setid,action,query)
                try:
                    speak("tell me receiver email")
                   # to = takeCommand().lower().replace(" ","")+"@gmail.com"
                    to = "vatsalnjoshi@gmail.com"
                    print(to)
                    speak("What should I say?")
                    content = takeCommand()
                    sendEmail(to, content)
                    a="Email has been sent!"
                    speak("Email has been sent!")
                    InsertText(a)
                    break
                except Exception as e:
                    print(e)
                    speak("Sorry my friend yaksh. I am not able to send this email")  
                
                break
        elif "weather" in query:
            action = "weather"
            insert(setid,action,query)
            print("City name : ")
            speak("City name ? ")
            city_name=takeCommand()
            response = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city_name+"&APPID=ad54d94279cd61fb0e4187a6ec50701f")
            x = response.json()

            if x["cod"] != "404": 
                y = x["main"] 
                current_temperature = y["temp"] 
                current_pressure = y["pressure"] 
                current_humidiy = y["humidity"] 
                z = x["weather"] 
                weather_description = z[0]["description"] 
                a=" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description)
                InsertText(a)
                
                print(" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description)) 
                speak(a)
            break

        elif 'wallpaper' in query:
            
                action = "change wallpaper"
                insert(setid,action,query)
                num = random.randint(1,99)

                b = "Which type of wallpaper : "
                print(b)
                speak("Which type of wallpaper : ")
                InsertText(b)

                type=takeCommand()

                payload = {'Authorization': '563492ad6f91700001000001c0ffa00cf9dc4edd82b31a17b90c25ec'}
                
                url = 'https://api.pexels.com/v1/search?per_page=1&page=' + str(num) + '&query=' + type

                res= requests.get(url, headers=payload)
                if res.status_code == 200:
                    img_url = res.json().get('photos')[0]['src']['original']
                    img = requests.get(img_url)
                    with open('temp.jpg', 'wb') as f:
                        f.write(img.content)

                else:
                    print('error in making http request')


                path = os.getcwd()+'\\temp.jpg'
                ctypes.windll.user32.SystemParametersInfoW(20,0,path,0)

                a = "Successfully Changed wallpaper"
                print(a)
                speak("Successfully Changed wallpaper")
                InsertText(a)

                break
        elif 'news' in query:
            action = "news"
            insert(setid,action,query)
            try:
                news_url="https://news.google.com/news/rss"
                Client=urlopen(news_url)
                xml_page=Client.read()
                Client.close()
                soup_page=soup(xml_page,"html.parser")
                news_list=soup_page.findAll("item")
                for news in news_list[:3]:
                    a = news.title.text.encode('utf-8')
                    InsertText(a)
                    print(news.title.text.encode('utf-8'))
                    speak(news.title.text.encode('utf-8'))
            except Exception as e:
                    print(e)

            break

        elif 'hey' in query or 'hello' in query or 'hey there' in query or query=='hi' or query == 'Hi':
            list=['hi', 'hello', 'hey there', 'whats up!', 'hey']
            a = (random.choice(list))
            speak(a)
            print(a)
            InsertText(a)
            break;

        elif 'how are you' in query or 'whats up' in query or 'how are things' in query or 'all right' in query:
            list = ['I am good', 'its all fine', 'i am happy, thank you', 'pretty well', 'better than nothing']
            a = random.choice(list)
            speak(a)
            print(a)
            InsertText(a)
            break;

        elif 'whats your name' in query or 'what is your name' in query:
            a = 'my name is burpy'
            speak(a)
            print(a)
            InsertText(a)
            break;

        elif 'who made you' in query or 'who created you' in query:
            a = "I have been created by BVM Students"
            speak(a)
            print(a)
            InsertText(a)
            break;

        elif 'joke' in query:
            a = pyjokes.get_joke(language = 'en', category = 'all')
            speak(a)
            print(a)
            InsertText(a)
            break;

        elif 'search' in query:
            query = query.replace("search", "")
            driver = webdriver.Chrome()
            driver.get("https://www.google.com/search?q=" + query + "&oq=" + query +  "&aqs=chrome..69i57j69i59.1033j0j7&sourceid=chrome&ie=UTF-8")
            break; 
        
        elif 'who i am' in query or 'who am i' in query:            
            a = 'If you talk then definately your human'
            speak(a)
            print(a)
            InsertText(a)
            break;

        elif 'is love' in query:
            list = ['It’s a big waste of time', 'It is 7th sense that destroy all other senses and makes people believe nonsense.']
            a = random.choice(list)
            speak(a)
            print(a)
            InsertText(a)
            break;

        elif 'who are you' in query:
            a = 'I am your virtual assistant'
            speak(a)
            print(a)
            InsertText(a)
            break;
 
        elif 'reason for you' in query:
            a = 'I was created as a Mini project'
            speak(a)
            print(a)
            InsertText(a)
            break;

        elif 'shutdown system' in query:
            a = 'Hold On a Sec ! Your system is on its way to shut down'
            speak(a)
            print(a)
            InsertText(a)
            os.system("shutdown /s /t 1")
            break;

        elif 'where is' in query:
            query = query.replace("where is", "")
            location = query
            a = 'User asked to Locate' + location
            speak(a)
            print(a)
            InsertText(a)
            webbrowser.open("https://www.google.nl/maps/place/" + location + "/&amp;")
            break;

        elif 'gf' in query or 'girlfriend' in query:  
            a = 'I am not sure about, may be you should give me some time'
            speak(a)
            print(a)
            InsertText(a)
            break;

        elif "i love you" in query:
            list = ['I love ME too!', 'Ohh, hard to understand', 'Well, who doesn’t?', 'Awww, but my hatred for you is even more truthful than this.']
            a = random.choice(list)
            speak(a)
            print(a)
            InsertText(a)
            break;

        elif 'exit' in query or 'quit' in query:
            list = ['Thanks for giving me your time', 'See you again, bye']
            a = random.choice(list)
            speak(a)
            print(a)
            InsertText(a)
            exit()
            break;

        elif 'meaning' in query:
            query = query.replace("what is the", "")
            driver = webdriver.Chrome()
            driver.get("https://www.google.com/search?q=" + query + "&oq=" + query +  "&aqs=chrome..69i57j69i59.1033j0j7&sourceid=chrome&ie=UTF-8")
            break;

        else:
            speak("I cant understand")
            speak("Say it again")
            InsertText("I cant understand\nSay it again")
            query= takeCommand()



def close_window():
    window.destroy()
 
#Make the window
def main_window():
    global window 
    window = Toplevel()
    window.geometry('348x600')
    window.configure(bg='#000000')
    window.title("BURPY")

    robot = PhotoImage(file='C:\\Users\\asus\\source\\repos\\Burpy\\Robot1.png')
    tk.Label(window, image = robot, bg = "black").place(x=8, y=5)

    global textentry
    textentry = Entry(window, width = 30,bg="#161617",fg="white", justify = LEFT)
    textentry.grid(row =2 , column=0, columnspan=2, sticky =pos, pady=13)
    text = textentry.get()

    nameButton = Button(window, text= "Enter your Name", width = 20, command = click, fg = "#272324", bg= "#A9A9A9").grid(row=3, column=0 ,sticky=pos, pady=13)

    global output
    output  = Text(window, width=43, height = 20, wrap = WORD, bg= 'black',fg = "white")
    output.grid(row=4, column=0, columnspan=1, sticky=pos, pady=10)
    output.config(state=NORMAL)

    tk.Label(window, text="Tap to speak", fg = "white" , bg = "black").grid(row=5, column=0 ,sticky=pos, pady=10)

    ask_button = PhotoImage(file='C:\\Users\\asus\\source\\repos\\Burpy\\1.png')
    askButton = Button(window, image = ask_button, width=50, height=50, borderwidth=0, command = refresh, fg = "white", bg= "#000000", activebackground='#3d3d3d').grid(row=6, column=0 ,sticky=pos, pady=10)

    Button(window, text= "EXIT", width= 14, command=close_window, fg = "#272324", bg= "#A9A9A9").grid(row=8, column= 0 , sticky=pos, pady=10)


    window.mainloop()


conn()
main_screen()

       
         
            