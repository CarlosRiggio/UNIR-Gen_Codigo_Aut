class Config:
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    DEBUG_MODE = True
    # Ya no se usa un CSV_FILE_PATH único para la carga maestra
    # CSV_FILE_PATH = 'exercises.csv' 

    ROUTINE_CSVS = {
        # Mapea la CATEGORÍA DE IMC directamente al archivo CSV de la rutina
        # Las claves deben coincidir con las salidas de IMCCalculator.get_imc_category()
        "Bajo Peso": "rutina_ganancia_de_masa_muscular.csv",
        "Normal": "rutina_mantenimiento_bienestar_general.csv",
        "Sobrepeso": "rutina_prdida_de_peso.csv",
        "Obesidad": "rutina_prdida_de_peso_progresiva_salud.csv"
    } 