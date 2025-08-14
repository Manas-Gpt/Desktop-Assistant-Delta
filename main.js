const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

// Keep a reference to the python process so we can kill it later
let pythonProcess;

const createWindow = () => {
  const win = new BrowserWindow({
    width: 500,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });
  win.loadFile('index.html');
};

app.whenReady().then(createWindow);

// Listen for the 'start-assistant' event from the button
ipcMain.on('start-assistant', () => {
  console.log('Starting Python script...');

  // Spawn the python process
  pythonProcess = spawn('python', ['delta.py']);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python Script: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error: ${data}`);
  });
});

// NEW: Listen for the 'stop-assistant' event
ipcMain.on('stop-assistant', () => {
  // Check if the process exists and kill it
  if (pythonProcess) {
    console.log('Stopping Python script...');
    pythonProcess.kill();
    pythonProcess = null;
  }
});

app.on('window-all-closed', () => {
  // Also kill the process if the app is closed
  if (pythonProcess) {
    pythonProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});