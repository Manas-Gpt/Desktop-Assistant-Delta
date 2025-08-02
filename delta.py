# ================================== IMPORTS ==================================
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
import operator

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QMovie

# ========================== LOCAL IMPORTS =================================
# Import your UI and config files. Ensure they are in the same directory.
from jarvisUi import Ui_jarvisUi
import config

# ============================= ASSISTANT THREAD =============================
class AssistantThread(QThread):
    """
    Runs the assistant's core logic in a separate thread to prevent the GUI from freezing.
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

    def run(self):
        """The main loop for the assistant."""
        self.wish_user()
        while True:
            query = self.take_command()
            if query == "none":
                continue

            # --- Command to Function Mapping ---
            command_map = {
                "notepad": self.open_notepad,
                "command prompt": self.open_cmd,
                "camera": self.open_camera,
                "weather": self.get_weather,
                "ip address": self.get_ip_address,
                "wikipedia": self.search_wikipedia,
                "open youtube": lambda: webbrowser.open("youtube.com"),
                "open google": self.search_google,
                "send message": self.send_whatsapp,
                "play song": self.play_on_youtube,
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

            executed = False
            for command, func in command_map.items():
                if command in query:
                    func()
                    executed = True
                    break
            
            if not executed:
                self.speak("I'm not sure how to do that yet.")

    # ========================== CORE METHODS ================================
    def speak(self, text):
        """Makes the assistant speak the given text."""
        self.engine.say(text)
        self.engine.runAndWait()
        self.assistant_spoke.emit(f"Delta: {text}")

    def take_command(self):
        """Listens for a command and returns it as a string."""
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

    # ========================== COMMAND FUNCTIONS ===========================
    def wish_user(self):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12: greeting = "Good Morning"
        elif 12 <= hour < 17: greeting = "Good Afternoon"
        else: greeting = "Good Evening"
        self.speak(f"{greeting}, Sir. I am Delta. How can I help you?")

    def exit_assistant(self):
        self.speak("Goodbye, Sir!")
        sys.exit()

    def open_notepad(self):
        os.startfile("notepad.exe")

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
    
    def get_ip_address(self):
        try:
            ip = requests.get('https://api.ipify.org').text
            self.speak(f"Your IP address is {ip}")
        except requests.ConnectionError:
            self.speak("Sorry, I'm unable to connect to the internet to check your IP address.")

    def search_wikipedia(self):
        self.speak("What should I search for on Wikipedia?")
        topic = self.take_command()
        if topic != "none":
            try:
                self.speak(f"Searching for {topic} on Wikipedia...")
                results = wi.summary(topic, sentences=2)
                self.speak("According to Wikipedia...")
                self.speak(results)
            except Exception:
                self.speak(f"Sorry, I couldn't find any results for {topic}.")

    def search_google(self):
        self.speak("What should I search on Google?")
        search_term = self.take_command()
        if search_term != 'none':
            webbrowser.open(f"https://google.com/search?q={search_term}")
    
    def play_on_youtube(self):
        self.speak("What song or video should I play?")
        media = self.take_command()
        if media != 'none':
            kit.playonyt(media)
            
    def send_whatsapp(self):
        self.speak("What message should I send?")
        message = self.take_command()
        if message != 'none':
            now = datetime.datetime.now()
            # Send one minute from now
            kit.sendwhatmsg(config.WHATSAPP_PHONE_NUMBER, message, now.hour, now.minute + 1)
            self.speak("Message scheduled.")

    def get_weather(self):
        self.speak("Which city's weather would you like?")
        city = self.take_command()
        if city != "none":
            url = f""
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
    
    def get_system_status(self):
        battery = psutil.sensors_battery()
        self.speak(f"Battery is at {battery.percent} percent.")
        self.speak(f"CPU is at {psutil.cpu_percent()} percent utilization.")
        self.speak(f"RAM usage is at {psutil.virtual_memory().percent} percent.")

    def tell_joke(self):
        joke = pyjokes.get_joke()
        self.speak(joke)

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

    def take_screenshot(self):
        self.speak("What should I name the screenshot file?")
        name = self.take_command()
        if name != 'none':
            self.speak("Taking screenshot.")
            time.sleep(1)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            self.speak("Screenshot saved.")

    def find_location(self):
        self.speak("Let me check your location.")
        try:
            ip = requests.get('https://api.ipify.org').text
            url = f'https://get.geojs.io/v1/ip/geo/{ip}.json'
            geo_data = requests.get(url).json()
            city = geo_data['city']
            country = geo_data['country']
            self.speak(f"I believe we are in {city}, {country}.")
        except Exception:
            self.speak("Sorry, I'm having trouble finding our location.")

    def check_instagram_profile(self):
        self.speak("Whose profile should I look for?")
        name = self.take_command()
        if name != 'none':
            self.speak(f"Searching for {name} on Instagram.")
            webbrowser.open(f"instagram.com/{name}")

    def read_pdf(self):
        self.speak("Reading PDF.")
        try:
            book = open(config.PDF_FILE_PATH, 'rb')
            pdf_reader = PyPDF2.PdfFileReader(book)
            self.speak(f"This book has {pdf_reader.numPages} pages.")
            self.speak("Which page should I read?")
            page_num_str = self.take_command()
            try:
                page_num = int(page_num_str)
                page = pdf_reader.getPage(page_num - 1)
                text = page.extractText()
                self.speak(text)
            except ValueError:
                self.speak("That's not a valid page number.")
        except FileNotFoundError:
            self.speak("Sorry, I could not find the PDF file. Please check the path in the config file.")
    
    def calculate(self):
        self.speak("What should I calculate? For example, 5 plus 3.")
        problem = self.take_command()
        if problem != 'none':
            # Basic calculation parsing
            # This is a simplified implementation
            try:
                if 'plus' in problem:
                    nums = problem.replace('plus', '').split()
                    result = int(nums[0]) + int(nums[1])
                    self.speak(f"The result is {result}.")
                elif 'minus' in problem:
                    # ... add other operators
                    pass
                else:
                    self.speak("I can only do simple calculations right now.")
            except:
                self.speak("I couldn't understand the calculation.")

# ================================ MAIN GUI ==================================
class Main(QMainWindow):
    """The main GUI window for the assistant."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_jarvisUi()
        self.ui.setupUi(self)
        
        # Connect buttons to functions
        self.ui.pushButton_start.clicked.connect(self.start_task)
        self.ui.pushButton_exit.clicked.connect(self.close)

    def start_task(self):
        # Setup and start GIF animation
        self.ui.movie = QMovie(config.GUI_GIF_PATH)
        self.ui.label_gif.setMovie(self.ui.movie)
        self.ui.movie.start()
        
        # Start the assistant logic in its own thread
        self.assistant_thread = AssistantThread()
        self.assistant_thread.start()

# ============================= SCRIPT ENTRY POINT ===========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())
