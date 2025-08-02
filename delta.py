import time
import instaloader
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
from bs4 import BeautifulSoup
import wikipedia as wi
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import psutil
import pyjokes
import pyautogui
import PyPDF2
import urllib.parse
import operator
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
#from jarvisUi import Ui_jarvisUi

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 5 and hour <= 12:
        speak("good morning")
    elif hour > 12 and hour < 18:
        speak("good afternoon")
    else:
        speak("good evening")
    speak("i am delta sir. please tell me how can i help you.")


def news():
    main_url = "https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbGhrcFFlUU16Nlk4VWpGNzdwSWxaZC13eHl4Z3xBQ3Jtc0tuYjB2R3lXcmFjekRZQkNubFlGTTMxTWhVaXlIUHJxYzFEUF9GWnhIRjVSTmZPdDRzVTdxSVFHalhsZHpzRXk1SWJncEpTYkhXT1E4VFV2Q1F3cmw1amVHa1BodGx1d2lfYldVT3RMVVQzUE1SdUJGSQ&q=https%3A%2F%2Fnewsapi.org%2F&v=w_Q_KBbl2Zs"
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")


class MainThread(QThread):
    update_time = pyqtSignal(str)

    def run(self):
        while True:
            current_time = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)
            self.update_time.emit(current_time)
            time.sleep(1)  # Update time every second


class JarvisThread(QThread):
    def __init__(self):
        super().__init__()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognition...")
            self.query = r.recognize_google(audio, language='en-in')
            print(f"user said:{self.query}")
        except Exception as e:
            speak("Say that again please...")
            return "none"
        return self.query

    def run(self):
        wish()
        while True:
            self.query = self.takecommand().lower()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.ui = Ui_jarvisUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.main_thread = MainThread()
        self.main_thread.update_time.connect(self.update_time_label)
        self.jarvis_thread = JarvisThread()

    def startTask(self):
        self.ui.movie = QMovie(r"C:\Users\ACER\Desktop\pyhton\PE2\jarvisAi.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QMovie(r"C:\Users\ACER\Desktop\pyhton\PE2\jarvisAi.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.main_thread.start()
        self.jarvis_thread.start()

    def update_time_label(self, current_time):
        self.ui.textBrowser_2.setText(current_time)

import requests
import speech_recognition as sr
import pyttsx3

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def takecommand():
    """Capture user input from speech and return as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please tell me the city name.")
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        city = r.recognize_google(audio, language='en-in')
        print(f"User said: {city}")
        return city
    except Exception as e:
        speak("Sorry, I couldn't understand. Please try again.")
        return None

def get_weather(city):
    """Fetch weather details for the given city using OpenWeatherMap API."""
    api_key = ""  # Replace with your actual API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(base_url)
        data = response.json()

        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_report = (f"The current temperature in {city} is {temp}°C "
                              f"with {description}. Humidity is at {humidity}%, "
                              f"and wind speed is {wind_speed} meters per second.")

            print(weather_report)
            speak(weather_report)
        else:
            speak("Sorry, I couldn't fetch the weather details. Please check the city name.")

    except Exception as e:
        speak("An error occurred while fetching the weather data.")

def weather():
    """Ask for city name and fetch weather details."""
    speak("Please tell me the city name.")
    city = takecommand()
    if city:
        get_weather(city)



def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo
    server.starttls()
    server.login("your email", "password")  # enter your email id
    server.sendmail('your email id', to, content)
    server.close()


def pdf_reader():
    book = open('py3.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)  # pip install PyPDF2
    pages = pdfReader.numPages
    speak(f"Total numbers of pages in this book {pages} ")
    speak("sir please enter the page number i have to read")
    pg = int(input("Please enter the page number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)




def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)  # ,timeout=1,phrase_time_limit=5)
    try:
        print("Recognition...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said:{query}")
    except Exception as e:
        speak("Say that again please...")
        return "none"
    return query


if __name__=="__main__":
    wish()
    while True:


        query=takecommand().lower()

        if "notepad" in query:
            npath = "C:/Windows//notepad.exe"
            os.startfile(npath)
        elif "open command prompt" in query:
            os.system("start cmd")

        elif "camera" in query:
            cap=cv2.VideoCapture(0)
            while True:
                ret,img=cap.read()
                cv2.imshow('webcam',img)
                k=cv2.waitKey(50)
                if k==27:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        elif "weather" in query:
            weather()


            
        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"your ip address is {ip}")



        elif "wikipedia" in query:
            try:
                speak("What would you like to know from Wikipedia?")
                search_query = takecommand().lower()
                if search_query == "none":
                    raise ValueError
                
                speak("Searching Wikipedia...")
                results = wi.summary(search_query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                print(results)
                
            except wi.exceptions.DisambiguationError as e:
                speak("There are multiple matches. Please be more specific.")
            except wi.exceptions.PageError:
                speak("No information found for this query.")
            except Exception as e:
                speak("Sorry, I couldn't retrieve Wikipedia information.")


        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")
            
        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")

        elif "open instagram" in query:
            webbrowser.open("www.instagram.com")

        elif "open google" in query:
            speak(f"what should I search on Google?")
            cm=takecommand().lower()
            webbrowser.open(f"{cm}")

        elif "send message" in query:
            kit.sendwhatmsg("+917007213658","this is testing protocol",2,25)

        elif "play song on youtube" in query:
            kit.playonyt("see you again")

        elif "open browser" in query:
            speak("Opening browser")
            webbrowser.open("https://www.google.com")  # Opens default browser with Google
            # Alternative: webbrowser.open_new_tab("https://www.google.com")


        elif "open music" in query:
            speak("Which song would you like to listen to?")
            song_name = takecommand().lower()  # Take voice input for the song name
            query_string = urllib.parse.quote(song_name)  # Convert song name to a URL-friendly format
            url = f"https://music.youtube.com/search?q={query_string}"  # Construct search URL
            speak(f"Playing {song_name} on YouTube Music")
            webbrowser.open(url)  # Open in the browser

        elif "open chat gpt" in query:
            webbrowser.open("https://chat.openai.com")
            speak("Opening ChatGPT. How can I assist you?")



        elif "system status" in query:
            battery = psutil.sensors_battery()
            cpu_usage = psutil.cpu_percent()
            ram_usage = psutil.virtual_memory().percent
            speak(f"Battery is at {battery.percent} percent")
            speak(f"CPU usage is {cpu_usage} percent")
            speak(f"RAM usage is {ram_usage} percent")

        elif "open whatsapp" in query:
            try:
                speak("Opening WhatsApp...")
                #os.system("start whatsapp")  # Opens the WhatsApp app if installed
                webbrowser.open("https://web.whatsapp.com")  # Opens WhatsApp Web
            except Exception as e:
                speak("Sorry, I was unable to open WhatsApp.")
                print(e)










        elif "no thanks" in query:
            speak("thanks for using me sir,have a good day.")
            sys.exit()
            
        #to set alarm
        # elif "set alarm" in query:
        #     nn=int(datetime.datetime.now().hour)
        #     if nn==22:
        #         music_dir=' '
        #         songs=os.listdir(music_dir)
        #         os.startfile(os.path.join(music_dir,songs[0]))

        #to find a joke
        elif "tell me a joke" in query:
            joke=pyjokes.get_joke()
            speak(joke)
            print(joke)
        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")
        elif "restart the system" in query:
            os.system("shutdown /r /t 5")
        elif "sleep the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif "switch the window" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        elif "open chat gpt" in query:
            webbrowser.open("https://chat.openai.com")
            speak("Opening ChatGPT. How can I assist you?")


        # elif "tell me news" in query:
        #     speak("please wait sir,fetching the latest news")
        #     news()
        
       #----------------To find my location using ip address----------------

        elif "where i am " in query or "where are we" in query:
            speak("wait sir,let me check")
            try:
                ipAdd=requests.get('https://api.ipify.org').text
                print(ipAdd)
                url='https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                geo_requests=requests.get(url)
                geo_data=geo_requests.json()
                city=geo_data['city']
                country=geo_data['country']
                speak(f"sir i am not sure,but i think we are in {city} city of {country} country")
            except Exception as e:
                speak("sorry sir,due to network issue i am not able to find where we are.")
                pass

        #--------------To check a instagram profiile---
        elif "instagram profile" in query or "profile on instagram" in query:
            speak("sir please enter the user name correctly.")
            name=input("enter username here:")
            webbrowser.open(f"www.instagram.com/{name}")
            speak(f"sir here is the profile of the user {name}")
            time.sleep(5)
            speak("sir would you like to download profile picture of this account")
            condition=takecommand().lower()
            if "yes" in condition:
                mod=instaloader.Instaloader()
                mod.download_profile(name,profile_pic_only=True)
                speak("i am done sir,profile picture is saved in our main folder.now i am ready for next command")
            else:
                pass

    #------------To take screenshot--------------
        elif "take screenshot" in query or "take a screenshot" in query:
            speak("sir,please tell me the name for this screenshot file")
            name=takecommand().lower()
            speak("please sir hold the screen for few seconds,i am taking screenshot")
            time.sleep(3)
            img=pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("i am done sir,the screenshot is saved in our main folder.now i am ready for next command")

            
       # speak("sir,do you have any other work")

       # speak("sir,do you have any other work")
        elif "read pdf" in query:
            pdf_reader()

        elif "hide all files" in query or "hide this folder" in query or "visible for everyone" in query:
            speak("sir please tell me you want to hide this folder or make it visible for everyone")
            condition = takecommand().lower()
            if "hide" in condition:
                os.system("attrib +h /s /d")  # os module
                speak("sir, all the files in this folder are now hidden.")
            elif "visible" in condition:
                os.system("attrib -h /s /d")
                speak("sir, all the files in this folder are now visible to everyone. i wish you are taking this decision in your benefit.")
            elif "leave it" in condition or "leave for now" in condition:
                speak("Ok sir")

        elif "do some calculations" in query or "can you calculate" in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("Say what you want to calculate, example: 3 plus 3")
                print("Listening...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                print(audio)  # Check if audio is captured correctly
                my_string = r.recognize_google(audio)
                print(my_string)

            def get_operator_fn(op):
                return {
                    '+': operator.add,
                    '-': operator.sub,
                    'x': operator.mul,
                    'divided': operator.__truediv__,
                    'Mod': operator.mod,
                    'mod': operator.mod,
                    '^': operator.xor,
                }[op]

            def eval_binary_expr(op1, op, op2):
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(op)(op1, op2)

            speak("your result is")
            print(eval_binary_expr(*(my_string.split())))



startExecution = JarvisThread


if __name__ == "__main__":
    app = QApplication(sys.argv)
    jarvis = Main()
    jarvis.show()
    sys.exit(app.exec_())
