const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let pythonProcess;
let win;

const createWindow = () => {
  win = new BrowserWindow({
    width: 500,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });
  win.loadFile('index.html');
};

app.whenReady().then(createWindow);

ipcMain.on('start-assistant', () => {
  console.log('Starting Python script...');
  pythonProcess = spawn('python', ['-u', 'delta.py']); 

  let buffer = '';
  pythonProcess.stdout.on('data', (data) => {
    buffer += data.toString();
    let lines = buffer.split('\n');

    for (let i = 0; i < lines.length - 1; i++) {
      let line = lines[i].trim();
      if (!line) continue; 

      console.log(`Python Line: ${line}`);

      if (line.startsWith('WEATHER_DATA::')) {
        // ... Weather logic
      }

      if (line.startsWith('OPEN_DIALOG::')) {
        console.log("Signal Matched! Opening file dialog...");
        const fileType = line.replace('OPEN_DIALOG::', '').trim();
        
        let options = {
          title: 'Select a File',
          properties: ['openFile'],
          filters: []
        };
        
        if (fileType === 'pdf') {
          options.filters.push({ name: 'PDF Documents', extensions: ['pdf'] });
        } else if (fileType === 'doc') {
          options.filters.push({ name: 'Word Documents', extensions: ['doc', 'docx'] });
        }
        options.filters.push({ name: 'All Files', extensions: ['*'] });
        
        dialog.showOpenDialog(options).then(result => {
          if (!result.canceled && result.filePaths.length > 0) {
            const filePath = result.filePaths[0];
            pythonProcess.stdin.write(filePath + '\n');
          }
        }).catch(err => {
          console.error("File Dialog Error:", err);
        });
      }
    }
    buffer = lines[lines.length - 1];
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error: ${data.toString()}`);
  });
});

// Stop assistant and window close logic
ipcMain.on('stop-assistant', () => {
  if (pythonProcess) {
    console.log('Stopping Python script...');
    pythonProcess.kill();
    pythonProcess = null;
  }
});

app.on('window-all-closed', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
// The extra '}' that was here has been removed.
