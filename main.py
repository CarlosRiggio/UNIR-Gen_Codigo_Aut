"""
Punto de entrada principal para la aplicación de generación de rutinas de ejercicio.
"""

import sys
import os

# Agregar el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import FlaskApp

if __name__ == '__main__':
    flask_app = FlaskApp()
    flask_app.run() 