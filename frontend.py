from flask import render_template, request, redirect, url_for
import pandas as pd # Para leer los CSVs de rutinas
import os # Para listar archivos CSV
# Suponiendo que FlaskApp se inicializa en main.py y pasamos la instancia de app
# o que FrontendController es llamado desde main.py donde app está definida.

# Importaciones del backend
from backend import UserData, IMCCalculator, WorkoutGenerator, DatabaseManager
from config import Config # Si es necesario para alguna configuración específica del frontend

class FrontendController:
    def __init__(self, app, db_manager_instance):
        self.app = app
        self.db_manager = db_manager_instance # Usar la instancia de DatabaseManager
        self.imc_calculator = IMCCalculator()
        self.workout_generator = WorkoutGenerator(self.db_manager)
        self._register_routes()
        # Ya no se generan CSVs al inicio desde aquí
        # print("Iniciando generación de rutinas generales desde FrontendController...")
        # self.workout_generator.generate_and_save_routines_for_all_goals()
        # print("Rutinas generales generadas.")

    def _register_routes(self):
        self.app.add_url_rule('/', 'render_home_page', self.render_home_page, methods=['GET'])
        self.app.add_url_rule('/calculator', 'render_calculator_form', self.render_calculator_form, methods=['GET'])
        self.app.add_url_rule('/calculate', 'handle_form_submission', self.handle_form_submission, methods=['POST'])
        self.app.add_url_rule('/general_routines', 'render_general_routines_page', self.render_general_routines_page, methods=['GET'])
        # La ruta 'render_workout_results' se llamará implícitamente o por redirección
        # desde handle_form_submission, pasando los datos necesarios.

    def render_home_page(self):
        """Renderiza la página de inicio."""
        return render_template('home.html')

    def render_calculator_form(self):
        """Renderiza el formulario de la calculadora de IMC."""
        return render_template('calculator_form.html')

    def handle_form_submission(self):
        """Maneja el envío del formulario de la calculadora y muestra los resultados."""
        if request.method == 'POST':
            try:
                gender = request.form['gender']
                # Convertir altura a metros si se ingresa en cm
                height_cm = float(request.form['height'])
                height_m = height_cm / 100.0
                weight = float(request.form['weight'])
                age = int(request.form['age'])

                user_data = UserData(gender=gender, height=height_m, weight=weight, age=age)
                
                if not user_data.validate_data():
                    return self.display_error_message("Datos inválidos. Por favor, verifique la información ingresada.")

                imc = self.imc_calculator.calculate_imc(user_data.weight, user_data.height)
                imc_category = self.imc_calculator.get_imc_category(imc)
                training_goal = self.imc_calculator.determine_training_goal(imc)
                
                workout_plan = self.workout_generator.generate_routine(user_data)
                
                return render_template('workout_results.html', 
                                       user_data=user_data.to_dict(), 
                                       imc=imc, 
                                       imc_category=imc_category, 
                                       training_goal=training_goal, 
                                       workout_plan=workout_plan # workout_plan.to_html() o workout_plan.get_plan_summary()
                                      )
            except ValueError as ve:
                 return self.display_error_message(f"Error en los datos ingresados: {ve}. Asegúrese de que los números son correctos.")
            except Exception as e:
                # Log a detailed error for debugging: print(f"Error handling form: {e}")
                return self.display_error_message(f"Ocurrió un error al procesar su solicitud: {e}")
        
        return redirect(url_for('render_calculator_form'))

    def display_error_message(self, message: str):
        """Muestra un mensaje de error."""
        # Podríamos tener una plantilla específica para errores o pasar el mensaje a una plantilla existente.
        return render_template('error.html', error_message=message)

    def render_general_routines_page(self):
        """Renderiza la página que muestra las rutinas generales por objetivo desde los CSVs predefinidos."""
        routines_data = {}
        # Usar el mapeo desde Config para encontrar los archivos CSV
        # y los nombres de los objetivos (categorías de IMC son las claves en ROUTINE_CSVS)

        temp_db_manager = DatabaseManager() # Crear instancia para usar su método de carga

        for imc_category_key, csv_filename in Config.ROUTINE_CSVS.items():
            # Determinar un nombre de objetivo más descriptivo para mostrar si es necesario
            # Por ahora, usaremos imc_category_key que es "Bajo Peso", "Normal", etc.
            display_goal_name = imc_category_key 
            # Si quisiéramos el nombre del objetivo completo como "Ganancia de Masa Muscular":
            # Podemos invertir el mapeo de IMCCalculator.get_all_training_goals_with_imc_categories()
            # o añadir otro mapeo en Config. Por simplicidad, usamos imc_category_key.
            
            # Usar el método de DatabaseManager para cargar los ejercicios del archivo
            # Esto encapsula la lógica de lectura y conversión a objetos Exercise
            exercises_list = temp_db_manager.get_exercises_from_routine_file(imc_category_key)
            
            if exercises_list:
                # Convertimos la lista de objetos Exercise a lista de diccionarios para la plantilla
                routines_data[display_goal_name] = [ex.to_dict() for ex in exercises_list]
            else:
                print(f"No se pudieron cargar ejercicios para '{display_goal_name}' desde '{csv_filename}'.")
                routines_data[display_goal_name] = []
        
        return render_template('general_routines.html', routines_data=routines_data)

# La instanciación de FrontendController y su enlace con la app Flask
# se realizará en main.py 