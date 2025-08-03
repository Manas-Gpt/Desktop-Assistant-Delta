# 🧠 Delta AI - Desktop Voice Assistant

Delta is an intelligent desktop voice assistant built with Python and PyQt5 that can perform a wide range of tasks using voice commands, such as opening apps, searching online, checking weather, reading PDFs, performing calculations, controlling system settings, and more.

---

## 🚀 Features

- 🔊 Text-to-Speech and Speech Recognition
- 🌐 Open websites like YouTube, Google, Instagram, Facebook
- 📖 Wikipedia search and reading
- ⛅ Weather updates via OpenWeatherMap API
- 📩 Send WhatsApp messages
- 📬 Send emails (SMTP integration)
- 🎶 Play music via YouTube and YouTube Music
- 📷 Open webcam and capture feed
- 📸 Take screenshots with custom names
- 📚 Read content from PDF files
- 📍 Location detection via IP
- 🧮 Voice-based calculator
- 😂 Jokes using `pyjokes`
- ⚙️ System status reports (CPU, RAM, Battery)
- 🔐 Hide/Unhide files and folders
- 🧠 GUI with PyQt5 and background threading
- 📸 Download Instagram profile pictures

---

## 📦 Dependencies

### Core Libraries

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
