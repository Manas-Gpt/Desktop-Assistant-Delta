const { contextBridge, ipcRenderer } = require('electron');

// Expose a secure API to the window object
contextBridge.exposeInMainWorld('electronAPI', {
  // This function sends the 'start' signal
  startAssistant: () => ipcRenderer.send('start-assistant'),
  
  // NEW: This function sends the 'stop' signal
  stopAssistant: () => ipcRenderer.send('stop-assistant') 
});