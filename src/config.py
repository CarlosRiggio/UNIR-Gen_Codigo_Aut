"""
Configuración de la aplicación.
"""


class Config:
    """Clase de configuración para la aplicación de generación de rutinas."""
    
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    DEBUG_MODE = True

    ROUTINE_CSVS = {
        # Mapea la CATEGORÍA DE IMC directamente al archivo CSV de la rutina
        # Las claves deben coincidir con las salidas de IMCCalculator.get_imc_category()
        "Bajo Peso": "data/rutina_ganancia_de_masa_muscular.csv",
        "Normal": "data/rutina_mantenimiento_bienestar_general.csv",
        "Sobrepeso": "data/rutina_prdida_de_peso.csv",
        "Obesidad": "data/rutina_prdida_de_peso_progresiva_salud.csv"
    } 