"""
Controlador frontend para la aplicación web Flask.
"""

from flask import render_template, request, redirect, url_for
from ..backend import UserData, IMCCalculator, WorkoutGenerator, DatabaseManager
from ..config import Config


class FrontendController:
    """Controlador para manejar las rutas y lógica de presentación de la aplicación web."""
    
    def __init__(self, app, db_manager_instance):
        self.app = app
        self.db_manager = db_manager_instance  # Usar la instancia de DatabaseManager
        self.imc_calculator = IMCCalculator()
        self.workout_generator = WorkoutGenerator(self.db_manager)
        self._register_routes()

    def _register_routes(self):
        """Registra todas las rutas de la aplicación."""
        self.app.add_url_rule('/', 'render_home_page', self.render_home_page, methods=['GET'])
        self.app.add_url_rule('/calculator', 'render_calculator_form', self.render_calculator_form, methods=['GET'])
        self.app.add_url_rule('/calculate', 'handle_form_submission', self.handle_form_submission, methods=['GET', 'POST'])
        self.app.add_url_rule('/general_routines', 'render_general_routines_page', self.render_general_routines_page, methods=['GET'])

    def render_home_page(self):
        """Renderiza la página de inicio."""
        return render_template('home.html')

    def render_calculator_form(self):
        """Renderiza el formulario de la calculadora de IMC."""
        return render_template('calculator_form.html')

    def handle_form_submission(self):
        """Maneja el envío del formulario de la calculadora y muestra los resultados."""
        if request.method == 'GET':
            return redirect(url_for('render_calculator_form'))
            
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
                                   workout_plan=workout_plan
                                  )
        except ValueError as ve:
            return self.display_error_message(f"Error en los datos ingresados: {ve}. Asegúrese de que los números son correctos.")
        except Exception as e:
            return self.display_error_message(f"Ocurrió un error al procesar su solicitud: {e}")

    def display_error_message(self, message: str):
        """Muestra un mensaje de error."""
        return render_template('error.html', error_message=message)

    def render_general_routines_page(self):
        """Renderiza la página que muestra las rutinas generales por objetivo desde los CSVs predefinidos."""
        routines_data = {}
        
        temp_db_manager = DatabaseManager()  # Crear instancia para usar su método de carga

        for imc_category_key, csv_filename in Config.ROUTINE_CSVS.items():
            # Determinar un nombre de objetivo más descriptivo para mostrar si es necesario
            # Por ahora, usaremos imc_category_key que es "Bajo Peso", "Normal", etc.
            display_goal_name = imc_category_key 
            
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