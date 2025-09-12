# Desktop Assistant Delta

Delta is a desktop voice assistant built with a powerful Python backend and a sleek user interface powered by Electron.js. It allows you to control your system, fetch information from the web, perform calculations, and manage tasks using voice commands.

## Features

Delta comes packed with a wide range of voice-activated commands:

### 🖥️ System & Application Control
- **Open Applications**: "Open notepad," "open command prompt," "open camera"
- **System Power**: "Shut down the system," "restart the system," "sleep the system"
- **Window Management**: "Switch the window" (Alt+Tab)
- **System Status**: "System status" (reports battery, CPU, and RAM usage)
- **Screenshots**: "Take screenshot" (prompts for a filename)

### 🌐 Web & Internet
- **Search**: "Open Google" (prompts for a search query), "Wikipedia" (prompts for a topic)
- **Open Websites**: "Open YouTube"
- **Play Music**: "Play song on YouTube" (prompts for a song name)
- **Information**: "What is my IP address?", "Where am I?" (uses IP-based geolocation)
- **Weather**: "Weather" (prompts for a city name)
- **Social Media**: "Instagram profile" (prompts for a username and can download the profile picture)

### 🛠️ Productivity & Utilities
- **Read PDFs**: "Read PDF" (opens a file dialog to select a PDF and reads a specified page)
- **Print Documents**: "Print document" (opens a file dialog to select a document and sends it to the default printer)
- **Send WhatsApp Messages**: "Send message" (sends a pre-configured message)
- **Calculations**: "Calculate" (e.g., "3 plus 5", "10 divided by 2")
- **Entertainment**: "Tell me a joke"

### 👋 Assistant Control
- **Exit**: "No thanks," "exit," "goodbye"

## Technology Stack

- **Frontend**: Electron.js, HTML, CSS, JavaScript
- **Backend**: Python
- **Core Libraries**:
  - `SpeechRecognition` for voice-to-text
  - `pyttsx3` for text-to-speech
  - `requests` for API calls
  - `pyautogui`, `psutil`, `opencv-python` for system interactions
  - `PyPDF2` for PDF reading

## Installation & Setup

Follow these steps to get Delta running on your local machine.

### Prerequisites

Make sure you have the following software installed:
- Node.js and npm
- Python 3.x and pip
- Git

### Step 1: Clone the Repository

Open your terminal or command prompt and clone this repository:

```bash
git clone https://github.com/Manas-Gpt/Desktop-Assistant-Delta.git
cd Desktop-Assistant-Delta
```

### Step 2: Install Node.js Dependencies

In the project's root directory, run the following command to install the necessary Electron packages:

```bash
npm install
```

### Step 3: Install Python Dependencies

Install all the required Python libraries using the provided list. It's recommended to do this within a virtual environment.

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install the required packages
pip install pyttsx3 SpeechRecognition wikipedia pywhatkit psutil pyjokes pyautogui opencv-python instaloader PyPDF2 requests PyQt5
```

### Step 4: Configure API Key (Required)

The weather functionality requires an API key from OpenWeatherMap.

1. Sign up for a free account at [OpenWeatherMap](https://openweathermap.org/)
2. Find your API key on your account page
3. Open the `delta.py` file and replace `"YOUR_API_KEY"` with your actual key:

```python
# In the get_weather function inside delta.py
api_key = "YOUR_API_KEY"  # Replace with your actual key
```

### Step 5: Personalize (Optional)

You can change the default phone number for sending WhatsApp messages in `delta.py`:

```python
# In the run function inside delta.py
elif "send message" in query:
    # Replace +91xxxxxxxxxx with the recipient's number including country code
    kit.sendwhatmsg("+91xxxxxxxxxx", "This is a testing protocol", ...)
```

## How to Run the Application

Once the setup is complete, you can start the application with a single command from the project's root directory:

```bash
npm start
```

This will launch the Electron UI, and the assistant will be ready to use.

## Usage Guide

1. **Start the Assistant**: Click the Start button on the interface. The status will change to "Assistant Online."
2. **Wait for the Greeting**: The assistant will greet you ("Good morning," etc.) to indicate it's ready and listening.
3. **Speak Your Command**: Clearly say one of the supported commands.
4. **Interact**: For commands like "read pdf" or "print document," a system file dialog will appear for you to select a file. For others like "Wikipedia," the assistant will ask for more input.
5. **Stop the Assistant**: Click the Stop button to terminate the Python backend script. The status will change to "Assistant Offline."

## How It Works

Delta operates on a two-part architecture:

1. **Electron Frontend**: The main window (`index.html`) provides the user interface. It communicates with the main Electron process (`main.js`) to start and stop the backend.

2. **Python Backend**: The `delta.py` script contains all the logic for voice recognition, command processing, and task execution. It runs as a separate child process.

3. **Communication Bridge**: `main.js` launches `delta.py` using Node.js's `child_process`. The two processes communicate through their standard I/O streams (stdin and stdout):
   - When the Python script needs to perform an action that requires a native UI element (like opening a file dialog), it prints a specially formatted message to its stdout (e.g., `OPEN_DIALOG::pdf`)
   - The `main.js` process listens to this output, performs the action (shows the dialog), and writes the result (the selected file path) back to the Python script's stdin
   - The Python script then reads this input to complete its task

This decoupled architecture keeps the UI responsive while the Python backend handles the heavy lifting of voice processing.
