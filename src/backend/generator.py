"""
Generador de rutinas de ejercicio basado en datos del usuario.
"""

from .models import UserData, WorkoutPlan
from .calculator import IMCCalculator
from .database import DatabaseManager


class WorkoutGenerator:
    """Generador de rutinas de ejercicio personalizadas."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.imc_calculator = IMCCalculator()

    def generate_routine(self, user_data: UserData) -> WorkoutPlan:
        """Genera una rutina de ejercicios cargando el CSV apropiado según el IMC del usuario."""
        imc = self.imc_calculator.calculate_imc(user_data.weight, user_data.height)
        imc_category = self.imc_calculator.get_imc_category(imc)
        training_goal = self.imc_calculator.determine_training_goal(imc)  # Se mantiene para info al usuario
        
        print(f"[WG GEN ROUTINE] IMC: {imc}, Categoría: {imc_category}, Objetivo: {training_goal}")
        
        # Obtener todos los ejercicios del archivo CSV de rutina correspondiente a la categoría de IMC
        # Ya no se filtra por género aquí, se asume que el CSV de rutina ya está curado.
        # O si se quisiera mantener, se podría añadir un filtro post-carga aquí.
        selected_exercises = self.db_manager.get_exercises_from_routine_file(imc_category)

        if not selected_exercises:
            print(f"[WG GEN ROUTINE] No se encontraron ejercicios en el archivo CSV para '{imc_category}'.")
            return WorkoutPlan(exercises=[], goal=training_goal, difficulty_level="Variable")
        
        # Determinar la dificultad general del plan basado en los ejercicios seleccionados
        plan_difficulty = "Intermedio"  # Default
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