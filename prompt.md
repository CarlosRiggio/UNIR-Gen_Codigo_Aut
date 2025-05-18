Descripción del proyecto
El objetivo de nuestro proyecto es el desarrollo de una página web para la generación de rutinas de ejercicios personalizadas en función de la condición física del usuario. 
En la interfaz gráfica el cliente introducirá datos como su sexo, altura, el peso y edad. Con esta información, el sistema calculará el Índice de Masa Corporal (IMC).
Según el resultado del IMC, el sistema proporcionará una rutina de ejercicios personalizada. Por ejemplo, si el IMC indica bajo peso, se sugerirá una rutina enfocada en ganar masa muscular. Si el IMC es normal, se recomendará una rutina de mantenimiento y bienestar general. Para valores elevados de IMC, las rutinas estarán orientadas a la pérdida de peso, con ejercicios de cardio y fuerza progresiva.
Análisis de requisitos
Los requisitos a tener en cuenta son:
El lenguaje de programación que utilizaremos para las funciones del backend será Python debido a su facilidad de uso. 
Debido a su compatibilidad con Python, el frontend será implementado usando Flask

Para la implementación de la base de datos utilizaremos un archivo CSV.
Diagrama de clases
La estructura que tenemos pensada para el proyecto sería la siguiente:
main.py: este será el programa que se ejecutará y llamará al resto de programas para desplegar la interfaz gráfica y las demás funcionalidades del sistema. Como salida imprimirá por terminal la IP y puerto en la que se lanza nuestra web.
frontend.py: en este archivo se definen todas las funciones relacionadas con el diseño gráfico de la interfaz gráfica del sistema. 
backend.py: en este archivo se define la lógica de nuestro sistema, incluyendo las siguientes funcionalidades:
Calculadora de IMC: en base a los datos de sexo, altura, peso y edad introducidos por el usuario, se calcula su IMC.
Generación de rutina: a partir del IMC calculado, se extrae de la base de datos de ejercicios aquellos que estén indicados para la finalidad del entrenamiento sugerida por el sistema, como podría ser ganancia de masa muscular, pérdida de peso o mantenimiento. 
Base de datos: como base de datos tendremos 1 archivo CSV, donde estarán las descripciones de los ejercicios a hacer en función del rango del IMC obtenido. Cada ejercicio estará etiquetado en función del rango

Diagrama:
@startuml

skinparam classAttributeIconSize 0
skinparam backgroundColor white
skinparam roundcorner 5

class FlaskApp {
    - app: Flask
    - host: string
    - port: int
    + __init__()
    + run()
    + get_server_info(): tuple
}

class FrontendController {
    + render_home_page()
    + render_calculator_form()
    + render_workout_results()
    + handle_form_submission()
    + display_error_message()
}

class UserData {
    - gender: string
    - height: float
    - weight: float
    - age: int
    + validate_data(): bool
    + to_dict(): dict
}

class IMCCalculator {
    - UNDERWEIGHT_THRESHOLD: float
    - NORMAL_THRESHOLD: float
    - OVERWEIGHT_THRESHOLD: float
    - OBESE_THRESHOLD: float
    + calculate_imc(weight: float, height: float): float
    + get_imc_category(imc: float): string
    + determine_training_goal(imc: float): string
}

class WorkoutGenerator {
    - db_manager: DatabaseManager
    + generate_routine(imc: float, gender: string, age: int): List[Exercise]
    + filter_exercises_by_goal(exercises: List[Exercise], goal: string): List[Exercise]
    + create_workout_plan(filtered_exercises: List[Exercise]): WorkoutPlan
}

class Exercise {
    - id: int
    - name: string
    - description: string
    - imc_range: string
    - difficulty: string
    - category: string
    - gender_specific: string
    - equipment_needed: List[string]
    + to_dict(): dict
}

class WorkoutPlan {
    - exercises: List[Exercise]
    - duration: int
    - difficulty_level: string
    - goal: string
    + get_plan_summary(): dict
    + to_html(): string
}

class DatabaseManager {
    - CSV_FILE_PATH: string
    - exercises_data: DataFrame
    + __init__()
    + load_exercises()
    + get_exercises_by_criteria(imc: float, gender: string): List[Exercise]
    + update_exercise_database(new_exercise: Exercise)
}

class Config {
    + FLASK_HOST: string
    + FLASK_PORT: int
    + CSV_FILE_PATH: string
    + DEBUG_MODE: bool
}

FlaskApp --> FrontendController
FlaskApp --> Config
FrontendController --> UserData
FrontendController --> IMCCalculator
FrontendController --> WorkoutGenerator
WorkoutGenerator --> DatabaseManager
WorkoutGenerator --> Exercise
WorkoutGenerator --> WorkoutPlan
DatabaseManager --> Exercise

note right of FlaskApp
  Punto de entrada principal
  Configuración de Flask
end note

note right of IMCCalculator
  Cálculos y categorización
  del IMC según estándares
  médicos
end note

note right of WorkoutPlan
  Estructura final de la
  rutina generada para
  el usuario
end note

@enduml
