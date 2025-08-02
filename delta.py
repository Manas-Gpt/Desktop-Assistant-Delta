import sys
import os
import time
import datetime
import webbrowser
import requests
import speech_recognition as sr
import pyttsx3
import wikipedia as wi
import pywhatkit as kit
import smtplib
import psutil
import pyjokes
import pyautogui
import cv2
import instaloader
import PyPDF2

from PyQt5.QtCore import QThread, pyqtSignal, QTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QMovie

# Import your UI and config file
from jarvisUi import Ui_jarvisUi 
import config

class AssistantThread(QThread):
    """
    The main thread that runs the assistant logic in the background,
    so the GUI doesn't freeze.
    """
    # Signals to communicate with the main GUI thread
    assistant_spoke = pyqtSignal(str)
    user_spoke = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # --- Initialize Engines Once ---
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        
        self.recognizer = sr.Recognizer()
        
        # --- Map voice commands to functions ---
        self.commands = {
            "notepad": self.open_notepad,
            "command prompt": self.open_cmd,
            "camera": self.open_camera,
            "weather": self.get_weather,
            "ip address": self.get_ip_address,
            "wikipedia": self.search_wikipedia,
            "open youtube": lambda: self.open_website("youtube.com"),
            "open facebook": lambda: self.open_website("facebook.com"),
            "open google": self.search_google,
            "send message": self.send_whatsapp_message,
            "play song": self.play_song_on_youtube,
            "system status": self.get_system_status,
            "tell me a joke": self.tell_joke,
            "shut down": self.shutdown_system,
            "restart": self.restart_system,
            "sleep": self.sleep_system,
            "switch the window": self.switch_window,
            "where am i": self.find_location,
            "instagram profile": self.check_instagram_profile,
            "take screenshot": self.take_screenshot,
            "read pdf": self.read_pdf,
            "calculate": self.calculate,
            "hide files": lambda: os.system("attrib +h /s /d"),
            "show files": lambda: os.system("attrib -h /s /d"),
            "no thanks": self.exit_assistant,
            "exit": self.exit_assistant,
        }

    # 1. Core Methods: speak and take_command
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        self.assistant_spoke.emit(f"Delta: {text}")

    def take_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)
        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            self.user_spoke.emit(f"You: {query}")
            return query.lower()
        except Exception as e:
            self.speak("Say that again please...")
            return "none"

    # 2. Main Execution Loop
    def run(self):
        self.wish_user()
        while True:
            query = self.take_command()
            if query == "none":
                continue

            # Find and execute the command
            command_executed = False
            for command_phrase, function in self.commands.items():
                if command_phrase in query:
                    function()
                    command_executed = True
                    break
            
            if not command_executed:
                self.speak("I'm not sure how to do that yet.")
    
    # 3. Command Functions
    def wish_user(self):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 17:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
        self.speak(f"{greeting}, Sir. I am Delta. How can I help you?")

    def exit_assistant(self):
        self.speak("Goodbye, Sir!")
        sys.exit()

    def open_notepad(self):
        os.startfile("C:\\Windows\\System32\\notepad.exe")

    def open_cmd(self):
        os.system("start cmd")
        
    def open_camera(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('webcam', img)
            if cv2.waitKey(1) & 0xFF == 27: # Press ESC to close
                break
        cap.release()
        cv2.destroyAllWindows()
    
    def open_website(self, url):
        webbrowser.open(f"https://{url}")

    def search_google(self):
        self.speak("What should I search on Google?")
        search_term = self.take_command()
        if search_term != 'none':
            webbrowser.open(f"https://google.com/search?q={search_term}")
    
    def get_weather(self):
        self.speak("Which city's weather would you like to know?")
        city = self.take_command()
        if city != "none":
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.OPENWEATHER_API_KEY}&units=metric"
            try:
                data = requests.get(url).json()
                if data["cod"] == 200:
                    temp = data["main"]["temp"]
                    desc = data["weather"][0]["description"]
                    self.speak(f"The weather in {city} is {desc} with a temperature of {temp} degrees Celsius.")
                else:
                    self.speak("Sorry, I couldn't find weather data for that city.")
            except Exception:
                self.speak("Sorry, I couldn't connect to the weather service.")
    
    # ... Add all your other command functions here in the same style ...
    # (search_wikipedia, send_whatsapp_message, tell_joke, etc.)
    
    def search_wikipedia(self):
        self.speak("What topic should I search for on Wikipedia?")
        topic = self.take_command()
        if topic != "none":
            try:
                results = wi.summary(topic, sentences=2)
                self.speak("According to Wikipedia...")
                self.speak(results)
            except Exception:
                self.speak(f"Sorry, I couldn't find any results for {topic} on Wikipedia.")

    def play_song_on_youtube(self):
        self.speak("What song should I play?")
        song = self.take_command()
        if song != 'none':
            kit.playonyt(song)
    
    def get_system_status(self):
        battery = psutil.sensors_battery()
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.speak(f"Battery is at {battery.percent} percent.")
        self.speak(f"CPU usage is at {cpu} percent.")
        self.speak(f"RAM usage is at {ram} percent.")

    def shutdown_system(self):
        self.speak("Shutting down the system.")
        os.system("shutdown /s /t 5")
    
    def restart_system(self):
        self.speak("Restarting the system.")
        os.system("shutdown /r /t 5")

    def sleep_system(self):
        self.speak("Putting the system to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    def switch_window(self):
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.keyUp("alt")
    
    def find_location(self):
        # Implement location logic here
        pass

    def check_instagram_profile(self):
        # Implement instagram logic here
        pass

    def take_screenshot(self):
        # Implement screenshot logic here
        pass
    
    def read_pdf(self):
        # Implement PDF logic here
        pass

    def calculate(self):
        # Implement calculation logic here
        pass

class Main(QMainWindow):
    """ The main GUI window """
    def __init__(self):
        super().__init__()
        self.ui = Ui_jarvisUi()
        self.ui.setupUi(self)
        
        self.ui.pushButton_start.clicked.connect(self.start_task)
        self.ui.pushButton_exit.clicked.connect(self.close)

    def start_task(self):
        # --- Setup and start GIF ---
        self.ui.movie = QMovie(config.GUI_GIF_PATH)
        self.ui.label_gif.setMovie(self.ui.movie)
        self.ui.movie.start()
        
        # --- Start Assistant Thread ---
        self.assistant_thread = AssistantThread()
        self.assistant_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())
