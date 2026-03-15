# IMPORTS
import sys
import re
import threading
import os
import time
import datetime
import webbrowser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
import requests
import speech_recognition as sr
import pyttsx3
import wikipedia as wi
import pywhatkit as kit
import smtplib
import psutil
import pyjokes
import pyautogui
import pyaudio
import cv2
import instaloader
import PyPDF2
import operator
import urllib.parse
import subprocess
import pyperclip
from deep_translator import GoogleTranslator
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QTime, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow

# ENGINE SETUP
# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def speak(audio):
    """Speaks the given text and emits it to Electron as SAY::"""
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception:
        # If TTS fails, continue emitting text to UI
        pass
    print(f"SAY::{audio}")
    sys.stdout.flush()

# MAIN GUI THREAD
# This class is for updating the time on the GUI. It's kept separate.
class MainThread(QThread):
    update_time = pyqtSignal(str)

    def run(self):
        while True:
            current_time = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)
            self.update_time.emit(current_time)
            time.sleep(1) # Update time every second

# DELTA ASSISTANT THREAD
class DeltaThread(QThread):
    """
    Runs the assistant's core logic in a separate thread
    to prevent the GUI from freezing.
    """
    def __init__(self):
        super().__init__()
        self.query = ""

    def takecommand(self):
        """Listens for a command and returns it as a string."""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognizing...")
            self.query = r.recognize_google(audio, language='en-in')
            print(f"User said: {self.query}")
        except Exception as e:
            speak("Say that again please...")
            return "none"
        return self.query.lower()

    def wish(self):
        """Greets the user based on the time of day."""
        hour = int(datetime.datetime.now().hour)
        if 5 <= hour < 12:
            speak("Good morning")
        elif 12 <= hour < 18:
            speak("Good afternoon")
        else:
            speak("Good evening")
        speak("I am Delta. Please tell me how I can help you.")

    def get_weather(self):
        """Fetches and speaks the weather for a given city."""
        speak("Please tell me the city name.")
        city = self.takecommand()
        if city and city != "none":
            api_key = os.getenv("OPENWEATHER_API_KEY")
            base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            try:
                response = requests.get(base_url)
                data = response.json()
                if data["cod"] == 200:
                    temp = data["main"]["temp"]
                    description = data["weather"][0]["description"]
                    weather_report = (f"The current temperature in {city} is {temp} degrees Celsius "
                                      f"with {description}.")
                    speak(weather_report)
                else:
                    speak("Sorry, I couldn't fetch the weather details. Please check the city name.")
            except Exception as e:
                speak("An error occurred while fetching the weather data.")

    def get_weather_for_city(self, city):
        """Fetch weather for a specific city (text chat)."""
        if not city:
            speak("Please provide a city name, for example: weather in Delhi")
            return
        api_key = os.getenv("OPENWEATHER_API_KEY")
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(base_url)
            data = response.json()
            if data.get("cod") == 200:
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]
                weather_report = (f"The current temperature in {city} is {temp} degrees Celsius "
                                  f"with {description}.")
                speak(weather_report)
            else:
                speak("Sorry, I couldn't fetch the weather details. Please check the city name.")
        except Exception:
            speak("An error occurred while fetching the weather data.")

    def pdf_reader(self):
        """Tells Electron to open a PDF dialog and reads the selected file."""
        try:
            print("OPEN_DIALOG::pdf")
            sys.stdout.flush() 

            filepath = sys.stdin.readline().strip()

            if filepath:
                book = open(filepath, 'rb')
                # UPDATED: Use PdfReader instead of the old PdfFileReader
                pdfReader = PyPDF2.PdfReader(book)
                
                # UPDATED: Use len(pdfReader.pages) instead of .numPages
                pages = len(pdfReader.pages)
                speak(f"This book has {pages} pages. Which page number should I read?")
                
                pg_str = self.takecommand()
                if pg_str and pg_str.isdigit():
                    pg_num = int(pg_str)
                    if 1 <= pg_num <= pages:
                        # UPDATED: Use pdfReader.pages[] instead of .getPage()
                        page = pdfReader.pages[pg_num - 1]
                        text = page.extract_text()
                        speak("Here is the content from that page.")
                        speak(text)
                    else:
                        speak("Sorry, that page number is out of range.")
                else:
                    speak("I didn't catch a valid page number.")

        except Exception as e:
            speak("An error occurred or no file was selected.")
            print(f"PDF Reader Error: {e}")

        except Exception as e:
            speak("An error occurred or no file was selected.")
            print(f"PDF Reader Error: {e}")
    
    def print_document(self):
        """Tells Electron to open a document dialog and prints the selected file."""
        try:
            # Tell Electron to open a dialog for Word documents
            print("OPEN_DIALOG::doc")
            sys.stdout.flush()

            # Wait for and read the file path sent back from Electron
            filepath = sys.stdin.readline().strip()

            if filepath and os.path.exists(filepath):
                # This command sends the file to the default printer on Windows
                os.startfile(filepath, "print")
                speak(f"The document has been sent to your default printer.")
            else:
                speak("Sorry, the file path seems to be invalid or no file was selected.")

        except Exception as e:
            speak("I encountered an error while trying to print the document.")
            print(f"Printing Error: {e}")

    # VOLUME CONTROL HELPERS
    def _get_volume_interface(self):
        """Returns the Windows audio endpoint volume interface."""
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))

    def control_volume(self, action):
        """Mute, unmute, increase, or decrease system volume."""
        try:
            vol = self._get_volume_interface()
            current = vol.GetMasterVolumeLevelScalar()
            if action == "mute":
                vol.SetMute(1, None)
                speak("System muted.")
            elif action == "unmute":
                vol.SetMute(0, None)
                speak("System unmuted.")
            elif action == "increase":
                new_vol = min(1.0, current + 0.1)
                vol.SetMasterVolumeLevelScalar(new_vol, None)
                speak(f"Volume increased to {int(new_vol * 100)} percent.")
            elif action == "decrease":
                new_vol = max(0.0, current - 0.1)
                vol.SetMasterVolumeLevelScalar(new_vol, None)
                speak(f"Volume decreased to {int(new_vol * 100)} percent.")
        except Exception as e:
            speak("Sorry, I was unable to control the volume.")
            print(f"Volume Error: {e}")

    def run(self):
        """The main loop for the assistant."""
        self.wish()
        while True:
            query = self.takecommand()

            if "notepad" in query:
                os.startfile("C:/Windows/notepad.exe")

            elif "open command prompt" in query:
                os.system("start cmd")

            elif "camera" in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    # Press 'ESC' key to exit the camera view
                    if cv2.waitKey(50) & 0xFF == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif "weather" in query:
                self.get_weather()

            elif "ip address" in query:
                try:
                    ip = requests.get('https://api.ipify.org').text
                    speak(f"Your IP address is {ip}")
                except requests.ConnectionError:
                    speak("Sorry, I am unable to connect to the internet.")

            elif "wikipedia" in query:
                speak("What would you like to know from Wikipedia?")
                search_query = self.takecommand()
                if search_query and search_query != "none":
                    try:
                        speak("Searching Wikipedia...")
                        results = wi.summary(search_query, sentences=2)
                        speak("According to Wikipedia")
                        speak(results)
                    except Exception:
                        speak("Sorry, I couldn't retrieve information for that query.")

            elif "open youtube" in query:
                webbrowser.open("https://www.youtube.com")
            
            elif "open google" in query:
                speak("What should I search on Google?")
                cm = self.takecommand()
                if cm and cm != "none":
                    webbrowser.open(f"https://google.com/search?q={cm}")

            elif "send message" in query:
                speak("Sending WhatsApp message.")
                # Sends a message to the specified number 1 minute from now
                kit.sendwhatmsg("+91xxxxxxxxxx", "This is a testing protocol", datetime.datetime.now().hour, datetime.datetime.now().minute + 1)

            elif "play song on youtube" in query:
                speak("What song would you like to hear?")
                song = self.takecommand()
                if song and song != 'none':
                    kit.playonyt(song)

            elif "system status" in query:
                battery = psutil.sensors_battery()
                cpu_usage = psutil.cpu_percent()
                ram_usage = psutil.virtual_memory().percent
                speak(f"Battery is at {battery.percent} percent")
                speak(f"CPU usage is {cpu_usage} percent")
                speak(f"RAM usage is {ram_usage} percent")

            # --- JOKE FUNCTIONALITY ---
            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)
                print(joke)

            elif "shut down the system" in query:
                speak("Shutting down the system.")
                os.system("shutdown /s /t 5")

            elif "restart the system" in query:
                speak("Restarting the system.")
                os.system("shutdown /r /t 5")

            elif "sleep the system" in query:
                speak("Putting the system to sleep.")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif "switch the window" in query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "where am i" in query or "where are we" in query:
                speak("Wait sir, let me check.")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    url = f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
                    geo_data = requests.get(url).json()
                    city = geo_data['city']
                    country = geo_data['country']
                    speak(f"I believe we are in {city} city of {country} country.")
                except Exception as e:
                    speak("Sorry sir, I am not able to find where we are due to a network issue.")

            elif query.startswith("find "):
                location = query.replace("find ", "", 1).strip()
                if location:
                    encoded = urllib.parse.quote(location)
                    webbrowser.open(f"https://www.google.com/maps/search/{encoded}")
                    speak(f"Opening Google Maps for {location}.")
                else:
                    speak("Please say the location you want me to find.")

            elif "instagram profile" in query:
                speak("Should I search by name, or do you have a username?")
                insta_choice = self.takecommand()
                if "search" in insta_choice or "name" in insta_choice:
                    speak("What name should I search for on Instagram?")
                    search_query = self.takecommand()
                    if search_query and search_query != "none":
                        encoded = urllib.parse.quote(search_query)
                        webbrowser.open(f"https://www.instagram.com/explore/search/?q={encoded}")
                        speak(f"Here are the Instagram search results for {search_query}.")
                else:
                    speak("Please say the Instagram username.")
                    username = self.takecommand()
                    if username and username != "none":
                        username = username.replace(" ", "").lower()
                        webbrowser.open(f"https://www.instagram.com/{username}")
                        speak(f"Opening the Instagram profile of {username}.")

            elif "take screenshot" in query:
                speak("Sir, what should I name this screenshot file?")
                name = self.takecommand()
                if name and name != "none":
                    speak("Please hold the screen, I am taking a screenshot.")
                    time.sleep(2)
                    img = pyautogui.screenshot()
                    img.save(f"{name}.png")
                    speak("The screenshot is saved in our main folder.")

            elif "read pdf" in query or "read a pdf" in query:
                self.pdf_reader()
            elif "print document" in query or "print a document" in query:
                self.print_document()
            
            elif "calculate" in query:
                speak("Say what you want to calculate. For example: 3 plus 3")
                try:
                    calc_string = self.takecommand()
                    # A simple parser for basic arithmetic
                    words = calc_string.split()
                    op1 = int(words[0])
                    op2 = int(words[2])
                    operator_str = words[1].lower()

                    if operator_str in ['plus', '+']:
                        result = op1 + op2
                    elif operator_str in ['minus', '-']:
                        result = op1 - op2
                    elif operator_str in ['times', 'x', 'multiply']:
                        result = op1 * op2
                    elif operator_str in ['divided', '/']:
                        result = op1 / op2
                    else:
                        raise ValueError("Unknown operator")
                        
                    speak(f"The result is {result}")
                    print(result)

                except Exception:
                    speak("I was unable to understand the calculation.")

            # OPEN ANY APP
            elif query.startswith("open "):
                app_name = query.replace("open ", "", 1).strip()
                try:
                    subprocess.Popen([app_name])
                    speak(f"Opening {app_name}.")
                except FileNotFoundError:
                    try:
                        os.startfile(app_name)
                        speak(f"Opening {app_name}.")
                    except Exception:
                        speak(f"Sorry, I couldn't find {app_name} on your system.")

            # CLIPBOARD
            elif "copy to clipboard" in query:
                speak("What should I copy to the clipboard?")
                content = self.takecommand()
                if content and content != "none":
                    pyperclip.copy(content)
                    speak("Copied to clipboard.")

            elif "read clipboard" in query or "what's in my clipboard" in query:
                content = pyperclip.paste()
                if content:
                    speak(f"Your clipboard contains: {content}")
                else:
                    speak("Your clipboard is empty.")

            # DICTIONARY
            elif "meaning of" in query:
                word = query.replace("meaning of", "").strip()
                if word:
                    try:
                        response = requests.get(
                            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
                        )
                        data = response.json()
                        meaning = data[0]['meanings'][0]['definitions'][0]['definition']
                        speak(f"The meaning of {word} is: {meaning}")
                    except Exception:
                        speak(f"Sorry, I couldn't find the meaning of {word}.")

            # TYPE / DICTATE TEXT
            elif query.startswith("type "):
                text_to_type = query.replace("type ", "", 1).strip()
                if text_to_type:
                    speak(f"Typing: {text_to_type}")
                    pyperclip.copy(text_to_type)
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 'v')

            # TRANSLATE TEXT 
            elif "translate" in query and " to " in query:
                try:
                    m = re.search(r"translate (.+) to (\w+)", query)
                    if m:
                        text  = m.group(1).strip()
                        lang  = m.group(2).strip()
                        translated = GoogleTranslator(source='auto', target=lang).translate(text)
                        speak(f"The translation is: {translated}")
                    else:
                        speak("Please say: translate hello to French.")
                except Exception:
                    speak("Sorry, I was unable to translate that.")

            # VOLUME CONTROL
            elif "mute" in query and "unmute" not in query:
                self.control_volume("mute")

            elif "unmute" in query:
                self.control_volume("unmute")

            elif "increase volume" in query or "volume up" in query:
                self.control_volume("increase")

            elif "decrease volume" in query or "volume down" in query:
                self.control_volume("decrease")

            elif "no thanks" in query or "exit" in query or "goodbye" in query:
                speak("Thank you for using me. Have a good day, sir.")
                sys.exit()

    # TEXT CHAT HANDLER
    def handle_text_command(self, text):
        """Processes a text command coming from Electron (stdin)."""
        if not text:
            return
        t = text.strip().lower()

        # weather in <city>
        m = re.search(r"weather in\s+(.+)$", t)
        if m:
            city = m.group(1).strip()
            self.get_weather_for_city(city)
            return

        # wikipedia <topic>
        m = re.search(r"^(wikipedia|wiki)\s+(.+)$", t)
        if m:
            topic = m.group(2).strip()
            try:
                speak("Searching Wikipedia...")
                results = wi.summary(topic, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception:
                speak("Sorry, I couldn't retrieve information for that query.")
            return

        # open youtube
        if "open youtube" in t:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")
            return

        # search / open google for <query>
        m = re.search(r"(search|open google( for)?)\s+(.+)$", t)
        if m:
            q = m.group(3).strip()
            webbrowser.open(f"https://google.com/search?q={q}")
            speak(f"Searching Google for {q}")
            return

        # joke
        if "joke" in t:
            try:
                joke = pyjokes.get_joke()
                speak(joke)
            except Exception:
                speak("I couldn't fetch a joke right now.")
            return

        # simple calculate: e.g., calculate 3 plus 5
        m = re.search(r"^calculate\s+(.*)$", t)
        if m:
            calc_string = m.group(1)
            try:
                words = calc_string.split()
                op1 = int(words[0])
                op2 = int(words[2])
                operator_str = words[1].lower()
                if operator_str in ['plus', '+']:
                    result = op1 + op2
                elif operator_str in ['minus', '-']:
                    result = op1 - op2
                elif operator_str in ['times', 'x', 'multiply', '*']:
                    result = op1 * op2
                elif operator_str in ['divided', '/', 'divide']:
                    result = op1 / op2
                else:
                    raise ValueError("Unknown operator")
                speak(f"The result is {result}")
            except Exception:
                speak("I couldn't parse that calculation. Try 'calculate 3 plus 3'")
            return

        # fallback
        speak(f"You said: {text}. I can do things like 'weather in Delhi', 'wikipedia Ada Lovelace', 'search quantum computing', or 'joke'.")

# MAIN GUI CLASS 
# NOTE: To run the GUI, you must have a 'deltaUi.py' file generated from a .ui file.
# from deltaUi import Ui_deltaUi 

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.ui = Ui_deltaUi()
        # self.ui.setupUi(self)
        # self.ui.pushButton.clicked.connect(self.startTask)
        # self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        # self.ui.movie = QMovie("path/to/your/deltaAi.gif")
        # self.ui.label.setMovie(self.ui.movie)
        # self.ui.movie.start()
        
        # Start the thread that runs the assistant's logic
        self.delta_thread = DeltaThread()
        self.delta_thread.start()
        
        # Start the thread to update the time on the GUI
        # self.main_thread = MainThread()
        # self.main_thread.update_time.connect(self.update_time_label)
        # self.main_thread.start()

    def update_time_label(self, current_time):
        # Updates a label on the GUI with the current time
        # self.ui.textBrowser_2.setText(current_time)
        pass

# SCRIPT ENTRY POINT
if __name__ == "__main__":
    # Start stdin listener thread for TEXT:: messages from Electron
    assistant = DeltaThread()

    def stdin_loop():
        for raw in sys.stdin:
            try:
                line = raw.strip()
                if not line:
                    continue
                if line.startswith('TEXT::'):
                    text = line.replace('TEXT::', '', 1).strip()
                    assistant.handle_text_command(text)
            except Exception:
                # Avoid crashing on malformed input
                pass

    threading.Thread(target=stdin_loop, daemon=True).start()

    # Run the voice assistant loop (blocking)
    assistant.run()

    # To run with the PyQt5 GUI (uncomment the lines below):
    # app = QApplication(sys.argv)
    # delta_gui = Main()
    # delta_gui.show()
    # delta_gui.startTask() # Start the assistant thread after showing the window
    # sys.exit(app.exec_())
