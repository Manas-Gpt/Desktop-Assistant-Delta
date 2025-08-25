# 🖥️ System Automation Features

> *This document describes features related to controlling the local operating system.*

---

## 📋 Quick Navigation
- [📝 Open Notepad](#1-open-notepad)
- [⌨️ Open Command Prompt](#2-open-command-prompt)
- [📷 Open Camera](#3-open-camera)
- [⚡ System Power Control](#4-system-power-control)
- [🔄 Switch Window](#5-switch-window)

---

## 1. 📝 Open Notepad

### Voice Command
```
"notepad"
```

### ⚙️ Action
Launches the Notepad application.

### 💡 Example Usage
- Say: *"notepad"*
- Notepad application opens instantly
- Ready for text editing

### 📌 Use Cases
- Quick note-taking
- Simple text editing
- Creating basic text files
- Temporary data storage

---

## 2. ⌨️ Open Command Prompt

### Voice Command
```
"open command prompt"
```

### ⚙️ Action
Opens the Windows Command Prompt.

### 💡 Example Usage
- Say: *"open command prompt"*
- Command Prompt window opens
- Ready for system commands

### 🔧 Common Commands
- `dir` - List directory contents
- `cd` - Change directory
- `ipconfig` - Network configuration
- `tasklist` - Show running processes

### ⚠️ Admin Note
> Some commands may require administrator privileges. Run as administrator if needed.

---

## 3. 📷 Open Camera

### Voice Command
```
"camera"
```

### ⚙️ Action
Activates the primary webcam and displays the feed in a new window. The window can be closed by pressing the `ESC` key.

### 💡 Example Usage
- Say: *"camera"*
- Camera feed opens in new window
- Press `ESC` to close

### 🎯 Features
- ✅ Real-time video feed
- ✅ Primary camera activation
- ✅ Easy close with ESC key
- ✅ Instant preview

### 🔒 Privacy Note
> Camera access is local only. No data is transmitted or stored remotely.

---

## 4. ⚡ System Power Control

### 🔴 Shutdown System

#### Voice Command
```
"shut down the system"
```

#### ⚙️ Action
Initiates a system shutdown with a 5-second timer.

#### 💡 Example Usage
- Say: *"shut down the system"*
- 5-second countdown begins
- System powers off safely

---

### 🔄 Restart System

#### Voice Command
```
"restart the system"
```

#### ⚙️ Action
Initiates a system restart with a 5-second timer.

#### 💡 Example Usage
- Say: *"restart the system"*
- 5-second countdown begins
- System restarts automatically

---

### 😴 Sleep System

#### Voice Command
```
"sleep the system"
```

#### ⚙️ Action
Puts the computer into sleep mode.

#### 💡 Example Usage
- Say: *"sleep the system"*
- System enters sleep mode immediately
- Wake with mouse/keyboard activity

### ⚠️ Power Control Safety
> **Important:** Always save your work before using power control commands. The 5-second timer provides a brief window to cancel if needed.

---

## 5. 🔄 Switch Window

### Voice Command
```
"switch the window"
```

### ⚙️ Action
Simulates an `Alt+Tab` keypress to switch to the previously active window.

### 💡 Example Usage
- Say: *"switch the window"*
- Switches to previous window
- Same as pressing `Alt+Tab`

### 🎯 Window Management
- ✅ Quick window switching
- ✅ Hands-free navigation
- ✅ Maintains window history
- ✅ Works with any application

---

## 🔧 Technical Requirements

### System Compatibility
- 💻 **OS**: Windows 10/11
- 🎤 **Voice Recognition**: Enabled
- 📷 **Camera**: Primary webcam (for camera feature)
- 🔊 **Audio**: Microphone access

### Permissions Required
- ✅ System control access
- ✅ Application launch permissions
- ✅ Camera access (for camera feature)
- ✅ Microphone access

---

## 🛡️ Security & Safety

### Best Practices
- 💾 **Always save work** before power commands
- 🔒 **Verify voice commands** before execution
- 👥 **Restrict access** to authorized users only
- 📋 **Regular backups** recommended

### Safety Features
- ⏱️ **5-second timer** for power operations
- 🚫 **ESC key** to close camera
- 🔄 **Alt+Tab simulation** for safe window switching
- 💡 **Voice confirmation** for critical commands

---

## 📞 Support & Troubleshooting

### Common Issues

#### Voice Commands Not Recognized
- Check microphone permissions
- Ensure clear pronunciation
- Verify voice recognition service is running
- Check system language settings

#### Applications Won't Open
- Verify applications are installed
- Check user permissions
- Run as administrator if needed
- Restart voice recognition service

#### Camera Won't Activate
- Check camera permissions
- Ensure camera isn't used by another app
- Verify camera drivers are installed
- Test camera in other applications

#### Power Commands Not Working
- Check system permissions
- Verify user has shutdown privileges
- Ensure no critical processes are blocking
- Try running as administrator

---

## ⌨️ Keyboard Shortcuts Reference

| Action | Voice Command | Keyboard Equivalent |
|--------|---------------|-------------------|
| Switch Window | "switch the window" | `Alt + Tab` |
| Close Camera | - | `ESC` |
| Command Prompt | "open command prompt" | `Win + R` → `cmd` |
| Notepad | "notepad" | `Win + R` → `notepad` |

---

## 🚀 Quick Start Guide

1. **🔧 Setup Requirements**
   - Enable voice recognition
   - Grant necessary permissions
   - Test microphone functionality

2. **🎯 Test Basic Commands**
   - Try "notepad" first
   - Test "switch the window"
   - Verify camera access

3. **⚡ Power Commands (Use Carefully)**
   - Save all work first
   - Test with "sleep the system"
   - Use shutdown/restart sparingly

4. **🛠️ Advanced Usage**
   - Combine with other features
   - Create custom workflows
   - Set up automated routines


---


**⚠️ Disclaimer:** Use power control commands responsibly. Always ensure important work is saved before initiating system shutdown, restart, or sleep operations.
