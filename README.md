# Desktop-Assistant-Delta
Delta: A powerful and extensible voice-controlled desktop assistant built with Python to automate your daily tasks.

# 🤖 Desktop Assistant Delta
A comprehensive, voice-controlled desktop assistant built with Python. Delta is designed to perform a wide range of tasks—from simple web searches to system automation—all through voice commands. It features a graphical user interface (GUI) built with PyQt5.

## 📁 File Structure
```
/delta-app
  |-- index.html
  |--docs
     |-- System Design
     |-- Technical Design
     |-- Logical Design
     |-- Assumptions
     |-- Productivity and tools
     |-- System Automation
     |-- Web and Information
  |-- delta.py  
  |-- main.js   
  |-- preload.js  
  |-- package.json 
  |-- /node_modules - directory - Installed dependencies (npm install electron)
```

## ✨ Features
-   **🗣️ Voice Control**: Greets you and listens for commands.
-   **🖥️ System Automation**:
    -   Open applications (Notepad, Command Prompt).
    -   Control system power (Shutdown, Restart, Sleep).
    -   Switch between open windows (tab switching).
-   **🌐 Web & Information**:
    -   Search **Wikipedia** and read summaries.
    -   Open websites like **Google**, **YouTube**, **Facebook**, **Instagram**, and **ChatGPT**.
    -   Play songs directly on YouTube.
    -   Get your public **IP address**.
    -   Find your approximate **location** based on your IP.
-   **🛠️ Productivity & Tools**:
    -   Get the current **weather** for your city.
    -   Send **emails**.
    -   Perform voice-based **calculations** (e.g., "3 plus 5").
    -   Take **screenshots** and save them with a custom name.
    -   Open your **camera**.
    -   Check **Instagram profiles**.
-   **😂 Entertainment**:
    -   Tells you a **joke**.
-   **📊 System Monitoring**:
    -   Reports current **CPU usage**, **RAM usage**, and **battery percentage**.

## Core Libraries
| Module               | Description                                |
|----------------------|--------------------------------------------|
| `pyttsx3`            | Text-to-speech conversion                  |
| `speech_recognition` | Voice input recognition                    |
| `webbrowser`         | Open URLs in a browser                     |
| `wikipedia`          | Wikipedia search                           |
| `requests`           | Make API and web requests                  |
| `pywhatkit`          | Send WhatsApp messages, play YouTube       |
| `pyjokes`            | Generate jokes                             |
| `PyPDF2`             | Read PDF documents                         |
| `instaloader`        | Instagram profile and media downloader     |
| `cv2` (OpenCV)       | Camera interface                           |
| `psutil`             | System resource monitoring                 |
| `pyautogui`          | Automation and screenshot                  |
| `datetime`, `time`   | Handle date/time                           |
| `os`, `sys`          | System operations                          |
| `smtplib`            | Email sending with SMTP                    |
| `operator`           | Arithmetic operator mapping                |
| `urllib.parse`       | For encoding YouTube Music search URL      |
| `BeautifulSoup`      | Web scraping                               |

### GUI Modules
- `PyQt5.QtCore`
- `PyQt5.QtGui`
- `PyQt5.QtWidgets`

---

## 🧩 GUI Components (PyQt5)
- **Main Thread** for updating time
- **Delta Thread** for continuous voice command listening
- **Buttons** to start/close assistant
- **Labels** for displaying animations (GIFs)
- **Text browser** for current time display
