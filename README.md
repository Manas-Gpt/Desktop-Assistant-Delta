# 🤖 Desktop Assistant Delta

Delta is a hybrid desktop assistant that combines an **Electron** frontend with a **Python** backend. The Electron window provides the GUI — a live clock, status indicator, and Start/Stop controls — while the Python script (`delta.py`) handles all voice recognition, text-to-speech, and task execution.

---

## 📁 Project Structure

```
Desktop-Assistant-Delta/
├── index.html          # Electron UI (clock, status, Start/Stop buttons)
├── main.js             # Electron main process — spawns delta.py, handles IPC & file dialogs
├── preload.js          # Electron preload — exposes electronAPI to the renderer
├── delta.py            # Python backend — voice commands, TTS, all assistant features
├── package.json        # Node.js project config (Electron dependency)
├── requirements.txt    # Python dependencies
├── .gitignore
└── node_modules/       # Installed by npm install (not committed)
```

---

## ✨ Features

### 🗣️ Voice & Text Input
- Listens for voice commands via microphone using Google Speech Recognition.
- Also accepts text commands sent from the Electron UI via stdin (`TEXT::` protocol).
- Greets the user based on the time of day (morning / afternoon / evening).

### 🌐 Web & Information
| Command | Action |
|---|---|
| `"wikipedia <topic>"` | Searches Wikipedia and reads a 2-sentence summary |
| `"open youtube"` | Opens YouTube in the browser |
| `"open google"` | Searches Google for a spoken query |
| `"play song on youtube"` | Plays a song on YouTube via pywhatkit |
| `"ip address"` | Fetches and reads out your public IP address |
| `"where am i"` | Geolocates you based on your IP address |

### 🌤️ Weather
| Command | Action |
|---|---|
| `"weather"` | Asks for a city and fetches weather from OpenWeatherMap |
| `"weather in <city>"` *(text)* | Fetches weather for the specified city directly |

> ⚠️ Requires a valid [OpenWeatherMap API key](https://openweathermap.org/api) set in `.env`.

### 🖥️ System Automation
| Command | Action |
|---|---|
| `"notepad"` | Opens Notepad |
| `"open command prompt"` | Opens Command Prompt |
| `"shut down the system"` | Shuts down the PC after 5 seconds |
| `"restart the system"` | Restarts the PC after 5 seconds |
| `"sleep the system"` | Puts the PC into sleep mode |
| `"switch the window"` | Alt+Tabs to the next window |
| `"camera"` | Opens webcam feed (press ESC to close) |

### 📊 System Monitoring
| Command | Action |
|---|---|
| `"system status"` | Reports battery %, CPU usage %, and RAM usage % |

### 🛠️ Productivity & Tools
| Command | Action |
|---|---|
| `"calculate <n> plus/minus/times/divided <n>"` | Performs basic arithmetic |
| `"take screenshot"` | Takes and saves a screenshot with a custom name |
| `"read pdf"` | Opens a file dialog, then reads a chosen page aloud |
| `"print document"` | Opens a file dialog and sends a Word doc to the default printer |
| `"send message"` | Sends a WhatsApp message via pywhatkit |
| `"instagram profile"` | Opens/searches an Instagram profile |
| `"find <location>"` | Searches Google Maps for the specified location |

### 😂 Entertainment
| Command | Action |
|---|---|
| `"tell me a joke"` | Fetches and tells a random joke |

### 🖥️ Open Any App
| Command | Action |
|---|---|
| `"open Spotify"` | Launches Spotify (or any app in your system PATH) |
| `"open calculator"` | Opens Windows Calculator |
| `"open chrome"` | Opens Google Chrome |

> Works with any app name recognized by your system. Tries `subprocess.Popen` first, then falls back to `os.startfile`.

### 📋 Clipboard
| Command | Action |
|---|---|
| `"copy to clipboard"` | Asks what to copy, then saves it to clipboard |
| `"read clipboard"` | Reads out the current clipboard content |

### 📖 Dictionary
| Command | Action |
|---|---|
| `"meaning of serendipity"` | Looks up and reads the definition (uses free dictionaryapi.dev — no key needed) |

### ⌨️ Type / Dictate Text
| Command | Action |
|---|---|
| `"type good morning"` | Types the spoken text into the currently focused window |

> Uses clipboard + Ctrl+V for reliable Unicode support.

### 🌍 Translate Text
| Command | Action |
|---|---|
| `"translate bonjour to English"` | Translates any text to the target language using Google Translate |
| `"translate hello to French"` | Supports all languages supported by Google Translate |

### 🔊 Volume Control
| Command | Action |
|---|---|
| `"mute"` | Mutes system audio |
| `"unmute"` | Unmutes system audio |
| `"increase volume"` / `"volume up"` | Increases system volume by 10% |
| `"decrease volume"` / `"volume down"` | Decreases system volume by 10% |

---

## ⚙️ Architecture

```
Electron (main.js)
    │
    ├─ Renders index.html (clock, status, Start/Stop UI)
    │
    ├─ On "Start": spawns delta.py as a child process
    │       │
    │       ├─ stdout listener → parses SAY:: and OPEN_DIALOG:: signals
    │       └─ stdin writer   → sends TEXT:: commands and file paths
    │
    └─ On "Stop": kills the Python process
```

**IPC Signals used between Electron and Python:**

| Signal | Direction | Meaning |
|---|---|---|
| `TEXT::<message>` | Electron → Python | User typed a message in UI |
| `SAY::<text>` | Python → Electron | Assistant is speaking |
| `OPEN_DIALOG::pdf` | Python → Electron | Request to open a PDF file picker |
| `OPEN_DIALOG::doc` | Python → Electron | Request to open a Word document picker |

---

## 🚀 Setup & Installation

### Prerequisites
- [Node.js](https://nodejs.org/) (v18+)
- Python 3.8+

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Desktop-Assistant-Delta.git
cd Desktop-Assistant-Delta
```

### 2. Install Python dependencies
```bash
# Create and activate a virtual environment (recommended)
python -m venv venv
.\venv\Scripts\activate     # Windows PowerShell

# Install packages
pip install -r requirements.txt
```

### 3. Install Node.js dependencies
```bash
npm install
```

### 4. Configure API Key
Create a `.env` file in the project root (copy from the template below) and add your [OpenWeatherMap API key](https://openweathermap.org/api):
```
OPENWEATHER_API_KEY=your_api_key_here
```

---

## ▶️ Running the App

```bash
npm start
```

This launches the Electron window. Click **Start** to activate Delta.

---

## 🛑 Stopping the App

Click the **Stop** button in the Electron window, or close the window entirely — the Python process is automatically terminated.

---

## 📦 Python Dependencies

| Package | Purpose |
|---|---|
| `SpeechRecognition` | Microphone voice input |
| `pyttsx3` | Text-to-speech (offline, SAPI5) |
| `requests` | Weather, IP, geolocation, and dictionary API calls |
| `wikipedia` | Wikipedia search and summaries |
| `pywhatkit` | WhatsApp messaging, YouTube playback |
| `psutil` | CPU, RAM, and battery monitoring |
| `pyjokes` | Random joke generation |
| `pyautogui` | Screenshots and keyboard automation |
| `opencv-python` | Webcam / camera feed |
| `instaloader` | Instagram profile loader |
| `PyPDF2` | PDF reading and page extraction |
| `PyQt5` | GUI framework (optional, wired but not active by default) |
| `python-dotenv` | Loads API keys from `.env` file |
| `pyperclip` | Clipboard read/write |
| `deep-translator` | Text translation via Google Translate |
| `pycaw` | Windows system volume and mute control |
| `comtypes` | Required by pycaw for Windows COM interface |

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 📝 Notes

- **PyQt5 GUI** is imported and partially wired but the Electron window is the active GUI. The PyQt5 code is present for optional future use.
- **WhatsApp messaging** via `pywhatkit` opens WhatsApp Web — ensure you are logged in.
- **Instagram** search opens Instagram's explore page; direct profile open works by exact username.
- **Volume control** (`pycaw`) is Windows-only.
- **Type text** uses clipboard + Ctrl+V internally for reliable Unicode support.
