# 📂 Organizador de Archivos

Una aplicación de escritorio moderna y eficiente construida con **Python** y **Tkinter** para gestionar y organizar tus archivos con estilo.

![Versión](https://img.shields.io/badge/version-11.0-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![Interfaz](https://img.shields.io/badge/UI-Dark_Mode-black)

## ✨ Características Principales

* **🌑 Interfaz Dark Mode:** Diseño elegante y profesional que reduce la fatiga visual.
* **📑 Paginación Inteligente:** Visualización fluida de archivos de 10 en 10 para mayor orden.
* **🔍 Buscador en Tiempo Real:** Filtra instantáneamente por nombre de archivo o por extensión (tipo).
* **✂️ Gestión de Archivos:** Funciones completas de Mover (Cortar/Pegar), Renombrar, Subir y Eliminar.
* **📥 Descarga de Carpetas:** Capacidad para exportar carpetas completas a cualquier directorio local.
* **🚀 Ventanas Emergentes Personalizadas:** Diálogos oscuros integrados que mantienen la estética del sistema.

## 🛠️ Requisitos

* Python 3.x instalado.
* Librerías estándar: `tkinter`, `os`, `shutil`.

## 🚀 Instalación y Uso

1. **Clona el repositorio:**
   ```bash
   git clone [https://github.com/Maicol843/Organizador-de-Archivos.git](https://github.com/Maicol843/Organizador-de-Archivos.git)
   cd Organizador-de-Archivos
   
2. **Ejecuta la aplicación:**
   ```bash
   python organizador.py

## 📦 Crear Ejecutable (.exe)

Si deseas generar un archivo ejecutable para Windows, asegúrate de tener instalado PyInstaller:

```bash
python -m pip install pyinstaller
```

Luego, utiliza el siguiente comando (incluyendo tu icono personalizado):
```bash
python -m PyInstaller --noconsole --onefile --icon=organizador.ico organizador.py
```

## 📸 Capturas de Pantalla
<p align="center">
  <img src="assets/Captura de pantalla 1.png" width="500">
  <img src="assets/Captura de pantalla 2.png" width="500">
</p>
