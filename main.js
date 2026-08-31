const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;
let pythonProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    icon: path.join(__dirname, 'static/img/logo.png'), // Ajusta la ruta a tu logo PNG
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      devTools: false // Deshabilita DevTools
    }
  });

  // Quita la barra de menú predeterminada
  mainWindow.setMenu(null);

  // Bloquea atajos de teclado de inspección (F12, Ctrl+Shift+I, etc.)
  mainWindow.webContents.on('before-input-event', (event, input) => {
    if (
      input.key === 'F12' ||
      (input.control && input.shift && input.key.toLowerCase() === 'i') ||
      (input.control && input.shift && input.key.toLowerCase() === 'j')
    ) {
      event.preventDefault();
    }
  });

  mainWindow.loadURL('http://127.0.0.1:5000');

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  const isPackaged = app.isPackaged;
  
  let pythonExecutable;
  let args = [];

  if (isPackaged) {
    // Apunta al app.exe generado por PyInstaller dentro del paquete de Electron
    pythonExecutable = path.join(process.resourcesPath, 'python_dist', 'app', 'app.exe');
  } else {
    // Modo desarrollo
    pythonExecutable = 'python';
    args = ['app.py'];
  }

  pythonProcess = spawn(pythonExecutable, args);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error: ${data}`);
  });

  // Da tiempo a que Flask levante el servidor antes de abrir la ventana
  setTimeout(createWindow, 3500);
});

app.on('window-all-closed', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});