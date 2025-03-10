const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1000,
    height: 1000,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation:false,
      preload: path.join(__dirname, 'preload.js'), // Ensure preload.js exists
    },
  });

  // Corrected typo: loadFile (capital 'F')
  mainWindow.loadFile('index.html'); // Ensure index.html exists in the same directory
}

// App lifecycle events
app.whenReady().then(() => {
  createWindow();

})

// Quit the app when all windows are closed (Windows & Linux)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});