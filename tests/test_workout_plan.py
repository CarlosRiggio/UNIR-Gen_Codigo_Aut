import pytest
import sys
import os

# Agregar el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.backend import WorkoutPlan, Exercise

class TestWorkoutPlan:
    """Test suite para la clase WorkoutPlan"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.sample_exercises = [
            Exercise(1, "Push-ups", "Ejercicio de pecho", "Normal", "Intermedio", "Fuerza", "Any", []),
            Exercise(2, "Squats", "Ejercicio de piernas", "Normal", "Intermedio", "Fuerza", "Any", ["Pesas"]),
            Exercise(3, "Running", "Ejercicio cardiovascular", "Normal", "Principiante", "Cardio", "Any", [])
        ]
    
    def test_init_with_defaults(self):
        """Test de inicialización con valores por defecto"""
        plan = WorkoutPlan(self.sample_exercises, "Test Goal")
        
        assert plan.exercises == self.sample_exercises
        assert plan.goal == "Test Goal"
        assert plan.duration == 30  # Default
        assert plan.difficulty_level == "Intermedio"  # Default
    
    def test_init_with_custom_values(self):
        """Test de inicialización con valores personalizados"""
        plan = WorkoutPlan(
            exercises=self.sample_exercises,
            goal="Pérdida de Peso",
            duration=45,
            difficulty_level="Avanzado"
        )
        
        assert plan.exercises == self.sample_exercises
        assert plan.goal == "Pérdida de Peso"
        assert plan.duration == 45
        assert plan.difficulty_level == "Avanzado"
    
    def test_init_with_empty_exercises(self):
        """Test de inicialización con lista de ejercicios vacía"""
        plan = WorkoutPlan([], "Empty Goal")
        
        assert plan.exercises == []
        assert plan.goal == "Empty Goal"
        assert len(plan.exercises) == 0
    
    def test_get_plan_summary_complete(self):
        """Test de resumen del plan completo"""
        plan = WorkoutPlan(
            exercises=self.sample_exercises,
            goal="Ganancia de Masa",
            duration=50,
            difficulty_level="Avanzado"
        )
        
        summary = plan.get_plan_summary()
        
        expected_summary = {
            "goal": "Ganancia de Masa",
            "duration_minutes": 50,
            "difficulty_level": "Avanzado",
            "number_of_exercises": 3,
            "exercises": [ex.to_dict() for ex in self.sample_exercises]
        }
        
        assert summary == expected_summary
    
    def test_get_plan_summary_empty_exercises(self):
        """Test de resumen con ejercicios vacíos"""
        plan = WorkoutPlan([], "Empty Goal")
        summary = plan.get_plan_summary()
        
        assert summary["number_of_exercises"] == 0
        assert summary["exercises"] == []
        assert summary["goal"] == "Empty Goal"
    
    def test_to_html_with_exercises(self):
        """Test de generación HTML con ejercicios"""
        plan = WorkoutPlan(
            exercises=self.sample_exercises,
            goal="Test Goal",
            duration=40,
            difficulty_level="Intermedio"
        )
        
        html = plan.to_html()
        
        # Verificar elementos HTML básicos
        assert "<h3>Objetivo: Test Goal</h3>" in html
        assert "Dificultad: Intermedio, Duración Estimada: 40 min" in html
        assert "<ul>" in html and "</ul>" in html
        
        # Verificar que todos los ejercicios están incluidos
        for exercise in self.sample_exercises:
            assert exercise.name in html
            assert exercise.description in html
    
    def test_to_html_empty_exercises(self):
        """Test de generación HTML sin ejercicios"""
        plan = WorkoutPlan([], "Empty Goal")
        html = plan.to_html()
        
        assert html == "<h3>Objetivo: Empty Goal</h3><p>No se encontraron ejercicios para este plan.</p>"
    
    def test_to_html_exercise_with_equipment(self):
        """Test de generación HTML con equipamiento"""
        exercise_with_equipment = Exercise(
            1, "Bench Press", "Ejercicio de pecho", "Normal", "Avanzado", "Fuerza", "Any", ["Banco", "Mancuernas"]
        )
        
        plan = WorkoutPlan([exercise_with_equipment], "Fuerza")
        html = plan.to_html()
        
        assert "Banco, Mancuernas" in html
        assert "<i>Equipo:" in html
    
    def test_to_html_exercise_without_equipment(self):
        """Test de generación HTML sin equipamiento"""
        exercise_no_equipment = Exercise(
            1, "Push-ups", "Ejercicio de pecho", "Normal", "Intermedio", "Fuerza", "Any", []
        )
        
        plan = WorkoutPlan([exercise_no_equipment], "Bodyweight")
        html = plan.to_html()
        
        assert "<i>Equipo: Ninguno</i>" in html
    
    def test_to_html_exercise_with_empty_equipment_list(self):
        """Test de HTML con lista de equipamiento que contiene strings vacíos"""
        exercise_empty_equipment = Exercise(
            1, "Jumping Jacks", "Ejercicio cardio", "Normal", "Principiante", "Cardio", "Any", ['']
        )
        
        plan = WorkoutPlan([exercise_empty_equipment], "Cardio")
        html = plan.to_html()
        
        # Debería mostrar "Ninguno" cuando la lista contiene solo strings vacíos
        assert "<i>Equipo: Ninguno</i>" in html
    
    def test_to_html_multiple_exercises_different_categories(self):
        """Test de HTML con múltiples ejercicios de diferentes categorías"""
        diverse_exercises = [
            Exercise(1, "Push-ups", "Pecho", "Normal", "Intermedio", "Fuerza", "Any", []),
            Exercise(2, "Running", "Cardio", "Normal", "Principiante", "Cardio", "Any", []),
            Exercise(3, "Yoga", "Estiramiento", "Normal", "Principiante", "Flexibilidad", "Any", ["Mat"])
        ]
        
        plan = WorkoutPlan(diverse_exercises, "Completo")
        html = plan.to_html()
        
        # Verificar que todas las categorías están presentes
        assert "Fuerza" in html
        assert "Cardio" in html
        assert "Flexibilidad" in html
        
        # Verificar que todos los niveles de dificultad están presentes
        assert "Intermedio" in html
        assert "Principiante" in html
    
    def test_plan_summary_exercises_serialization(self):
        """Test de serialización de ejercicios en el resumen"""
        plan = WorkoutPlan(self.sample_exercises, "Test")
        summary = plan.get_plan_summary()
        
        # Verificar que los ejercicios se serializan correctamente
        assert len(summary["exercises"]) == len(self.sample_exercises)
        
        for i, exercise_dict in enumerate(summary["exercises"]):
            original_exercise = self.sample_exercises[i]
            assert exercise_dict == original_exercise.to_dict()
    
    def test_workout_plan_duration_types(self):
        """Test con diferentes tipos de duración"""
        # Duración como entero
        plan1 = WorkoutPlan([], "Test", duration=30)
        assert plan1.duration == 30
        assert isinstance(plan1.duration, int)
        
        # Duración como float
        plan2 = WorkoutPlan([], "Test", duration=45.5)
        assert plan2.duration == 45.5
        assert isinstance(plan2.duration, float)
    
    def test_workout_plan_goal_special_characters(self):
        """Test con caracteres especiales en el objetivo"""
        goal_with_special_chars = "Pérdida de peso rápida & saludable"
        plan = WorkoutPlan([], goal_with_special_chars)
        
        assert plan.goal == goal_with_special_chars
        
        html = plan.to_html()
        assert goal_with_special_chars in html
    
    def test_workout_plan_immutability_of_exercises(self):
        """Test que modificar la lista original no afecta el plan"""
        original_exercises = self.sample_exercises.copy()
        plan = WorkoutPlan(original_exercises, "Test")
        
        # Modificar la lista original
        original_exercises.append(Exercise(99, "New", "New desc", "Normal", "Inter", "Cardio", "Any", []))
        
        # El plan no debería verse afectado
        assert len(plan.exercises) == 3  # Original length
        assert plan.exercises[-1].id != 99 