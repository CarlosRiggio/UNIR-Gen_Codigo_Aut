# Análisis y Planificación de Proyecto
_Exported on 5/18/2025 at 11:05:46 GMT+2 from Cursor (0.50.4)_

---

**User**

Estamos realizando un proyecto y hemos realizado un @prompt.md , quiero que lo analices a fondo, realizes un plan punto por punto y lo apliques paso a paso.

Debes razonar pensando con claridad y eficiencia

---

**Cursor**

¡Entendido! He analizado el archivo `prompt.md` que has proporcionado. Basándome en él, he elaborado el siguiente plan para desarrollar tu proyecto de generación de rutinas de ejercicios personalizadas. Procederé a implementarlo paso a paso.

**Plan de Desarrollo:**

1.  **Creación de la Estructura de Archivos:**
    *   Crear el archivo principal `main.py`.
    *   Crear el archivo para la lógica del frontend `frontend.py`.
    *   Crear el archivo para la lógica del backend `backend.py`.
    *   Crear un archivo `exercises.csv` que servirá como base de datos.
    *   Crear un directorio `templates` para las plantillas HTML de Flask.
    *   Crear un archivo `requirements.txt` para listar las dependencias.

2.  **Configuración Inicial y `main.py`:**
    *   Definir la clase `Config` (puede ir en `main.py` inicialmente o en un `config.py` separado).
    *   Implementar la clase `FlaskApp` en `main.py` para configurar y ejecutar la aplicación Flask. Esta clase también manejará la obtención de la información del servidor (IP y puerto) para mostrarla en la terminal.

3.  **Desarrollo del Backend (`backend.py`):**
    *   Implementar la clase `UserData` para almacenar y validar los datos del usuario.
    *   Implementar la clase `IMCCalculator` con métodos para calcular el IMC, obtener la categoría del IMC y determinar el objetivo del entrenamiento.
    *   Implementar la clase `Exercise` para representar la estructura de un ejercicio.
    *   Implementar la clase `DatabaseManager` para cargar y gestionar los datos desde `exercises.csv`. Incluirá un método para obtener ejercicios según criterios.
    *   Implementar la clase `WorkoutPlan` para estructurar la rutina generada.
    *   Implementar la clase `WorkoutGenerator` para generar la rutina de ejercicios utilizando el `DatabaseManager` y los datos del usuario.

4.  **Desarrollo del Frontend (`frontend.py`):**
    *   Implementar la clase `FrontendController` que manejará las rutas de la aplicación Flask.
    *   Definir rutas para:
        *   La página de inicio (`/`).
        *   El formulario para ingresar datos (`/calculator`).
        *   Mostrar los resultados de la rutina (`/workout`).
    *   Crear funciones para renderizar las plantillas HTML correspondientes y manejar la lógica de envío de formularios.

5.  **Creación de Plantillas HTML (en el directorio `templates`):**
    *   `home.html`: Página de bienvenida.
    *   `calculator_form.html`: Formulario para que el usuario ingrese sus datos.
    *   `workout_results.html`: Página para mostrar la rutina de ejercicios generada.

6.  **Poblar `exercises.csv`:**
    *   Definir las columnas (ej: id, name, description, imc_range, difficulty, category, gender_specific, equipment_needed).
    *   Añadir datos de ejemplo para diferentes rangos de IMC y objetivos.

7.  **Crear `requirements.txt`:**
    *   Añadir las dependencias necesarias (ej: Flask, pandas).

8.  **Pruebas y Refinamientos:**
    *   Probar la funcionalidad completa de la aplicación.
    *   Realizar ajustes y correcciones según sea necesario.

Comenzaré con el primer paso: la creación de la estructura de archivos.

Voy a crear el archivo `main.py`.


Ahora crearé el archivo `frontend.py`.


Ahora crearé el archivo `backend.py`.


Ahora crearé el archivo `exercises.csv` para la base de datos.


```csv
id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed

```

Voy a crear el directorio `templates`.


Y ahora, el archivo `requirements.txt`.


```pip-requirements
Flask
pandas

```

Hemos completado el primer paso del plan. Ahora pasaré al Paso 2: Configuración Inicial y `main.py`.

Comenzaré definiendo la clase `Config` y la clase `FlaskApp` en `main.py`.


```python
import socket
from flask import Flask

class Config:
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    CSV_FILE_PATH = 'exercises.csv'
    DEBUG_MODE = True

class FlaskApp:
    def __init__(self, host=Config.FLASK_HOST, port=Config.FLASK_PORT):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        # Aquí se registrarán las rutas más adelante

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
    flask_app.run()

```

He actualizado `main.py` con la configuración inicial de Flask y la lógica para mostrar la IP y el puerto.

Ahora, avanzaremos al Paso 3: Desarrollo del Backend (`backend.py`). Comenzaré implementando las clases `UserData` y `IMCCalculator`.


```python
class UserData:
    def __init__(self, gender: str, height: float, weight: float, age: int):
        self.gender = gender
        self.height = height  # en metros
        self.weight = weight  # en kg
        self.age = age

    def validate_data(self) -> bool:
        """Valida los datos del usuario."""
        if not all([self.gender, isinstance(self.height, (int, float)), isinstance(self.weight, (int, float)), isinstance(self.age, int)]):
            return False
        if self.height <= 0 or self.weight <= 0 or self.age <= 0:
            return False
        if self.gender.lower() not in ['male', 'female', 'other', 'masculino', 'femenino', 'otro']:
            # Permitimos varios términos para el género
            return False
        return True

    def to_dict(self) -> dict:
        """Convierte los datos del usuario a un diccionario."""
        return {
            'gender': self.gender,
            'height': self.height,
            'weight': self.weight,
            'age': self.age
        }

class IMCCalculator:
    # Umbrales basados en clasificaciones comunes, pueden ajustarse.
    UNDERWEIGHT_THRESHOLD = 18.5
    NORMAL_THRESHOLD_LOWER = 18.5
    NORMAL_THRESHOLD_UPPER = 24.9
    OVERWEIGHT_THRESHOLD_LOWER = 25
    OVERWEIGHT_THRESHOLD_UPPER = 29.9
    # OBESE_THRESHOLD = 30 (implícito, cualquier valor >= OVERWEIGHT_THRESHOLD_UPPER si no se define más)

    def calculate_imc(self, weight: float, height: float) -> float:
        """Calcula el Índice de Masa Corporal (IMC)."""
        if height <= 0:
            raise ValueError("La altura debe ser mayor que cero.")
        return round(weight / (height ** 2), 2)

    def get_imc_category(self, imc: float) -> str:
        """Obtiene la categoría del IMC."""
        if imc < self.UNDERWEIGHT_THRESHOLD:
            return "Bajo Peso"
        elif self.NORMAL_THRESHOLD_LOWER <= imc <= self.NORMAL_THRESHOLD_UPPER:
            return "Normal"
        elif self.OVERWEIGHT_THRESHOLD_LOWER <= imc <= self.OVERWEIGHT_THRESHOLD_UPPER:
            return "Sobrepeso"
        else:  # imc > self.OVERWEIGHT_THRESHOLD_UPPER
            return "Obesidad"

    def determine_training_goal(self, imc: float) -> str:
        """Determina el objetivo del entrenamiento según el IMC."""
        category = self.get_imc_category(imc)
        if category == "Bajo Peso":
            return "Ganancia de Masa Muscular"
        elif category == "Normal":
            return "Mantenimiento y Bienestar General"
        elif category == "Sobrepeso":
            return "Pérdida de Peso"
        else:  # Obesidad
            return "Pérdida de Peso Progresiva y Salud"

```

He añadido las clases `UserData` e `IMCCalculator` a `backend.py`.

Continuaré con el desarrollo del backend implementando las clases `Exercise` y `DatabaseManager`.


```python
// ... existing code ...
import pandas as pd
from main import Config # Para acceder a CSV_FILE_PATH
from typing import List, Dict, Any

class Exercise:
    def __init__(self, id: int, name: str, description: str, imc_range: str, 
                 difficulty: str, category: str, gender_specific: str, 
                 equipment_needed: List[str]):
        self.id = id
        self.name = name
        self.description = description
        self.imc_range = imc_range # e.g., "Bajo Peso", "Normal", "Sobrepeso", "Obesidad"
        self.difficulty = difficulty # e.g., "Principiante", "Intermedio", "Avanzado"
        self.category = category # e.g., "Fuerza", "Cardio", "Flexibilidad"
        self.gender_specific = gender_specific # e.g., "Any", "Male", "Female"
        self.equipment_needed = equipment_needed

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

class DatabaseManager:
    def __init__(self, csv_file_path: str = Config.CSV_FILE_PATH):
        self.csv_file_path = csv_file_path
        self.exercises_data = None
        self.load_exercises()

    def load_exercises(self):
        """Carga los ejercicios desde el archivo CSV."""
        try:
            self.exercises_data = pd.read_csv(self.csv_file_path)
            # Convertir la columna 'equipment_needed' de string a lista
            # Asumimos que en el CSV está como "item1,item2"
            if 'equipment_needed' in self.exercises_data.columns:
                self.exercises_data['equipment_needed'] = self.exercises_data['equipment_needed'].apply(
                    lambda x: [item.strip() for item in str(x).split(',')] if pd.notna(x) and str(x).strip() != '' else []
                )
            else:
                # Si la columna no existe, inicializarla como listas vacías para evitar errores posteriores
                self.exercises_data['equipment_needed'] = [[] for _ in range(len(self.exercises_data))]

        except FileNotFoundError:
            print(f"Error: El archivo CSV '{self.csv_file_path}' no fue encontrado.")
            # Crear un DataFrame vacío con las columnas esperadas si el archivo no existe
            self.exercises_data = pd.DataFrame(columns=[
                'id', 'name', 'description', 'imc_range', 'difficulty', 
                'category', 'gender_specific', 'equipment_needed'
            ])
        except Exception as e:
            print(f"Error al cargar el archivo CSV: {e}")
            self.exercises_data = pd.DataFrame(columns=[
                'id', 'name', 'description', 'imc_range', 'difficulty', 
                'category', 'gender_specific', 'equipment_needed'
            ])

    def get_exercises_by_criteria(self, imc_category: str, gender: str = 'Any') -> List[Exercise]:
        """Filtra los ejercicios según la categoría de IMC y el género."""
        if self.exercises_data is None or self.exercises_data.empty:
            return []

        # Filtrar por categoría de IMC
        # El prompt.md dice "Cada ejercicio estará etiquetado en función del rango"
        # por lo que una comparación directa de la categoría de IMC debería funcionar.
        filtered_df = self.exercises_data[self.exercises_data['imc_range'].str.lower() == imc_category.lower()]

        # Filtrar por género (si no es 'Any')
        # Considera ejercicios 'Any' o específicos para el género dado.
        if gender.lower() != 'any':
            filtered_df = filtered_df[
                (filtered_df['gender_specific'].str.lower() == gender.lower()) | 
                (filtered_df['gender_specific'].str.lower() == 'any')
            ]
        
        exercises_list = []
        for _, row in filtered_df.iterrows():
            # Asegurarse de que el id es un entero, manejando posibles NaN o formatos incorrectos
            try:
                exercise_id = int(row['id'])
            except ValueError:
                print(f"Advirtencia: ID de ejercicio no válido '{row['id']}' encontrado. Saltando ejercicio.")
                continue # Saltar este ejercicio si el ID no es un entero válido

            exercises_list.append(Exercise(
                id=exercise_id,
                name=str(row['name']),
                description=str(row['description']),
                imc_range=str(row['imc_range']),
                difficulty=str(row['difficulty']),
                category=str(row['category']),
                gender_specific=str(row['gender_specific']),
                equipment_needed=row['equipment_needed'] if isinstance(row['equipment_needed'], list) else []
            ))
        return exercises_list

    def update_exercise_database(self, new_exercise: Exercise):
        """Añade un nuevo ejercicio al DataFrame y (opcionalmente) al CSV."""
        # Esta función es para cumplir con el diagrama, pero su implementación completa
        # (guardar en CSV) puede ser más compleja y se omite por brevedad inicial.
        if self.exercises_data is None:
            self.load_exercises() # Asegurarse de que los datos están cargados
        
        new_exercise_df = pd.DataFrame([new_exercise.to_dict()])
        self.exercises_data = pd.concat([self.exercises_data, new_exercise_df], ignore_index=True)
        # Para persistir los cambios en el archivo CSV:
        # self.exercises_data.to_csv(self.csv_file_path, index=False)
        print(f"Ejercicio '{new_exercise.name}' añadido a la base de datos en memoria.")

# Las clases WorkoutPlan y WorkoutGenerator se añadirán después.

```

He incorporado las clases `Exercise` y `DatabaseManager` en `backend.py`.

Ahora, añadiré las clases `WorkoutPlan` y `WorkoutGenerator` para completar la lógica principal del backend.


```python
// ... existing code ...
import random # Para seleccionar ejercicios aleatoriamente si es necesario

class WorkoutPlan:
    def __init__(self, exercises: List[Exercise], goal: str, duration: int = 30, difficulty_level: str = "Intermedio"):
        self.exercises = exercises
        self.goal = goal
        self.duration = duration  # Duración total estimada en minutos
        self.difficulty_level = difficulty_level

    def get_plan_summary(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "duration_minutes": self.duration,
            "difficulty_level": self.difficulty_level,
            "number_of_exercises": len(self.exercises),
            "exercises": [ex.to_dict() for ex in self.exercises]
        }

    def to_html(self) -> str:
        """Genera una representación HTML simple del plan de entrenamiento."""
        if not self.exercises:
            return "<p>No se encontraron ejercicios para este plan.</p>"

        html_string = f"<h3>Objetivo: {self.goal}</h3>"
        html_string += f"<p>Dificultad: {self.difficulty_level}, Duración Estimada: {self.duration} min</p>"
        html_string += "<ul>"
        for ex in self.exercises:
            html_string += f"<li><b>{ex.name}</b> ({ex.category}, {ex.difficulty}): {ex.description}. "
            if ex.equipment_needed and ex.equipment_needed != ['']:
                html_string += f"<i>Equipo: {', '.join(ex.equipment_needed)}</i></li>"
            else:
                html_string += "<i>Equipo: Ninguno</i></li>"
        html_string += "</ul>"
        return html_string

class WorkoutGenerator:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.imc_calculator = IMCCalculator() # Para determinar el objetivo si es necesario

    def generate_routine(self, user_data: UserData, num_exercises: int = 5) -> WorkoutPlan:
        """Genera una rutina de ejercicios basada en los datos del usuario."""
        imc = self.imc_calculator.calculate_imc(user_data.weight, user_data.height)
        imc_category = self.imc_calculator.get_imc_category(imc)
        training_goal = self.imc_calculator.determine_training_goal(imc)
        
        # Obtener ejercicios que coincidan con la categoría de IMC y el género del usuario
        # El prompt.md dice: "se extrae de la base de datos de ejercicios aquellos que estén indicados 
        # para la finalidad del entrenamiento sugerida por el sistema"
        # La finalidad ya está determinada por el IMC (training_goal) y la categoría de IMC.
        # DatabaseManager ya filtra por imc_category (que está directamente ligada al training_goal)
        available_exercises = self.db_manager.get_exercises_by_criteria(
            imc_category=imc_category, 
            gender=user_data.gender
        )

        if not available_exercises:
            return WorkoutPlan(exercises=[], goal=training_goal, difficulty_level="Variable")

        # Lógica de selección de ejercicios (ej. aleatoria, basada en dificultad, etc.)
        # Por ahora, seleccionamos aleatoriamente si hay más de los necesarios.
        # Una lógica más avanzada podría considerar la variedad de categorías, dificultad, etc.
        if len(available_exercises) > num_exercises:
            selected_exercises = random.sample(available_exercises, num_exercises)
        else:
            selected_exercises = available_exercises
        
        # Determinar la dificultad general del plan basado en los ejercicios seleccionados
        # Esto es una simplificación; podría ser más complejo.
        plan_difficulty = "Intermedio" # Default
        if selected_exercises:
            difficulties = [ex.difficulty for ex in selected_exercises if ex.difficulty]
            if difficulties:
                # Podríamos tomar la más común o la más alta, etc.
                plan_difficulty = max(set(difficulties), key=difficulties.count) 

        return WorkoutPlan(
            exercises=selected_exercises, 
            goal=training_goal, 
            difficulty_level=plan_difficulty
        )

    # filter_exercises_by_goal y create_workout_plan del diagrama de clases original
    # están implícitamente manejados dentro de generate_routine y DatabaseManager.
    # Si se necesita una lógica más explícita o granular, se pueden descomponer.

```

He eliminado el comentario marcador de posición `Las clases WorkoutPlan y WorkoutGenerator se añadirán después.` al final del archivo `backend.py`.


```python
// ... existing code ...
    # Si se necesita una lógica más explícita o granular, se pueden descomponer.

```

Parece que la última edición no eliminó el comentario como esperaba. Voy a intentarlo de nuevo, asegurándome de proporcionar suficiente contexto.


```python
            exercises=selected_exercises, 
            goal=training_goal, 
            difficulty_level=plan_difficulty
        )

    # filter_exercises_by_goal y create_workout_plan del diagrama de clases original
    # están implícitamente manejados dentro de generate_routine y DatabaseManager.
    # Si se necesita una lógica más explícita o granular, se pueden descomponer.

# Las clases WorkoutPlan y WorkoutGenerator se añadirán después. 
// ... existing code ...
```

Parece que sigo teniendo problemas para eliminar ese comentario específico con `edit_file`. Puede que la IA que aplica los cambios no lo esté interpretando correctamente o que el comentario ya no exista y la lectura del archivo esté desactualizada.

Por ahora, asumiré que el comentario residual no afectará la ejecución y continuaré con el siguiente paso para no bloquear el progreso. Si surgen problemas más adelante debido a esto, lo revisaré.

Pasamos al **Paso 4: Desarrollo del Frontend (`frontend.py`)**.

Comenzaré implementando la clase `FrontendController` y definiré las rutas básicas y la lógica para interactuar con el backend. También necesitaré importar las clases necesarias de `backend.py` y `main.py`.


```python
from flask import render_template, request, redirect, url_for
# Suponiendo que FlaskApp se inicializa en main.py y pasamos la instancia de app
# o que FrontendController es llamado desde main.py donde app está definida.

# Importaciones del backend
from backend import UserData, IMCCalculator, WorkoutGenerator, DatabaseManager
from main import Config # Si es necesario para alguna configuración específica del frontend

class FrontendController:
    def __init__(self, app, db_manager_instance):
        self.app = app
        self.db_manager = db_manager_instance # Usar la instancia de DatabaseManager
        self.imc_calculator = IMCCalculator()
        self.workout_generator = WorkoutGenerator(self.db_manager)
        self._register_routes()

    def _register_routes(self):
        self.app.add_url_rule('/', 'render_home_page', self.render_home_page, methods=['GET'])
        self.app.add_url_rule('/calculator', 'render_calculator_form', self.render_calculator_form, methods=['GET'])
        self.app.add_url_rule('/calculate', 'handle_form_submission', self.handle_form_submission, methods=['POST'])
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

# La instanciación de FrontendController y su enlace con la app Flask
# se realizará en main.py

```

Ahora necesito modificar `main.py` para que instancie y utilice `FrontendController` y `DatabaseManager`.


```python
// ... existing code ...
from flask import Flask
from frontend import FrontendController # Importar el controlador del frontend
from backend import DatabaseManager # Importar el gestor de la base de datos

class Config:
// ... existing code ...
class FlaskApp:
    def __init__(self, host=Config.FLASK_HOST, port=Config.FLASK_PORT):
        self.app = Flask(__name__, template_folder='templates') # Especificar la carpeta de templates
        self.host = host
        self.port = port
        
        # Configurar la app con valores de Config
        self.app.config['FLASK_HOST'] = Config.FLASK_HOST
        self.app.config['FLASK_PORT'] = Config.FLASK_PORT
        self.app.config['CSV_FILE_PATH'] = Config.CSV_FILE_PATH
        self.app.config['DEBUG'] = Config.DEBUG_MODE

        # Instanciar DatabaseManager
        self.db_manager = DatabaseManager(csv_file_path=Config.CSV_FILE_PATH)

        # Instanciar y registrar el controlador del frontend
        self.frontend_controller = FrontendController(self.app, self.db_manager)

    def get_server_info(self):
// ... existing code ...
if __name__ == '__main__':
    flask_app = FlaskApp()
    # Inicializar la base de datos (cargar ejercicios)
    # flask_app.db_manager.load_exercises() # Se llama en el __init__ de DatabaseManager
    flask_app.run()

```

Con `frontend.py` y `main.py` actualizados, ahora pasamos al **Paso 5: Creación de Plantillas HTML**.

Crearé tres archivos HTML básicos en el directorio `templates`: `home.html`, `calculator_form.html`, y `workout_results.html`. También crearé una plantilla `error.html` que es referenciada en `frontend.py`.

Primero, `home.html`:


```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de Rutinas de Ejercicio</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        .container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bienvenido al Generador de Rutinas de Ejercicio</h1>
        <p>Obtén una rutina de ejercicios personalizada basada en tu Índice de Masa Corporal (IMC).</p>
        <p><a href="{{ url_for('render_calculator_form') }}">Comenzar aquí</a></p>
    </div>
</body>
</html>

```

Ahora, `calculator_form.html`:


```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de IMC y Rutina</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        .container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 500px; margin: auto; }
        h1 { color: #333; text-align: center;}
        label { display: block; margin-top: 10px; }
        input[type="text"], input[type="number"], select {
            width: calc(100% - 22px);
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 20px;
            width: 100%;
            font-size: 16px;
        }
        input[type="submit"]:hover { background-color: #0056b3; }
        .error { color: red; margin-top: 10px; }
        a { display: inline-block; margin-top:15px; color: #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Calcula tu Rutina</h1>
        <form action="{{ url_for('handle_form_submission') }}" method="POST">
            <div>
                <label for="gender">Sexo:</label>
                <select id="gender" name="gender" required>
                    <option value="male">Masculino</option>
                    <option value="female">Femenino</option>
                    <option value="other">Otro</option>
                </select>
            </div>
            <div>
                <label for="height">Altura (cm):</label>
                <input type="number" id="height" name="height" step="0.1" required placeholder="Ej: 175">
            </div>
            <div>
                <label for="weight">Peso (kg):</label>
                <input type="number" id="weight" name="weight" step="0.1" required placeholder="Ej: 70">
            </div>
            <div>
                <label for="age">Edad:</label>
                <input type="number" id="age" name="age" required placeholder="Ej: 30">
            </div>
            <input type="submit" value="Calcular y Generar Rutina">
        </form>
        <a href="{{ url_for('render_home_page') }}">Volver al inicio</a>
    </div>
</body>
</html>

```

Ahora, `workout_results.html`:


```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultados de tu Rutina</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        .container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 700px; margin: auto; }
        h1, h2, h3 { color: #333; }
        .user-data, .imc-results, .workout-plan { margin-bottom: 20px; padding: 15px; border: 1px solid #eee; border-radius: 5px; }
        ul { list-style-type: none; padding: 0; }
        li { background-color: #f9f9f9; margin-bottom: 8px; padding: 10px; border-radius: 4px; }
        li b { color: #007bff; }
        a { display: inline-block; margin-top:20px; color: #007bff; text-decoration: none;}
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Resultados de tu Rutina Personalizada</h1>

        {% if user_data %}
        <div class="user-data">
            <h2>Tus Datos:</h2>
            <p><strong>Sexo:</strong> {{ user_data.gender }}</p>
            <p><strong>Altura:</strong> {{ user_data.height * 100 }} cm</p> {# Convertir de nuevo a cm para mostrar #}
            <p><strong>Peso:</strong> {{ user_data.weight }} kg</p>
            <p><strong>Edad:</strong> {{ user_data.age }} años</p>
        </div>
        {% endif %}

        {% if imc is defined and imc_category and training_goal %}
        <div class="imc-results">
            <h2>Resultados del IMC:</h2>
            <p><strong>Tu IMC es:</strong> {{ imc }}</p>
            <p><strong>Categoría de IMC:</strong> {{ imc_category }}</p>
            <p><strong>Objetivo de Entrenamiento Sugerido:</strong> {{ training_goal }}</p>
        </div>
        {% endif %}

        {% if workout_plan %}
        <div class="workout-plan">
            <h2>Tu Plan de Entrenamiento:</h2>
            {{ workout_plan.to_html() | safe }}
        </div>
        {% else %}
        <p>No se pudo generar un plan de entrenamiento con los datos proporcionados o no hay ejercicios disponibles.</p>
        {% endif %}

        <a href="{{ url_for('render_calculator_form') }}">Calcular otra rutina</a><br>
        <a href="{{ url_for('render_home_page') }}">Volver al inicio</a>
    </div>
</body>
</html>

```

Y finalmente, `error.html`:


```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        .container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 500px; margin: auto; text-align: center; }
        h1 { color: red; }
        a { display: inline-block; margin-top:20px; color: #007bff; text-decoration: none;}
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Error en la Aplicación</h1>
        <p>{{ error_message | default('Ha ocurrido un error inesperado.') }}</p>
        <a href="{{ url_for('render_calculator_form') }}">Intentar de nuevo</a><br>
        <a href="{{ url_for('render_home_page') }}">Volver al inicio</a>
    </div>
</body>
</html>

```

Hemos creado las plantillas HTML básicas.

Ahora, el **Paso 6: Poblar `exercises.csv`**.

Añadiré algunas filas de ejemplo al archivo `exercises.csv` para que la aplicación tenga datos con los que trabajar. He definido las columnas como: `id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed`.
`imc_range` corresponderá a "Bajo Peso", "Normal", "Sobrepeso", "Obesidad".
`equipment_needed` será una lista separada por comas, o vacía si no se necesita equipo.


```csv
id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed
1,Flexiones de Pecho,Ejercicio de fuerza para el tren superior,Normal,Principiante,Fuerza,Any,
2,Sentadillas,Ejercicio de fuerza para piernas y glúteos,Normal,Principiante,Fuerza,Any,
3,Plancha Abdominal,Ejercicio isométrico para el core,Normal,Intermedio,Fuerza,Any,
4,Correr Suave (Trote),Ejercicio cardiovascular de bajo impacto,Sobrepeso,Principiante,Cardio,Any,
5,Elevaciones Laterales de Hombros,Ejercicio para deltoides,Bajo Peso,Principiante,Fuerza,Any,Mancuernas Pequeñas
6,Curl de Bíceps con Mancuernas,Ejercicio para bíceps,Bajo Peso,Principiante,Fuerza,Any,Mancuernas
7,Caminata Rápida,Ejercicio cardiovascular moderado,Obesidad,Principiante,Cardio,Any,
8,Zancadas (Lunges),Ejercicio para piernas y glúteos,Normal,Intermedio,Fuerza,Any,
9,Burpees,Ejercicio compuesto de cuerpo completo,Normal,Avanzado,Cardio,Any,
10,Remo con Mancuerna,Ejercicio de espalda y bíceps,Bajo Peso,Intermedio,Fuerza,Any,Mancuerna,Banco (opcional)
11,Prensa de Hombros con Mancuernas,Ejercicio de hombros,Bajo Peso,Intermedio,Fuerza,Any,Mancuernas
12,Saltos de Tijera (Jumping Jacks),Calentamiento cardiovascular,Sobrepeso,Principiante,Cardio,Any,
13,Bicicleta Estática,Ejercicio cardiovascular de bajo impacto,Obesidad,Principiante,Cardio,Any,Bicicleta Estática
14,Estiramiento de Isquiotibiales,Estiramiento para la parte posterior de las piernas,Normal,Principiante,Flexibilidad,Any,
15,Estiramiento de Cuádriceps,Estiramiento para la parte frontal de los muslos,Normal,Principiante,Flexibilidad,Any,
16,Sentadilla Sumo,Variación de sentadilla para aductores y glúteos,Bajo Peso,Intermedio,Fuerza,Any,Pesa Rusa (opcional)
17,Caminata Inclinada,Cardio con mayor intensidad para piernas,Sobrepeso,Intermedio,Cardio,Any,Cinta de correr
18,Natación,Ejercicio de cuerpo completo de bajo impacto,Obesidad,Intermedio,Cardio,Any,Piscina
19,Yoga para principiantes,Mejora flexibilidad y fuerza,Normal,Principiante,Flexibilidad,Any,Mat de yoga
20,Pilates Mat,Fortalecimiento del core y flexibilidad,Normal,Intermedio,Fuerza,Any,Mat

```

El archivo `exercises.csv` ha sido poblado con datos de ejemplo.

El **Paso 7: Crear `requirements.txt`** ya fue realizado al inicio cuando creamos la estructura de archivos. El contenido actual es:
```
Flask
pandas
```
Esto cubre las dependencias que hemos usado.

Finalmente, llegamos al **Paso 8: Pruebas y Refinamientos**.

En este punto, la estructura básica de la aplicación está completa según el `prompt.md`. Se podría ejecutar `python main.py` para iniciar el servidor Flask y probar la aplicación abriendo la dirección proporcionada en un navegador.

Dado que no puedo ejecutar la aplicación directamente ni interactuar con un navegador, consideraré esta fase como una revisión de la coherencia del código desarrollado.

**Posibles Refinamientos y Puntos a Considerar (para desarrollo futuro):**

*   **Manejo de Errores y Validación:** Aunque se ha implementado validación básica y manejo de errores, podría robustecerse (ej. validaciones más específicas en `UserData`, manejo más detallado de errores de CSV en `DatabaseManager`).
*   **Lógica de `WorkoutGenerator`:** La selección de ejercicios es actualmente simple (aleatoria si hay muchos). Podría mejorarse para asegurar variedad de grupos musculares, alternar dificultad, considerar preferencias del usuario (si se añadieran), etc.
*   **Persistencia de `DatabaseManager`:** La función `update_exercise_database` actualmente solo actualiza el DataFrame en memoria. Para persistir cambios, se debería descomentar y probar la línea `self.exercises_data.to_csv(self.csv_file_path, index=False)`.
*   **Seguridad:** Consideraciones de seguridad si la aplicación se expone públicamente (ej. validación de entradas para prevenir XSS si se muestran datos directamente, aunque Flask y Jinja2 ofrecen protecciones).
*   **Estilos y UX:** Las plantillas HTML son básicas. Se podrían mejorar significativamente los estilos (CSS) y la experiencia de usuario (UX).
*   **Pruebas Unitarias y de Integración:** Para un proyecto más grande, sería crucial añadir pruebas automatizadas.
*   **Despliegue:** Consideraciones para desplegar la aplicación en un servidor de producción (ej. usando Gunicorn/Waitress, configuración de un servidor web como Nginx).
*   **Comentarios en el Código:** Revisar y añadir más comentarios donde la lógica sea compleja.

He revisado el código y la estructura generada. Parece coherente con los requisitos del `prompt.md`.

Con esto, he completado todos los pasos del plan de desarrollo. La aplicación base está estructurada y debería ser funcional. ¿Hay alguna parte específica que quieras revisar o alguna modificación que te gustaría hacer?

```plaintext
Flask
pandas
```

---

**User**

Me ha dado este error, analizalo y arreglalo

---

**Cursor**

¡Entendido! El error que estás viendo es un `ImportError` debido a una dependencia circular.

Esto sucede porque:
1.  `main.py` intenta importar `FrontendController` desde `frontend.py`.
2.  `frontend.py` importa varias clases desde `backend.py`.
3.  `backend.py` importa la clase `Config` desde `main.py`.

Este ciclo (`main.py` -> `frontend.py` -> `backend.py` -> `main.py`) impide que Python cargue los módulos correctamente.

La solución más común y limpia es mover la clase `Config` a su propio archivo, por ejemplo, `config.py`. De esta manera, tanto `main.py` como `backend.py` (y `frontend.py` si fuera necesario) pueden importar `Config` desde `config.py` sin crear un ciclo.

Voy a realizar los siguientes pasos:

1.  **Crear `config.py`** y mover la clase `Config` allí.
2.  **Actualizar `main.py`** para importar `Config` desde `config.py`.
3.  **Actualizar `backend.py`** para importar `Config` desde `config.py`.
4.  **Actualizar `frontend.py`** para importar `Config` desde `config.py`.

Empecemos creando `config.py` y moviendo la clase `Config`.


```python
class Config:
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    CSV_FILE_PATH = 'exercises.csv'
    DEBUG_MODE = True

```

Ahora, modificaré `main.py` para eliminar la clase `Config` y la importaré desde `config.py`.


```python
import socket
from flask import Flask
from frontend import FrontendController # Importar el controlador del frontend
from backend import DatabaseManager # Importar el gestor de la base de datos
from config import Config # Importar Config desde config.py

// ... existing code ...
class FlaskApp:
// ... existing code ...
```

A continuación, actualizaré `backend.py` para que importe `Config` desde `config.py`.


```python
import pandas as pd
from config import Config # Para acceder a CSV_FILE_PATH
from typing import List, Dict, Any
// ... existing code ...
```

Finalmente, actualizaré `frontend.py` para que importe `Config` desde `config.py`.


```python
// ... existing code ...
# Importaciones del backend
from backend import UserData, IMCCalculator, WorkoutGenerator, DatabaseManager
from config import Config # Si es necesario para alguna configuración específica del frontend

class FrontendController:
// ... existing code ...
```

Con estos cambios, la dependencia circular debería estar resuelta. La clase `Config` ahora está en un módulo separado `config.py`, y los otros módulos (`main.py`, `backend.py`, `frontend.py`) la importan desde allí.

Puedes intentar ejecutar `main.py` de nuevo.

---

**User**

A partir del "training goal" que se determina en base al IMC de una persona, generá un archivo .csv por cada tipo de objetivo (por ejemplo: pérdida de peso, ganancia muscular, mantenimiento, etc.).
Cada archivo debe contener una rutina de ejercicios diferente, adaptada al objetivo correspondiente.
Luego, en el frontend, mostrá estos ejercicios de forma organizada según el objetivo.
@UNIR-Gen_Codigo_Aut 

---

**Cursor**

¡Excelente idea para ampliar la funcionalidad! Vamos a reestructurar un poco el backend y luego el frontend para lograr esto.

**Plan de Acción Detallado:**

1.  **Actualizar `backend.py`:**
    *   **`DatabaseManager`**:
        *   Añadir un método `save_exercises_to_csv(exercises: List[Exercise], filename: str, objective_name: str)` para guardar una lista de ejercicios (una rutina) en un archivo CSV. Incluirá el nombre del objetivo como una columna o en el nombre del archivo. Para simplificar, lo añadiré al nombre del archivo y las columnas serán las propiedades del ejercicio.
    *   **`WorkoutGenerator`**:
        *   Crear un nuevo método `generate_and_save_routines_for_all_goals(num_exercises_per_routine: int = 5)`.
            *   Este método identificará los principales objetivos de entrenamiento ("Ganancia de Masa Muscular", "Mantenimiento y Bienestar General", "Pérdida de Peso", "Pérdida de Peso Progresiva y Salud").
            *   Para cada objetivo, determinará la categoría de IMC asociada.
            *   Obtendrá ejercicios generales (sin especificar género o usando 'Any') para esa categoría de IMC.
            *   Creará una lista de ejercicios seleccionados.
            *   Guardará esta lista en un archivo CSV específico para ese objetivo (ej., `rutina_ganancia_muscular.csv`).
        *   Asegurarnos de que este método se llame, por ejemplo, al inicializar `FrontendController` para que los archivos se generen.
    *   **`IMCCalculator`**:
        *   Puede ser útil tener un método que devuelva un mapeo de objetivos a categorías de IMC, o simplemente una lista de todos los objetivos posibles y sus correspondientes categorías de IMC para iterar sobre ellos en `WorkoutGenerator`.

2.  **Actualizar `frontend.py`:**
    *   **`FrontendController`**:
        *   En `__init__`, llamar a `workout_generator.generate_and_save_routines_for_all_goals()` para que los CSVs se creen al iniciar la aplicación.
        *   Añadir una nueva ruta, por ejemplo, `/general_routines`.
        *   Crear un método `render_general_routines_page()` que:
            *   Identifique los archivos CSV de rutinas generados (basándose en los nombres de los objetivos).
            *   Lea cada CSV (usando pandas).
            *   Compile los datos de manera que se puedan pasar a la plantilla (por ejemplo, un diccionario donde las claves son los nombres de los objetivos y los valores son listas de ejercicios).
            *   Renderice una nueva plantilla HTML (`general_routines.html`) pasando estos datos.

3.  **Crear Plantillas HTML (en `templates`):**
    *   Crear `general_routines.html`.
        *   Esta plantilla recibirá el diccionario de rutinas.
        *   Iterará sobre los objetivos y mostrará cada rutina de forma organizada (por ejemplo, con un encabezado para cada objetivo y luego una lista/tabla de los ejercicios).

4.  **Actualizar `main.py`:**
    *   Añadir la nueva ruta a `FrontendController` si la forma de registrar rutas lo requiere (en nuestro caso, `add_url_rule` en `_register_routes` de `FrontendController` es suficiente).
    *   Asegurar que las instancias se pasen correctamente.

Vamos a empezar con las modificaciones en `backend.py`.

Primero, modificaré `IMCCalculator` para obtener fácilmente los objetivos y sus categorías.


```python
\
// ... existing code ...
    def determine_training_goal(self, imc: float) -> str:
        """Determina el objetivo del entrenamiento según el IMC."""
        category = self.get_imc_category(imc)
        if category == "Bajo Peso":
            return "Ganancia de Masa Muscular"
        elif category == "Normal":
            return "Mantenimiento y Bienestar General"
        elif category == "Sobrepeso":
            return "Pérdida de Peso"
        else:  # Obesidad
            return "Pérdida de Peso Progresiva y Salud"

    def get_all_training_goals_with_imc_categories(self) -> Dict[str, str]:
        """Devuelve un diccionario de todos los objetivos de entrenamiento y sus categorías de IMC asociadas."""
        # Estas categorías deben coincidir con las usadas en get_imc_category y los datos del CSV
        return {
            "Ganancia de Masa Muscular": "Bajo Peso",
            "Mantenimiento y Bienestar General": "Normal",
            "Pérdida de Peso": "Sobrepeso",
            "Pérdida de Peso Progresiva y Salud": "Obesidad" 
            # Nota: El objetivo "Pérdida de Peso" se asigna a "Sobrepeso".
            # El objetivo "Pérdida de Peso Progresiva y Salud" se asigna a "Obesidad".
            # Esto es consistente con determine_training_goal.
        }

class Exercise:
// ... existing code ...

```

Ahora, añadiré el método `save_exercises_to_csv` a `DatabaseManager`.


```python
// ... existing code ...
        # self.exercises_data.to_csv(self.csv_file_path, index=False)
        print(f"Ejercicio '{new_exercise.name}' añadido a la base de datos en memoria.")

    def save_exercises_to_csv(self, exercises: List[Exercise], filename: str):
        """Guarda una lista de objetos Exercise en un archivo CSV."""
        if not exercises:
            print(f"No hay ejercicios para guardar en {filename}")
            # Opcionalmente, crear un archivo vacío o con cabeceras
            # df = pd.DataFrame(columns=['id', 'name', 'description', 'imc_range', 'difficulty', 'category', 'gender_specific', 'equipment_needed'])
            # df.to_csv(filename, index=False)
            return

        exercises_dict_list = [ex.to_dict() for ex in exercises]
        df = pd.DataFrame(exercises_dict_list)
        
        # Asegurar el orden de las columnas y manejar equipment_needed como string
        df['equipment_needed'] = df['equipment_needed'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
        
        # Columnas deseadas en el CSV, igual que el original exercises.csv
        output_columns = ['id', 'name', 'description', 'imc_range', 'difficulty', 'category', 'gender_specific', 'equipment_needed']
        df = df[output_columns] # Reordenar y seleccionar columnas

        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Rutina guardada exitosamente en {filename}")
        except Exception as e:
            print(f"Error al guardar la rutina en {filename}: {e}")

class WorkoutPlan:
// ... existing code ...

```

Ahora, el método principal en `WorkoutGenerator` para crear y guardar estas rutinas.


```python
// ... existing code ...
    # Si se necesita una lógica más explícita o granular, se pueden descomponer.

    def _sanitize_filename(self, name: str) -> str:
        """Limpia un string para que sea un nombre de archivo válido."""
        name = name.lower()
        name = name.replace(" y ", "_")
        name = name.replace(" ", "_")
        name = name.replace("(", "")
        name = name.replace(")", "")
        name = name.replace(",", "")
        # Eliminar otros caracteres no deseados si es necesario
        import re
        name = re.sub(r'[^a-z0-9_\\]', '', name)
        return name

    def generate_and_save_routines_for_all_goals(self, num_exercises_per_routine: int = 5):
        """Genera y guarda en CSV rutinas para todos los objetivos de entrenamiento principales."""
        print("Generando rutinas generales por objetivo...")
        all_goals_map = self.imc_calculator.get_all_training_goals_with_imc_categories()

        for goal_name, imc_category in all_goals_map.items():
            print(f"Generando rutina para el objetivo: {goal_name} (Categoría IMC: {imc_category})")
            
            # Obtener ejercicios generales para la categoría de IMC
            # Usamos gender='Any' para obtener ejercicios no específicos de género para estas rutinas generales
            available_exercises = self.db_manager.get_exercises_by_criteria(
                imc_category=imc_category,
                gender='Any' 
            )

            if not available_exercises:
                print(f"No se encontraron ejercicios disponibles para el objetivo '{goal_name}'.")
                continue

            # Selección de ejercicios (similar a generate_routine)
            if len(available_exercises) > num_exercises_per_routine:
                selected_exercises = random.sample(available_exercises, num_exercises_per_routine)
            else:
                selected_exercises = available_exercises
            
            if selected_exercises:
                sanitized_goal_name = self._sanitize_filename(goal_name)
                filename = f"rutina_{sanitized_goal_name}.csv"
                # Guardar la lista de Exercise directamente
                self.db_manager.save_exercises_to_csv(selected_exercises, filename)
            else:
                print(f"No se seleccionaron ejercicios para el objetivo '{goal_name}'.")
        print("Finalizada la generación de rutinas generales.")

# Comentario residual que no pude eliminar antes, intentando nuevamente.
# Las clases WorkoutPlan y WorkoutGenerator se añadirán después. 

```

Parece que el comentario `# Las clases WorkoutPlan y WorkoutGenerator se añadirán después.` al final de `backend.py` persiste. Voy a intentar eliminarlo de forma más directa, especificando las líneas exactas.
Primero, leeré el final del archivo para confirmar su ubicación.


El comentario residual parece estar en la línea 343. Procederé a eliminarlo.


```python
        print("Finalizada la generación de rutinas generales.")

```

Sigue sin eliminarse. Parece que la herramienta `edit_file` o el modelo que la aplica tiene dificultades con este caso específico, o la información de las líneas no es del todo precisa entre lecturas y ediciones. Por ahora, y dado que es solo un comentario, lo ignoraré para no atascar el proceso. Si causa problemas reales más adelante (lo cual es improbable para un comentario), lo abordaremos.

Continuemos con el plan. Ya hemos modificado `backend.py`.

Ahora, **actualizar `frontend.py`**:
Llamaremos a `generate_and_save_routines_for_all_goals()` en el `__init__` de `FrontendController` y añadiremos la nueva ruta y el método para mostrar estas rutinas.


```python
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
        # Generar los CSV de rutinas generales al iniciar
        print("Iniciando generación de rutinas generales desde FrontendController...")
        self.workout_generator.generate_and_save_routines_for_all_goals()
        print("Rutinas generales generadas.")

    def _register_routes(self):
        self.app.add_url_rule('/', 'render_home_page', self.render_home_page, methods=['GET'])
        self.app.add_url_rule('/calculator', 'render_calculator_form', self.render_calculator_form, methods=['GET'])
        self.app.add_url_rule('/calculate', 'handle_form_submission', self.handle_form_submission, methods=['POST'])
        self.app.add_url_rule('/general_routines', 'render_general_routines_page', self.render_general_routines_page, methods=['GET'])
        # La ruta 'render_workout_results' se llamará implícitamente o por redirección
        # desde handle_form_submission, pasando los datos necesarios.

// ... existing code ...
    def display_error_message(self, message: str):
        """Muestra un mensaje de error."""
        # Podríamos tener una plantilla específica para errores o pasar el mensaje a una plantilla existente.
        return render_template('error.html', error_message=message)

    def render_general_routines_page(self):
        """Renderiza la página que muestra las rutinas generales por objetivo desde los CSVs."""
        routines_data = {}
        # Nombres de objetivos como se usan para generar los archivos CSV (después de sanitizar)
        # Esto debería coincidir con la lógica de _sanitize_filename en WorkoutGenerator
        goal_to_filename_map = {
            "Ganancia de Masa Muscular": "rutina_ganancia_de_masa_muscular.csv",
            "Mantenimiento y Bienestar General": "rutina_mantenimiento_bienestar_general.csv",
            "Pérdida de Peso": "rutina_prdida_de_peso.csv", # Corregir si el sanitizado produce otro nombre
            "Pérdida de Peso Progresiva y Salud": "rutina_prdida_de_peso_progresiva_salud.csv" # Corregir si el sanitizado produce otro nombre
        }
        
        # Para una mayor robustez, obtenemos los nombres de archivo reales después de la sanitización
        # desde IMCCalculator y WorkoutGenerator._sanitize_filename
        temp_imc_calc = IMCCalculator()
        temp_workout_gen = WorkoutGenerator(self.db_manager) # Necesita db_manager aunque no lo use para _sanitize_filename

        all_goals_map = temp_imc_calc.get_all_training_goals_with_imc_categories()
        actual_goal_filenames = {}
        for goal_name in all_goals_map.keys():
            sanitized_name = temp_workout_gen._sanitize_filename(goal_name)
            actual_goal_filenames[goal_name] = f"rutina_{sanitized_name}.csv"

        for goal_name, csv_filename in actual_goal_filenames.items():
            try:
                if os.path.exists(csv_filename):
                    df = pd.read_csv(csv_filename)
                    # Convertir 'equipment_needed' de string de nuevo a lista para la plantilla si es necesario
                    if 'equipment_needed' in df.columns:
                         df['equipment_needed'] = df['equipment_needed'].apply(
                            lambda x: [item.strip() for item in str(x).split(',')] if pd.notna(x) and str(x).strip() != '' else []
                        )
                    routines_data[goal_name] = df.to_dict(orient='records')
                else:
                    print(f"Archivo de rutina no encontrado: {csv_filename}")
                    routines_data[goal_name] = [] # Dejarlo vacío si no se encuentra
            except Exception as e:
                print(f"Error al leer el archivo CSV '{csv_filename}': {e}")
                routines_data[goal_name] = [] # Dejarlo vacío en caso de error
        
        return render_template('general_routines.html', routines_data=routines_data)

# La instanciación de FrontendController y su enlace con la app Flask
# se realizará en main.py

```

Ahora, creo la nueva plantilla HTML `templates/general_routines.html`.


```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rutinas Generales por Objetivo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        .container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 900px; margin: auto; }
        h1 { text-align: center; color: #333; margin-bottom: 30px;}
        h2 { color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 5px; margin-top: 30px;}
        .routine-section { margin-bottom: 30px; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #e9ecef;
            color: #495057;
        }
        tr:nth-child(even) { background-color: #f8f9fa; }
        .no-exercises { color: #777; font-style: italic; }
        a.nav-link { display: inline-block; margin: 20px 0; color: #007bff; text-decoration: none; font-size: 16px; }
        a.nav-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Rutinas Generales por Objetivo de Entrenamiento</h1>
        
        <a href="{{ url_for('render_home_page') }}" class="nav-link">Volver al Inicio</a>
        <a href="{{ url_for('render_calculator_form') }}" class="nav-link" style="margin-left: 15px;">Calcular Rutina Personalizada</a>

        {% if routines_data %}
            {% for goal, exercises in routines_data.items() %}
            <div class="routine-section">
                <h2>{{ goal }}</h2>
                {% if exercises %}
                    <table>
                        <thead>
                            <tr>
                                <th>Nombre del Ejercicio</th>
                                <th>Descripción</th>
                                <th>Categoría</th>
                                <th>Dificultad</th>
                                <th>Equipo Necesario</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for ex in exercises %}
                            <tr>
                                <td>{{ ex.name }}</td>
                                <td>{{ ex.description }}</td>
                                <td>{{ ex.category }}</td>
                                <td>{{ ex.difficulty }}</td>
                                <td>
                                    {% if ex.equipment_needed %}
                                        {{ ex.equipment_needed | join(', ') }}
                                    {% else %}
                                        Ninguno
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                {% else %}
                    <p class="no-exercises">No hay ejercicios definidos para este objetivo en este momento.</p>
                {% endif %}
            </div>
            {% endfor %}
        {% else %}
            <p class="no-exercises">No se encontraron rutinas generales. Es posible que aún no se hayan generado.</p>
        {% endif %}

    </div>
</body>
</html>

```

Finalmente, añadiré un enlace a la nueva página de rutinas generales en `templates/home.html` para que sea accesible.


```html
// ... existing code ...
    <div class="container">
        <h1>Bienvenido al Generador de Rutinas de Ejercicio</h1>
        <p>Obtén una rutina de ejercicios personalizada basada en tu Índice de Masa Corporal (IMC).</p>
        <p><a href="{{ url_for('render_calculator_form') }}">Calcular mi Rutina Personalizada</a></p>
        <p><a href="{{ url_for('render_general_routines_page') }}">Ver Rutinas Generales por Objetivo</a></p>
    </div>
</body>
// ... existing code ...

```

Con estos cambios, la aplicación debería ahora:

1.  Al iniciarse, generar archivos CSV (por ejemplo, `rutina_ganancia_de_masa_muscular.csv`, `rutina_prdida_de_peso.csv`, etc.) cada uno con una selección de ejercicios para el objetivo de entrenamiento correspondiente. Estos archivos se guardarán en el directorio raíz del proyecto.
2.  Ofrecer una nueva página (accesible desde la página de inicio) donde se muestran estas rutinas generales, leídas desde los archivos CSV y organizadas por objetivo.

Te sugiero probar la aplicación. Ejecuta `python main.py` y navega primero a la página de inicio. Deberías ver el nuevo enlace. Al hacer clic en él, se deberían mostrar las rutinas. Verifica también que los archivos CSV se hayan creado en el directorio de tu proyecto.

Ten en cuenta que la función `_sanitize_filename` en `backend.py` intenta limpiar los nombres de los objetivos para usarlos como nombres de archivo. La lógica en `frontend.py` para encontrar estos archivos intenta replicar esta sanitización. Si los nombres de archivo generados no coinciden exactamente con lo que `frontend.py` espera, los archivos no se encontrarán. Los `print` que añadí deberían ayudar a depurar esto si ocurre. Específicamente, he ajustado `frontend.py` para que utilice la misma lógica de sanitización para encontrar los nombres de archivo, lo que debería hacerlo más robusto.

---

**User**

Genera los csv necesarios para estos cambios como comentaste, todos los necesarios con las filas necesarias

---

**Cursor**

Entendido. Voy a generar el contenido para los archivos CSV que se crearían al ejecutar la lógica que hemos implementado.

Basándome en el `exercises.csv` original y la lógica de `WorkoutGenerator`:

1.  **Para "Ganancia de Masa Muscular" (IMC "Bajo Peso", gender "Any"):**
    *   Ejercicios de `exercises.csv` que coinciden:
        *   5,Elevaciones Laterales de Hombros,Ejercicio para deltoides,Bajo Peso,Principiante,Fuerza,Any,Mancuernas Pequeñas
        *   6,Curl de Bíceps con Mancuernas,Ejercicio para bíceps,Bajo Peso,Principiante,Fuerza,Any,Mancuernas
        *   10,Remo con Mancuerna,Ejercicio de espalda y bíceps,Bajo Peso,Intermedio,Fuerza,Any,Mancuerna,Banco (opcional)
        *   11,Prensa de Hombros con Mancuernas,Ejercicio de hombros,Bajo Peso,Intermedio,Fuerza,Any,Mancuernas
        *   16,Sentadilla Sumo,Variación de sentadilla para aductores y glúteos,Bajo Peso,Intermedio,Fuerza,Any,Pesa Rusa (opcional)
    *   Seleccionaremos estos 5 (o un subconjunto aleatorio si hubiera más de 5).

2.  **Para "Mantenimiento y Bienestar General" (IMC "Normal", gender "Any"):**
    *   Ejercicios de `exercises.csv` que coinciden:
        *   1,Flexiones de Pecho,Ejercicio de fuerza para el tren superior,Normal,Principiante,Fuerza,Any,
        *   2,Sentadillas,Ejercicio de fuerza para piernas y glúteos,Normal,Principiante,Fuerza,Any,
        *   3,Plancha Abdominal,Ejercicio isométrico para el core,Normal,Intermedio,Fuerza,Any,
        *   8,Zancadas (Lunges),Ejercicio para piernas y glúteos,Normal,Intermedio,Fuerza,Any,
        *   9,Burpees,Ejercicio compuesto de cuerpo completo,Normal,Avanzado,Cardio,Any,
        *   14,Estiramiento de Isquiotibiales,Estiramiento para la parte posterior de las piernas,Normal,Principiante,Flexibilidad,Any,
        *   15,Estiramiento de Cuádriceps,Estiramiento para la parte frontal de los muslos,Normal,Principiante,Flexibilidad,Any,
        *   19,Yoga para principiantes,Mejora flexibilidad y fuerza,Normal,Principiante,Flexibilidad,Any,Mat de yoga
        *   20,Pilates Mat,Fortalecimiento del core y flexibilidad,Normal,Intermedio,Fuerza,Any,Mat
    *   Seleccionaremos 5 aleatorios de esta lista.

3.  **Para "Pérdida de Peso" (IMC "Sobrepeso", gender "Any"):**
    *   Ejercicios de `exercises.csv` que coinciden:
        *   4,Correr Suave (Trote),Ejercicio cardiovascular de bajo impacto,Sobrepeso,Principiante,Cardio,Any,
        *   12,Saltos de Tijera (Jumping Jacks),Calentamiento cardiovascular,Sobrepeso,Principiante,Cardio,Any,
        *   17,Caminata Inclinada,Cardio con mayor intensidad para piernas,Sobrepeso,Intermedio,Cardio,Any,Cinta de correr
    *   Seleccionaremos estos 3 (ya que son menos de 5).

4.  **Para "Pérdida de Peso Progresiva y Salud" (IMC "Obesidad", gender "Any"):**
    *   Ejercicios de `exercises.csv` que coinciden:
        *   7,Caminata Rápida,Ejercicio cardiovascular moderado,Obesidad,Principiante,Cardio,Any,
        *   13,Bicicleta Estática,Ejercicio cardiovascular de bajo impacto,Obesidad,Principiante,Cardio,Any,Bicicleta Estática
        *   18,Natación,Ejercicio de cuerpo completo de bajo impacto,Obesidad,Intermedio,Cardio,Any,Piscina
    *   Seleccionaremos estos 3.

Ahora, crearé los archivos con una selección de estos ejercicios. La selección real sería aleatoria si hay más de 5 opciones, pero para este ejemplo, elegiré los primeros que encuentre o todos si son menos de 5.

**1. `rutina_ganancia_de_masa_muscular.csv`**
(Nombre sanitizado de "Ganancia de Masa Muscular")


```csv
id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed
5,Elevaciones Laterales de Hombros,Ejercicio para deltoides,Bajo Peso,Principiante,Fuerza,Any,"Mancuernas Pequeñas"
6,Curl de Bíceps con Mancuernas,Ejercicio para bíceps,Bajo Peso,Principiante,Fuerza,Any,Mancuernas
10,Remo con Mancuerna,"Ejercicio de espalda y bíceps",Bajo Peso,Intermedio,Fuerza,Any,"Mancuerna, Banco (opcional)"
11,Prensa de Hombros con Mancuernas,Ejercicio de hombros,Bajo Peso,Intermedio,Fuerza,Any,Mancuernas
16,Sentadilla Sumo,"Variación de sentadilla para aductores y glúteos",Bajo Peso,Intermedio,Fuerza,Any,"Pesa Rusa (opcional)"

```

**2. `rutina_mantenimiento_bienestar_general.csv`**
(Nombre sanitizado de "Mantenimiento y Bienestar General")
Para este, elegiré 5 de los disponibles:


```csv
id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed
1,Flexiones de Pecho,Ejercicio de fuerza para el tren superior,Normal,Principiante,Fuerza,Any,
2,Sentadillas,Ejercicio de fuerza para piernas y glúteos,Normal,Principiante,Fuerza,Any,
3,Plancha Abdominal,Ejercicio isométrico para el core,Normal,Intermedio,Fuerza,Any,
8,Zancadas (Lunges),Ejercicio para piernas y glúteos,Normal,Intermedio,Fuerza,Any,
14,Estiramiento de Isquiotibiales,Estiramiento para la parte posterior de las piernas,Normal,Principiante,Flexibilidad,Any,

```

**3. `rutina_prdida_de_peso.csv`**
(Nombre sanitizado de "Pérdida de Peso". La función `_sanitize_filename` convierte "Pérdida de Peso" a "prdida_de_peso").


```csv
id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed
4,Correr Suave (Trote),Ejercicio cardiovascular de bajo impacto,Sobrepeso,Principiante,Cardio,Any,
12,Saltos de Tijera (Jumping Jacks),Calentamiento cardiovascular,Sobrepeso,Principiante,Cardio,Any,
17,Caminata Inclinada,Cardio con mayor intensidad para piernas,Sobrepeso,Intermedio,Cardio,Any,"Cinta de correr"

```

Hubo un problema al crear `rutina_prdida_de_peso.csv`, parece que se creó vacío. Lo intentaré de nuevo.


```csv
id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed
4,Correr Suave (Trote),Ejercicio cardiovascular de bajo impacto,Sobrepeso,Principiante,Cardio,Any,
12,Saltos de Tijera (Jumping Jacks),Calentamiento cardiovascular,Sobrepeso,Principiante,Cardio,Any,
17,Caminata Inclinada,Cardio con mayor intensidad para piernas,Sobrepeso,Intermedio,Cardio,Any,"Cinta de correr"

```

**4. `rutina_prdida_de_peso_progresiva_salud.csv`**
(Nombre sanitizado de "Pérdida de Peso Progresiva y Salud").


```csv
id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed
7,Caminata Rápida,Ejercicio cardiovascular moderado,Obesidad,Principiante,Cardio,Any,
13,Bicicleta Estática,Ejercicio cardiovascular de bajo impacto,Obesidad,Principiante,Cardio,Any,"Bicicleta Estática"
18,Natación,Ejercicio de cuerpo completo de bajo impacto,Obesidad,Intermedio,Cardio,Any,Piscina

```

He creado los cuatro archivos CSV con ejemplos de rutinas basadas en los objetivos. Estos archivos se guardarán en el directorio raíz de tu proyecto (donde están `main.py`, `backend.py`, etc.).

Cuando ejecutes la aplicación (`python main.py`), la lógica en `FrontendController` intentará leer estos archivos CSV para mostrar las rutinas en la página `/general_routines`. Si los nombres de archivo que he usado (que se basan en la función `_sanitize_filename` que implementamos) coinciden con los que `FrontendController` espera, todo debería funcionar correctamente.

Puedes verificar que estos archivos se hayan creado en tu directorio `/c:/Users/jorge/Desktop/UNIR-Gen_Codigo_Aut/`.

---

**User**

Con estos cambios al intentar realizar la rutina personalizada siguiente, no devuelve rutina, arregla lo necesario:
Resultados de tu Rutina Personalizada
Tus Datos:
Sexo: male

Altura: 175.0 cm

Peso: 150.0 kg

Edad: 20 años

Resultados del IMC:
Tu IMC es: 48.98

Categoría de IMC: Obesidad

Objetivo de Entrenamiento Sugerido: Pérdida de Peso Progresiva y Salud

Tu Plan de Entrenamiento:
No se encontraron ejercicios para este plan.

@UNIR-Gen_Codigo_Aut 

---

**Cursor**

Entendido. El problema que describes ("No se encontraron ejercicios para este plan") cuando intentas generar una rutina personalizada para un IMC de "Obesidad" (48.98 en tu ejemplo) sugiere que la lógica de `WorkoutGenerator.generate_routine` podría no estar encontrando ejercicios adecuados para ese caso específico, o la forma en que se filtran los ejercicios no es la esperada.

Vamos a revisar la lógica en `WorkoutGenerator.generate_routine` y `DatabaseManager.get_exercises_by_criteria` para asegurarnos de que manejan correctamente este escenario.

**Posibles Causas y Plan de Revisión:**

1.  **Coincidencia de `imc_category` en `get_exercises_by_criteria`**:
    *   En `WorkoutGenerator`, `imc_category` se determina como "Obesidad".
    *   En `DatabaseManager.get_exercises_by_criteria`, se filtra así: `filtered_df = self.exercises_data[self.exercises_data['imc_range'].str.lower() == imc_category.lower()]`.
    *   Debemos asegurar que en `exercises.csv` haya ejercicios con `imc_range` igual a "Obesidad" (insensible a mayúsculas/minúsculas). Ya hemos confirmado que sí los hay (ej. ID 7, 13, 18).

2.  **Filtrado por Género**:
    *   El usuario ingresó "male".
    *   `get_exercises_by_criteria` filtra por género:
        ```python
        if gender.lower() != 'any':
            filtered_df = filtered_df[
                (filtered_df['gender_specific'].str.lower() == gender.lower()) |
                (filtered_df['gender_specific'].str.lower() == 'any')
            ]
        ```
    *   Los ejercicios para "Obesidad" en `exercises.csv` (7, 13, 18) tienen `gender_specific` como "Any". Esto debería permitir que se seleccionen para "male".

3.  **Selección de Ejercicios en `generate_routine`**:
    *   Si `available_exercises` no está vacía, la lógica es:
        ```python
        if len(available_exercises) > num_exercises:
            selected_exercises = random.sample(available_exercises, num_exercises)
        else:
            selected_exercises = available_exercises
        ```
    *   Si se encuentran 3 ejercicios ("Caminata Rápida", "Bicicleta Estática", "Natación") y `num_exercises` es el predeterminado (5), entonces `selected_exercises` debería ser igual a `available_exercises` (los 3 ejercicios).

4.  **Paso de `UserData`**:
    *   Asegurarse de que el objeto `user_data` que llega a `generate_routine` tiene los valores correctos (`gender='male'`, `height`, `weight`, `age`). Por lo que muestras en la salida, esto parece correcto.

**Sospecha Principal:**
La causa más probable es cómo se está interpretando `gender` o `imc_category` en algún punto del filtrado, o si hay algún detalle sutil en los datos del CSV que no coincide exactamente.

Revisemos el código de `backend.py` en las partes relevantes.

**Paso 1: Revisar `DatabaseManager.get_exercises_by_criteria`**
La lógica de filtrado parece correcta. El `str.lower()` debería manejar las diferencias de mayúsculas/minúsculas.
Los ejercicios 7, 13 y 18 tienen `imc_range` como "Obesidad" y `gender_specific` como "Any". Con `imc_category = "Obesidad"` y `gender = "male"`, el filtro debería funcionar.

**Paso 2: Revisar `WorkoutGenerator.generate_routine`**
El `user_data` se pasa y se utiliza para obtener `imc_category` y `gender`.
```python
available_exercises = self.db_manager.get_exercises_by_criteria(
    imc_category=imc_category,
    gender=user_data.gender
)

if not available_exercises:
    # Aquí es donde se estaría devolviendo el WorkoutPlan vacío
    return WorkoutPlan(exercises=[], goal=training_goal, difficulty_level="Variable")
```
Si `available_exercises` queda vacío después de llamar a `get_exercises_by_criteria`, entonces el problema reside en esa función o en los datos que recibe.

Voy a añadir algunos `print` temporales en `DatabaseManager.get_exercises_by_criteria` para ver qué está pasando con los filtros y los datos. Esto nos ayudará a diagnosticar.



```python
        if gender.lower() != 'any':
            filtered_df = filtered_df[
                (filtered_df['gender_specific'].str.lower() == gender.lower()) |
                (filtered_df['gender_specific'].str.lower() == 'any')
            ]
```

```python
        if len(available_exercises) > num_exercises:
            selected_exercises = random.sample(available_exercises, num_exercises)
        else:
            selected_exercises = available_exercises
```

```python
available_exercises = self.db_manager.get_exercises_by_criteria(
    imc_category=imc_category,
    gender=user_data.gender
)

if not available_exercises:
    # Aquí es donde se estaría devolviendo el WorkoutPlan vacío
    return WorkoutPlan(exercises=[], goal=training_goal, difficulty_level="Variable")
```

```python
// ... existing code ...
    def get_exercises_by_criteria(self, imc_category: str, gender: str = 'Any') -> List[Exercise]:
        """Filtra los ejercicios según la categoría de IMC y el género."""
        print(f"[DB DEBUG] get_exercises_by_criteria: imc_category='{imc_category}', gender='{gender}'")
        if self.exercises_data is None or self.exercises_data.empty:
            print("[DB DEBUG] exercises_data es None o vacío.")
            return []

        # Filtrar por categoría de IMC
        print(f"[DB DEBUG] Filtrando por imc_category: '{imc_category.lower()}'")
        # print("[DB DEBUG] Valores únicos en CSV para imc_range (lower):", self.exercises_data['imc_range'].str.lower().unique())
        filtered_df_imc = self.exercises_data[self.exercises_data['imc_range'].str.lower() == imc_category.lower()]
        print(f"[DB DEBUG] DataFrame después de filtrar por IMC (len: {len(filtered_df_imc)}):")
        # print(filtered_df_imc.head())

        if filtered_df_imc.empty:
            print("[DB DEBUG] Ningún ejercicio encontrado para la categoría de IMC dada.")
            return []

        # Filtrar por género (si no es 'Any')
        # Considera ejercicios 'Any' o específicos para el género dado.
        current_filtered_df = filtered_df_imc
        if gender.lower() != 'any':
            print(f"[DB DEBUG] Filtrando por gender: '{gender.lower()}'")
            # print("[DB DEBUG] Valores únicos en CSV para gender_specific (lower):", current_filtered_df['gender_specific'].str.lower().unique())
            final_filtered_df = current_filtered_df[
                (current_filtered_df['gender_specific'].str.lower() == gender.lower()) |
                (current_filtered_df['gender_specific'].str.lower() == 'any')
            ]
            print(f"[DB DEBUG] DataFrame después de filtrar por GÉNERO (len: {len(final_filtered_df)}):")
            # print(final_filtered_df.head())
        else:
            final_filtered_df = current_filtered_df
            print("[DB DEBUG] No se aplica filtro de género (gender es 'Any').")
            print(f"[DB DEBUG] DataFrame sin filtro de GÉNERO (len: {len(final_filtered_df)}):")
        
        if final_filtered_df.empty:
            print("[DB DEBUG] Ningún ejercicio encontrado después del filtro de género.")
            return []
            
        exercises_list = []
        for _, row in final_filtered_df.iterrows():
// ... existing code ...

```

Con estos mensajes de depuración en `backend.py`, cuando ejecutes la aplicación e intentes obtener una rutina personalizada para el caso que falló (IMC "Obesidad", género "male"), deberías ver en la consola del servidor Flask los resultados de cada paso del filtrado dentro de `get_exercises_by_criteria`.

Por favor, ejecuta la aplicación con estos cambios y reproduce el error. Luego, comparte la salida de la consola. Esto nos dirá exactamente dónde se está interrumpiendo el proceso de filtrado (si después del filtro de IMC o después del filtro de género) y cuántos ejercicios se encuentran en cada etapa.

Si la salida muestra:
*   `[DB DEBUG] DataFrame después de filtrar por IMC (len: 3)` (o un número mayor que 0)
*   Y luego `[DB DEBUG] DataFrame después de filtrar por GÉNERO (len: 0)`

Entonces el problema está en el filtro de género o en los datos de `gender_specific` en el CSV para esos ejercicios de "Obesidad".

Si ya la primera etapa de filtro por IMC devuelve 0, entonces el `imc_category` "obesidad" no está coincidiendo con ninguna fila del CSV por alguna razón (quizás un espacio extra, un carácter oculto, o una diferencia de escritura que `lower()` no captura, aunque es improbable).

Una vez que tengamos esa información de depuración, podremos aplicar la corrección precisa.

---

**User**

Aqui tienes los logs de la consola, analizalos, por lo que vemos estás intentando utilizar un csv que no existe, deberás implementar los nuevos que hicimos:


---

**Cursor**

¡Tienes toda la razón! He analizado los logs y el problema es claro:

En múltiples puntos, tanto durante la generación de rutinas generales (`generate_and_save_routines_for_all_goals`) como durante la generación de la rutina personalizada (`generate_routine` a través de `/calculate`), el log muestra:

`[DB DEBUG] exercises_data es None o vac�o.`

Esto indica que `self.exercises_data` dentro de la instancia de `DatabaseManager` está vacío o no se ha cargado correctamente.

La línea `self.load_exercises()` se llama en el `__init__` de `DatabaseManager`:
```python
class DatabaseManager:
    def __init__(self, csv_file_path: str = Config.CSV_FILE_PATH):
        self.csv_file_path = csv_file_path # Debería ser 'exercises.csv'
        self.exercises_data = None
        self.load_exercises() # Aquí se carga
```
Y `load_exercises` intenta leer `self.csv_file_path`, que por defecto es `Config.CSV_FILE_PATH` ('exercises.csv').

El problema NO es que esté intentando usar los *nuevos* CSVs de rutinas (`rutina_ganancia_de_masa_muscular.csv`, etc.) para cargar la base de datos principal de ejercicios. Esos nuevos CSVs son para *guardar* rutinas, no para *cargar* el catálogo maestro de ejercicios.

El problema es que la carga inicial desde el archivo CSV maestro, `exercises.csv`, está fallando o resultando en un DataFrame vacío.

**Posibles causas para que `exercises.csv` no se cargue correctamente:**

1.  **Ruta del archivo incorrecta en `Config.CSV_FILE_PATH`**: Aunque parece ser solo `'exercises.csv'`, podría haber un problema si el directorio de trabajo actual de la aplicación no es donde se encuentra `exercises.csv`. Sin embargo, Flask suele ejecutarse desde la raíz del proyecto donde está `main.py`, y `exercises.csv` también está allí, por lo que esto es menos probable.
2.  **Error dentro de `load_exercises` que no se está propagando o que lleva a un `exercises_data` vacío**:
    ```python
    def load_exercises(self):
        """Carga los ejercicios desde el archivo CSV."""
        try:
            self.exercises_data = pd.read_csv(self.csv_file_path)
            # ... (procesamiento de equipment_needed)
        except FileNotFoundError:
            print(f"Error: El archivo CSV '{self.csv_file_path}' no fue encontrado.")
            self.exercises_data = pd.DataFrame(columns=[...]) # Se asigna un DF vacío
        except Exception as e:
            print(f"Error al cargar el archivo CSV: {e}")
            self.exercises_data = pd.DataFrame(columns=[...]) # Se asigna un DF vacío
    ```
    Si ocurre un `FileNotFoundError` o cualquier otra `Exception`, `self.exercises_data` se establece explícitamente como un DataFrame vacío, lo que coincide con el log `[DB DEBUG] exercises_data es None o vac�o.` (técnicamente no es `None` sino vacío después de estas excepciones).

**Revisión del Log:**

El log no muestra ningún mensaje de "Error: El archivo CSV 'exercises.csv' no fue encontrado." ni "Error al cargar el archivo CSV: ...". Esto es extraño. Significa que o bien:
a.  La lectura de `exercises.csv` ocurre sin excepciones, PERO el archivo `exercises.csv` está realmente vacío o solo tiene la cabecera (lo cual no es el caso según nuestros pasos anteriores).
b.  Hay algún problema con la instancia de `DatabaseManager` que se está utilizando, o cómo se comparten los datos.

Dado que los archivos CSV de rutinas específicas *sí* se están creando (lo cual indica que `WorkoutGenerator` y `DatabaseManager` pueden *escribir* archivos), el problema es más agudo en la lectura o el estado de `self.exercises_data` de `DatabaseManager`.

Vamos a añadir un `print` justo después de `pd.read_csv` en `load_exercises` para ver el estado del DataFrame inmediatamente después de la carga y antes de cualquier procesamiento.



```python
class DatabaseManager:
    def __init__(self, csv_file_path: str = Config.CSV_FILE_PATH):
        self.csv_file_path = csv_file_path # Debería ser 'exercises.csv'
        self.exercises_data = None
        self.load_exercises() # Aquí se carga
```

```python
    def load_exercises(self):
        """Carga los ejercicios desde el archivo CSV."""
        try:
            self.exercises_data = pd.read_csv(self.csv_file_path)
            # ... (procesamiento de equipment_needed)
        except FileNotFoundError:
            print(f"Error: El archivo CSV '{self.csv_file_path}' no fue encontrado.")
            self.exercises_data = pd.DataFrame(columns=[...]) # Se asigna un DF vacío
        except Exception as e:
            print(f"Error al cargar el archivo CSV: {e}")
            self.exercises_data = pd.DataFrame(columns=[...]) # Se asigna un DF vacío
```

```python
// ... existing code ...
    def load_exercises(self):
        """Carga los ejercicios desde el archivo CSV."""
        try:
            print(f"[DB LOAD DEBUG] Intentando cargar CSV desde: {os.path.abspath(self.csv_file_path)}")
            self.exercises_data = pd.read_csv(self.csv_file_path)
            print(f"[DB LOAD DEBUG] CSV '{self.csv_file_path}' cargado. Shape: {self.exercises_data.shape if self.exercises_data is not None else 'None'}. Vacío: {self.exercises_data.empty if self.exercises_data is not None else 'N/A'}")
            # Convertir la columna 'equipment_needed' de string a lista
// ... existing code ...
        except FileNotFoundError:
            print(f"[DB LOAD ERROR] FileNotFoundError: El archivo CSV '{self.csv_file_path}' (abs: {os.path.abspath(self.csv_file_path)}) no fue encontrado.")
            self.exercises_data = pd.DataFrame(columns=[
// ... existing code ...
        except Exception as e:
            print(f"[DB LOAD ERROR] Exception al cargar CSV '{self.csv_file_path}': {e}")
            self.exercises_data = pd.DataFrame(columns=[
// ... existing code ...

```

He añadido el import `os` que faltaba en la edición anterior de `backend.py`.
Por favor, ejecuta la aplicación de nuevo con estos cambios. La nueva información de depuración debería darnos una imagen más clara de lo que sucede durante la carga de `exercises.csv`.

Los mensajes clave a buscar ahora en la consola serán:
*   `[DB LOAD DEBUG] Intentando cargar CSV desde: ...` (para ver la ruta absoluta que intenta usar)
*   `[DB LOAD DEBUG] CSV 'exercises.csv' cargado. Shape: ... Vacío: ...`
*   O, si falla, `[DB LOAD ERROR] FileNotFoundError...` o `[DB LOAD ERROR] Exception al cargar CSV...`

Con esta información, deberíamos poder identificar la causa raíz.

---

**User**

Tienes que analizar los paths en el @config.py , ya que hay que utilizar los nuevos .csv que hemos creado, para asociar según los objetivos

---

**Cursor**

Entiendo tu razonamiento, pero creo que hay una pequeña confusión sobre cómo se utilizan los archivos CSV en el diseño actual, y quiero aclararlo para que podamos resolver el problema de raíz.

**Cómo Funciona Actualmente:**

1.  **`exercises.csv` (El Maestro):**
    *   Este archivo es la **base de datos principal y única** que contiene *todos* los ejercicios disponibles con sus detalles (ID, nombre, descripción, rango de IMC, dificultad, categoría, etc.).
    *   La clase `DatabaseManager` (en `backend.py`) tiene la tarea de **cargar todos los ejercicios desde ESTE ÚNICO archivo (`exercises.csv`)** en memoria cuando la aplicación se inicia. La variable `Config.CSV_FILE_PATH` en `config.py` correctamente apunta a `'exercises.csv'` para este propósito.

2.  **Los Nuevos CSVs de Rutinas (ej. `rutina_ganancia_de_masa_muscular.csv`):**
    *   Estos archivos **NO son fuentes de datos primarias** para `DatabaseManager`.
    *   Son **archivos de SALIDA generados** por `WorkoutGenerator`.
    *   Cuando `WorkoutGenerator.generate_and_save_routines_for_all_goals()` se ejecuta:
        *   Primero, consulta los ejercicios ya cargados en memoria por `DatabaseManager` (que vienen de `exercises.csv`).
        *   Luego, filtra estos ejercicios para cada objetivo de entrenamiento (pérdida de peso, ganancia muscular, etc.).
        *   Finalmente, **guarda** estas rutinas filtradas en los nuevos archivos CSV (como `rutina_ganancia_de_masa_muscular.csv`).
    *   Posteriormente, la página `/general_routines` en el frontend lee estos CSVs generados para mostrarlos.

**El Problema Real (Basado en los Logs Anteriores):**

Los logs que me proporcionaste anteriormente mostraron consistentemente:
`[DB DEBUG] exercises_data es None o vac�o.`

Esto significa que `DatabaseManager` **no está logrando cargar los datos correctamente desde el archivo maestro `exercises.csv`** en primer lugar. Si no hay datos en `DatabaseManager.exercises_data`, entonces:
*   La generación de rutinas personalizadas fallará (como viste).
*   La generación de los CSVs de rutinas generales (para cada objetivo) también fallará o producirá archivos vacíos porque no hay ejercicios base de donde seleccionar.

**Por Qué `config.py` Está Correcto (Por Ahora):**

`config.py` tiene `CSV_FILE_PATH = 'exercises.csv'`, lo cual es correcto porque es el archivo que `DatabaseManager` debe usar como su fuente principal de todos los ejercicios. No necesitamos cambiar `config.py` para que apunte a los múltiples CSVs de rutinas generadas para la carga inicial de datos.

**Qué Necesitamos Hacer:**

El paso crucial ahora es entender **por qué `DatabaseManager.load_exercises()` no está cargando `exercises.csv` correctamente.**

En mi mensaje anterior, modifiqué `backend.py` para añadir impresiones de depuración muy específicas dentro de la función `load_exercises` de `DatabaseManager`. Estas impresiones nos dirán:
1.  Si el archivo `exercises.csv` se encuentra en la ruta esperada.
2.  Si se lee correctamente o si ocurre algún error durante la lectura.
3.  Cuántas filas y columnas se cargan si la lectura es exitosa.

**Por favor, haz lo siguiente:**
1.  Asegúrate de que tienes la **última versión de `backend.py`** que te proporcioné (con los mensajes `[DB LOAD DEBUG]` y `[DB LOAD ERROR]`).
2.  **Ejecuta `python main.py` de nuevo.**
3.  Intenta acceder a la calculadora o a la página de rutinas personalizadas para que se active la lógica de carga y filtrado.
4.  **Comparte conmigo la salida COMPLETA de la consola del servidor Flask desde el momento en que inicias la aplicación.**

Esta nueva salida de la consola, con los mensajes de depuración detallados de `load_exercises`, es esencial para diagnosticar por qué tu base de datos principal de ejercicios (`exercises.csv`) no se está cargando en `DatabaseManager`. Una vez que `exercises.csv` se cargue correctamente, el resto de la lógica (generación de rutinas personalizadas y generales) debería funcionar como se espera.

---

**User**

Vale en base a tu respuesta no queremos esa lógica, queremos tener un conjunto de ejercicios para cada imc o finalidad segun los objetivos, de esos csv queremos que se le muestre al usuario los que se corresponden con su rutina personalizada con lo cual la logica inicial de exercises.csv queda modificada
Algo asi:
rutina_ganancia para imc bajo, rutina_mantenimiento para imc medio y rutina_perdida para imc alto, y tambien si ves bien añadir alguna extra, añadela e implementala

---

**Cursor**

¡Ah, entiendo perfectamente ahora! Quieres un cambio de enfoque más fundamental: en lugar de tener un `exercises.csv` maestro y generar rutinas a partir de él, quieres tener **archivos CSV predefinidos para cada tipo de rutina/objetivo**, y que la aplicación seleccione y muestre el contenido de uno de estos archivos CSV según el IMC del usuario.

Esto simplifica algunas partes y cambia la lógica de `DatabaseManager` y `WorkoutGenerator` significativamente.

**Nuevo Plan de Acción (Revisado):**

1.  **Archivos CSV de Rutinas Predefinidas:**
    *   Ya hemos creado:
        *   `rutina_ganancia_de_masa_muscular.csv` (para IMC Bajo Peso)
        *   `rutina_mantenimiento_bienestar_general.csv` (para IMC Normal)
        *   `rutina_prdida_de_peso.csv` (para IMC Sobrepeso)
        *   `rutina_prdida_de_peso_progresiva_salud.csv` (para IMC Obesidad)
    *   Estos serán ahora los archivos fuente directos.

2.  **Actualizar `config.py`:**
    *   En lugar de un solo `CSV_FILE_PATH`, podríamos tener un diccionario que mapee los objetivos o categorías de IMC a sus respectivos nombres de archivo CSV.
    *   Ejemplo:
        ```python
        ROUTINE_CSVS = {
            "Bajo Peso": "rutina_ganancia_de_masa_muscular.csv",
            "Normal": "rutina_mantenimiento_bienestar_general.csv",
            "Sobrepeso": "rutina_prdida_de_peso.csv",
            "Obesidad": "rutina_prdida_de_peso_progresiva_salud.csv"
        }
        ```

3.  **Actualizar `backend.py`:**
    *   **`DatabaseManager`**:
        *   `load_exercises()` ya no cargará un solo CSV maestro.
        *   Podría eliminarse o reorientarse si fuera necesario para alguna otra gestión de datos, pero para la lógica principal de rutinas, no será el cargador central de *todos* los ejercicios.
        *   `get_exercises_by_criteria()`: Su lógica cambiará drásticamente. En lugar de filtrar un DataFrame grande, podría ser responsable de leer el contenido del archivo CSV específico basado en la `imc_category` proporcionada. Devolverá una lista de objetos `Exercise` leídos de ese CSV.
        *   `update_exercise_database()`: Probablemente ya no sea relevante en este nuevo modelo si las rutinas son fijas por archivo.
        *   `save_exercises_to_csv()`: No será necesario para la generación de rutinas personalizadas, ya que las rutinas ahora están predefinidas en archivos.

    *   **`Exercise`**: La clase sigue siendo útil para estructurar los datos de cada ejercicio.

    *   **`IMCCalculator`**: Sigue siendo igual para calcular el IMC y determinar la categoría. Su método `get_all_training_goals_with_imc_categories()` ya no sería para generar CSVs, sino para ayudar a mapear la categoría de IMC a un archivo CSV.

    *   **`WorkoutGenerator`**:
        *   `generate_routine(self, user_data: UserData)`:
            *   Calculará el IMC y la categoría de IMC.
            *   Usará la categoría de IMC para determinar qué archivo CSV de rutina cargar (a través del `DatabaseManager` modificado).
            *   Leerá todos los ejercicios de ese CSV específico.
            *   Creará un `WorkoutPlan` con *todos* los ejercicios de ese archivo CSV (ya no hay `num_exercises` para seleccionar un subconjunto, a menos que decidas mantener esa opción dentro de la rutina predefinida).
        *   `generate_and_save_routines_for_all_goals()`: Este método ya no es necesario, porque los CSVs de rutinas ahora son la fuente, no el destino.

    *   **`WorkoutPlan`**: Sigue siendo útil para pasar la rutina seleccionada al frontend.

4.  **Actualizar `frontend.py` (`FrontendController`):**
    *   Ya no necesitará llamar a `workout_generator.generate_and_save_routines_for_all_goals()` al inicio.
    *   La lógica de `handle_form_submission` seguirá llamando a `workout_generator.generate_routine()`, pero esta función ahora devolverá una rutina completa de un archivo CSV específico.
    *   La ruta y el método `render_general_routines_page()`:
        *   En lugar de buscar archivos CSV generados, ahora directamente usará el mapeo de `Config.ROUTINE_CSVS`.
        *   Para cada archivo CSV en `Config.ROUTINE_CSVS`, lo leerá y pasará los datos a la plantilla `general_routines.html`. Esto es bastante similar a lo que ya hacía, pero la fuente de los nombres de archivo será más directa desde la configuración.

5.  **Eliminar Archivos No Necesarios:**
    *   El archivo `exercises.csv` original (el maestro) ya no sería la fuente principal y podría eliminarse o archivarse si todas las rutinas están cubiertas por los CSVs específicos. Por ahora, lo dejaremos, pero `DatabaseManager` dejará de usarlo por defecto.

Empecemos con los cambios.

**Paso 1: Actualizar `config.py`**


```python
        ROUTINE_CSVS = {
            "Bajo Peso": "rutina_ganancia_de_masa_muscular.csv",
            "Normal": "rutina_mantenimiento_bienestar_general.csv",
            "Sobrepeso": "rutina_prdida_de_peso.csv",
            "Obesidad": "rutina_prdida_de_peso_progresiva_salud.csv"
        }
```

```python
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

```

**Paso 2: Actualizar `backend.py`**

Primero, la clase `Exercise` se mantiene igual. `IMCCalculator` se mantiene igual.
Modificaremos `DatabaseManager`.
El `__init__` ya no necesita `csv_file_path` ni llamar a `load_exercises`.
`load_exercises` se elimina.
`get_exercises_by_criteria` se reescribe.
`update_exercise_database` y `save_exercises_to_csv` (la que guarda una lista de ejercicios en un archivo) ya no son estrictamente necesarias para la lógica principal, pero las dejaré comentadas por si son útiles para alguna herramienta de administración futura. Los prints de depuración que añadimos antes se quitarán o adaptarán.



```python
import pandas as pd
from config import Config # Para acceder a ROUTINE_CSVS
from typing import List, Dict, Any
import random # Para seleccionar ejercicios aleatoriamente si es necesario
import os # Para manejar rutas y archivos

class UserData:
    # ... (sin cambios)
// ... existing code ...
    def get_all_training_goals_with_imc_categories(self) -> Dict[str, str]:
        """Devuelve un diccionario de todos los objetivos de entrenamiento y sus categorías de IMC asociadas."""
        # Estas categorías deben coincidir con las usadas en get_imc_category y las claves de Config.ROUTINE_CSVS
        return {
            "Ganancia de Masa Muscular": "Bajo Peso",
            "Mantenimiento y Bienestar General": "Normal",
            "Pérdida de Peso": "Sobrepeso",
            "Pérdida de Peso Progresiva y Salud": "Obesidad"
        }

class Exercise:
    # ... (sin cambios)
// ... existing code ...
class DatabaseManager:
    def __init__(self):
        # Ya no carga un CSV maestro al iniciar.
        # self.exercises_data se cargará bajo demanda por get_exercises_from_routine_file
        pass 

    # load_exercises() ya no es necesaria como antes.
    # def load_exercises(self): ... 

    def get_exercises_from_routine_file(self, imc_category: str) -> List[Exercise]:
        """Carga ejercicios desde el archivo CSV de rutina específico para la categoría de IMC."""
        print(f"[DB GET ROUTINE] Solicitando rutina para IMC Category: '{imc_category}'")
        routine_csv_filename = Config.ROUTINE_CSVS.get(imc_category)

        if not routine_csv_filename:
            print(f"[DB GET ROUTINE ERROR] No se encontró un archivo CSV de rutina para la categoría de IMC: '{imc_category}'")
            return []
        
        abs_path = os.path.abspath(routine_csv_filename)
        print(f"[DB GET ROUTINE] Intentando cargar desde: {abs_path}")

        try:
            if not os.path.exists(routine_csv_filename):
                print(f"[DB GET ROUTINE ERROR] Archivo no encontrado: {abs_path}")
                return []
                
            df = pd.read_csv(routine_csv_filename)
            print(f"[DB GET ROUTINE] CSV '{routine_csv_filename}' cargado. Shape: {df.shape}. Vacío: {df.empty}")

            # Convertir la columna 'equipment_needed' de string a lista
            if 'equipment_needed' in df.columns:
                df['equipment_needed'] = df['equipment_needed'].apply(
                    lambda x: [item.strip() for item in str(x).split(',')] if pd.notna(x) and str(x).strip().lower() not in ['', 'nan'] else []
                )
            else:
                df['equipment_needed'] = [[] for _ in range(len(df))]
            
            exercises_list = []
            for _, row in df.iterrows():
                try:
                    exercise_id = int(row['id'])
                except ValueError:
                    print(f"[DB GET ROUTINE WARN] ID de ejercicio no válido '{row['id']}' en {routine_csv_filename}. Saltando.")
                    continue
                
                exercises_list.append(Exercise(
                    id=exercise_id,
                    name=str(row['name']),
                    description=str(row['description']),
                    imc_range=str(row['imc_range']), # Esta columna podría ser redundante ahora
                    difficulty=str(row['difficulty']),
                    category=str(row['category']),
                    gender_specific=str(row['gender_specific']), # Podría ser redundante
                    equipment_needed=row['equipment_needed'] if isinstance(row['equipment_needed'], list) else []
                ))
            print(f"[DB GET ROUTINE] Devolviendo {len(exercises_list)} ejercicios de '{routine_csv_filename}'")
            return exercises_list

        except FileNotFoundError:
            print(f"[DB GET ROUTINE ERROR] FileNotFoundError: El archivo CSV de rutina '{routine_csv_filename}' no fue encontrado.")
            return []
        except Exception as e:
            print(f"[DB GET ROUTINE ERROR] Exception al cargar CSV de rutina '{routine_csv_filename}': {e}")
            return []

    # get_exercises_by_criteria() fue reemplazada por get_exercises_from_routine_file

    # def update_exercise_database(self, new_exercise: Exercise): ... (Comentada o eliminada)
    # def save_exercises_to_csv(self, exercises: List[Exercise], filename: str): ... (Comentada o eliminada)

class WorkoutPlan:
    # ... (sin cambios)
// ... existing code ...
class WorkoutGenerator:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.imc_calculator = IMCCalculator()

    def generate_routine(self, user_data: UserData) -> WorkoutPlan:
        """Genera una rutina de ejercicios cargando el CSV apropiado según el IMC del usuario."""
        imc = self.imc_calculator.calculate_imc(user_data.weight, user_data.height)
        imc_category = self.imc_calculator.get_imc_category(imc)
        training_goal = self.imc_calculator.determine_training_goal(imc) # Se mantiene para info al usuario
        
        print(f"[WG GEN ROUTINE] IMC: {imc}, Categoría: {imc_category}, Objetivo: {training_goal}")
        
        # Obtener todos los ejercicios del archivo CSV de rutina correspondiente a la categoría de IMC
        # Ya no se filtra por género aquí, se asume que el CSV de rutina ya está curado.
        # O si se quisiera mantener, se podría añadir un filtro post-carga aquí.
        selected_exercises = self.db_manager.get_exercises_from_routine_file(imc_category)

        if not selected_exercises:
            print(f"[WG GEN ROUTINE] No se encontraron ejercicios en el archivo CSV para '{imc_category}'.")
            return WorkoutPlan(exercises=[], goal=training_goal, difficulty_level="Variable")
        
        # Determinar la dificultad general del plan basado en los ejercicios seleccionados
        plan_difficulty = "Intermedio" # Default
        if selected_exercises:
            difficulties = [ex.difficulty for ex in selected_exercises if ex.difficulty]
            if difficulties:
                plan_difficulty = max(set(difficulties), key=difficulties.count)

        print(f"[WG GEN ROUTINE] Plan generado con {len(selected_exercises)} ejercicios.")
        return WorkoutPlan(
            exercises=selected_exercises, 
            goal=training_goal, 
            difficulty_level=plan_difficulty
        )

    # _sanitize_filename y generate_and_save_routines_for_all_goals ya no son necesarios aquí.
    # def _sanitize_filename(self, name: str) -> str: ...
    # def generate_and_save_routines_for_all_goals(self, num_exercises_per_routine: int = 5): ...

# ... (Eliminar comentario residual si aún existe al final)

```

Se han reescrito `DatabaseManager` y `WorkoutGenerator` en `backend.py` para adoptar la nueva lógica.

**Paso 3: Actualizar `frontend.py`**
`FrontendController` ya no llamará a `generate_and_save_routines_for_all_goals`. La lógica de `render_general_routines_page` cambiará para usar `Config.ROUTINE_CSVS`.


```python
from flask import render_template, request, redirect, url_for
import pandas as pd # Para leer los CSVs de rutinas
import os 

from backend import UserData, IMCCalculator, WorkoutGenerator, DatabaseManager # DatabaseManager sigue siendo necesario
from config import Config

class FrontendController:
    def __init__(self, app, db_manager_instance):
        self.app = app
        # db_manager_instance sigue siendo útil para WorkoutGenerator
        self.db_manager = db_manager_instance 
        self.imc_calculator = IMCCalculator()
        # WorkoutGenerator ahora usará el db_manager_instance modificado
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

    # ... (render_home_page, render_calculator_form, handle_form_submission sin cambios significativos aquí, 
    #      ya que dependen de workout_generator.generate_routine cuya lógica interna cambió)
    # ... (display_error_message sin cambios)
// ... existing code ...
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

# ... (resto del archivo igual)

```

**Paso 4: Revisar `main.py`**
No se necesitan cambios en `main.py` ya que la instanciación de `DatabaseManager` (ahora sin argumentos) y `FrontendController` sigue siendo la misma. `FrontendController` ya no llama a métodos de generación de CSVs en `WorkoutGenerator`.

**Paso 5: CSVs Existentes**
Los archivos CSV que creamos ( `rutina_ganancia_de_masa_muscular.csv`, `rutina_mantenimiento_bienestar_general.csv`, `rutina_prdida_de_peso.csv`, `rutina_prdida_de_peso_progresiva_salud.csv`) ahora son los archivos fuente directos.
El archivo `exercises.csv` original ya no es utilizado por `DatabaseManager` en esta nueva lógica. Puedes conservarlo o eliminarlo.

**Resumen de la Nueva Lógica:**

1.  **Usuario solicita rutina personalizada:**
    *   `FrontendController.handle_form_submission` recibe los datos.
    *   Llama a `WorkoutGenerator.generate_routine(user_data)`.
    *   `generate_routine` calcula el IMC y la categoría de IMC (ej: "Obesidad").
    *   Llama a `DatabaseManager.get_exercises_from_routine_file("Obesidad")`.
    *   `get_exercises_from_routine_file` usa `Config.ROUTINE_CSVS["Obesidad"]` para obtener el nombre de archivo `rutina_prdida_de_peso_progresiva_salud.csv`.
    *   Lee este CSV, convierte sus filas en objetos `Exercise`.
    *   Devuelve la lista de ejercicios a `WorkoutGenerator`.
    *   `WorkoutGenerator` crea un `WorkoutPlan` con estos ejercicios.
    *   El plan se envía a la plantilla `workout_results.html`.

2.  **Usuario visita `/general_routines`:**
    *   `FrontendController.render_general_routines_page` itera sobre `Config.ROUTINE_CSVS`.
    *   Para cada entrada (ej: "Bajo Peso": "rutina_ganancia_de_masa_muscular.csv"):
        *   Llama a `DatabaseManager.get_exercises_from_routine_file("Bajo Peso")`.
        *   Este carga `rutina_ganancia_de_masa_muscular.csv`.
        *   Los ejercicios se pasan a la plantilla `general_routines.html`.

Con estos cambios, la aplicación debería funcionar según tu nueva especificación.
Te recomiendo probar la generación de rutinas personalizadas y la página de rutinas generales. Los `print` que he dejado en los métodos de carga de `DatabaseManager` y en `WorkoutGenerator` te ayudarán a seguir el flujo y a depurar si algo no sale como se espera.

---

**User**

Hay errores con los import, arreglalo

---

**Cursor**

Tienes razón, revisando los cambios, es muy probable que haya introducido o no haya corregido algunos problemas de importación, especialmente relacionados con `os` o con cómo se llaman ahora los métodos.

Por favor, ¿podrías compartir el error exacto de importación que estás viendo en la consola cuando intentas ejecutar `python main.py`?

El traceback completo del error me dirá exactamente qué archivo y qué línea están causando el `ImportError` o `AttributeError` (si es un método mal llamado después de los cambios).

Mientras tanto, revisaré los archivos que modificamos (`config.py`, `backend.py`, `frontend.py`) en busca de problemas obvios de importación o referencias incorrectas basadas en las últimas modificaciones.

**Revisión Preliminar:**

1.  **`backend.py`**:
    *   Asegurarse de que `import os` esté presente si se usa `os.path.abspath` o `os.path.exists`. Lo añadí en una de las ediciones, pero es bueno confirmarlo.
    *   Confirmar que `from config import Config` esté correcto y se use `Config.ROUTINE_CSVS`.
    *   La clase `DatabaseManager` ahora tiene `get_exercises_from_routine_file`. `WorkoutGenerator` debe llamar a este método.

2.  **`frontend.py`**:
    *   Asegurarse de que `import os` y `import pandas as pd` estén si se usan.
    *   Verificar que `from config import Config` se use para `Config.ROUTINE_CSVS`.
    *   Confirmar que `from backend import ... DatabaseManager` se mantenga si `FrontendController` instancia o usa métodos de `DatabaseManager` (lo hace al crear `temp_db_manager`).

3.  **`main.py`**:
    *   Debería importar `DatabaseManager` de `backend` y `FrontendController` de `frontend`.
    *   La instanciación de `DatabaseManager` en `main.py` (dentro de `FlaskApp.__init__`) ahora debería ser `self.db_manager = DatabaseManager()` (sin argumentos), ya que el `__init__` de `DatabaseManager` cambió.

Voy a aplicar este cambio en `main.py` ya que es un error probable basado en nuestras últimas modificaciones a `DatabaseManager`.


```python
// ... existing code ...
        # Instanciar DatabaseManager
        self.db_manager = DatabaseManager() # Ahora __init__ no toma argumentos

        # Instanciar y registrar el controlador del frontend
// ... existing code ...
```

Este es un cambio que probablemente era necesario. Sin embargo, el error exacto que estás viendo me ayudará a identificar cualquier otro problema de importación o referencia.

Por favor, comparte el traceback del error.

---

**User**

@main.py No has llegado a arreglar el error, 

---

**Cursor**

¡Tienes toda la razón! Se me pasó por alto ese detalle.

Cuando modificamos `config.py` para usar `ROUTINE_CSVS` en lugar de un único `CSV_FILE_PATH`, comenté la línea `CSV_FILE_PATH = 'exercises.csv'` en `config.py`.

Sin embargo, en `main.py`, dentro de `FlaskApp.__init__`, todavía hay una línea que intenta acceder a `Config.CSV_FILE_PATH`:
```python
self.app.config['CSV_FILE_PATH'] = Config.CSV_FILE_PATH
```
Esto está causando el `AttributeError: type object 'Config' has no attribute 'CSV_FILE_PATH'`.

Dado que ya no usamos un `CSV_FILE_PATH` único y central en la configuración para la carga de datos (porque ahora cargamos rutinas específicas de archivos CSV dedicados), esta línea en `main.py` ya no es necesaria y puede eliminarse. La configuración de la aplicación Flask (`self.app.config`) ya no necesita esta ruta específica.

Voy a eliminar esa línea de `main.py`.


```python
self.app.config['CSV_FILE_PATH'] = Config.CSV_FILE_PATH
```

```python
        self.host = host
        self.port = port
        
        # Configurar la app con valores de Config
        self.app.config['FLASK_HOST'] = Config.FLASK_HOST
        self.app.config['FLASK_PORT'] = Config.FLASK_PORT
        # self.app.config['CSV_FILE_PATH'] = Config.CSV_FILE_PATH # Esta línea ya no es necesaria
        self.app.config['DEBUG'] = Config.DEBUG_MODE

        # Instanciar DatabaseManager

```

Con esta corrección, el `AttributeError` que estabas viendo debería resolverse. La aplicación ahora no intentará acceder a un atributo que ya no existe en la clase `Config`.

Por favor, intenta ejecutar `python main.py` de nuevo. Si surgen otros errores, por favor comparte el traceback completo.

