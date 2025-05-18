import socket
from flask import Flask
from frontend import FrontendController # Importar el controlador del frontend
from backend import DatabaseManager # Importar el gestor de la base de datos
from config import Config # Importar Config desde config.py

class FlaskApp:
    def __init__(self, host=Config.FLASK_HOST, port=Config.FLASK_PORT):
        self.app = Flask(__name__, template_folder='templates') # Especificar la carpeta de templates
        self.host = host
        self.port = port
        
        # Configurar la app con valores de Config
        self.app.config['FLASK_HOST'] = Config.FLASK_HOST
        self.app.config['FLASK_PORT'] = Config.FLASK_PORT
        self.app.config['DEBUG'] = Config.DEBUG_MODE

        # Instanciar DatabaseManager
        self.db_manager = DatabaseManager() # Ahora __init__ no toma argumentos

        # Instanciar y registrar el controlador del frontend
        self.frontend_controller = FrontendController(self.app, self.db_manager)

    def get_server_info(self):
        """Obtiene la IP local y el puerto en el que corre el servidor."""
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except socket.gaierror:
            # Fallback si gethostbyname(hostname) falla (e.g., sin conexión de red activa)
            local_ip = socket.gethostbyname('localhost')
        
        # Para obtener la IP en una red local (no solo localhost)
        # Esto puede variar dependiendo de la configuración de red y S.O.
        # Un método más robusto podría ser necesario en entornos complejos.
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) # Conectar a un DNS público para obtener la IP local de la interfaz de red
            network_ip = s.getsockname()[0]
            s.close()
        except Exception:
            network_ip = local_ip # Fallback a la IP local si no se puede determinar la IP de red

        return network_ip, self.port

    def run(self):
        ip_address, port = self.get_server_info()
        print(f"Servidor Flask corriendo en http://{ip_address}:{port}")
        print(f"También accesible en http://localhost:{port} o http://127.0.0.1:{port}")
        self.app.run(host=self.host, port=self.port, debug=Config.DEBUG_MODE)

if __name__ == '__main__':
    flask_app = FlaskApp()
    # Inicializar la base de datos (cargar ejercicios)
    # flask_app.db_manager.load_exercises() # Se llama en el __init__ de DatabaseManager
    flask_app.run() 