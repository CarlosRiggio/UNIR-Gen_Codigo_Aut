import pandas as pd
from config import Config # Para acceder a CSV_FILE_PATH y ROUTINE_CSVS
from typing import List, Dict, Any
import random # Para seleccionar ejercicios aleatoriamente si es necesario
import os # Para manejar rutas y archivos

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
    def __init__(self):
        # Ya no carga un CSV maestro al iniciar.
        # self.exercises_data se cargará bajo demanda por get_exercises_from_routine_file
        pass 

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

# Comentario residual que no pude eliminar antes, intentando nuevamente.
# Las clases WorkoutPlan y WorkoutGenerator se añadirán después. 