"""
Modelos de datos para el sistema de generación de rutinas de ejercicio.
"""

from typing import List, Dict, Any


class UserData:
    """Clase para almacenar y validar datos del usuario."""
    
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
        # Verificar que gender es string antes de usar .lower()
        if not isinstance(self.gender, str):
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


class Exercise:
    """Clase para representar un ejercicio individual."""
    
    def __init__(self, id: int, name: str, description: str, imc_range: str, 
                 difficulty: str, category: str, gender_specific: str, 
                 equipment_needed: List[str]):
        self.id = id
        self.name = name
        self.description = description
        self.imc_range = imc_range  # e.g., "Bajo Peso", "Normal", "Sobrepeso", "Obesidad"
        self.difficulty = difficulty  # e.g., "Principiante", "Intermedio", "Avanzado"
        self.category = category  # e.g., "Fuerza", "Cardio", "Flexibilidad"
        self.gender_specific = gender_specific  # e.g., "Any", "Male", "Female"
        self.equipment_needed = equipment_needed

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el ejercicio a un diccionario."""
        return self.__dict__


class WorkoutPlan:
    """Clase para representar un plan de entrenamiento completo."""
    
    def __init__(self, exercises: List[Exercise], goal: str, duration: int = 30, difficulty_level: str = "Intermedio"):
        # Crear una copia de la lista de ejercicios para evitar mutabilidad
        self.exercises = exercises.copy()
        self.goal = goal
        self.duration = duration  # Duración total estimada en minutos
        self.difficulty_level = difficulty_level

    def get_plan_summary(self) -> Dict[str, Any]:
        """Obtiene un resumen del plan de entrenamiento."""
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
            return f"<h3>Objetivo: {self.goal}</h3><p>No se encontraron ejercicios para este plan.</p>"

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