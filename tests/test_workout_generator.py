import pytest
import sys
import os

# Agregar el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.backend import WorkoutGenerator, DatabaseManager, UserData, IMCCalculator, WorkoutPlan

class TestWorkoutGenerator:
    """Test suite para la clase WorkoutGenerator"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.db_manager = DatabaseManager()
        self.workout_generator = WorkoutGenerator(self.db_manager)
    
    def test_init_workout_generator(self):
        """Test de inicialización del WorkoutGenerator"""
        generator = WorkoutGenerator(self.db_manager)
        
        assert generator.db_manager is not None
        assert isinstance(generator.imc_calculator, IMCCalculator)
    
    def test_generate_routine_bajo_peso(self):
        """Test de generación de rutina para bajo peso"""
        # Usuario con bajo peso (IMC < 18.5)
        user_data = UserData("male", 1.80, 55.0, 25)  # IMC ≈ 17.0
        
        workout_plan = self.workout_generator.generate_routine(user_data)
        
        assert isinstance(workout_plan, WorkoutPlan)
        assert workout_plan.goal == "Ganancia de Masa Muscular"
        # Verificar que los ejercicios provienen de la categoría correcta
        if workout_plan.exercises:
            # Si hay ejercicios cargados, verificar que son apropiados
            assert all(hasattr(ex, 'name') for ex in workout_plan.exercises)
    
    def test_generate_routine_normal(self):
        """Test de generación de rutina para peso normal"""
        # Usuario con peso normal (18.5 <= IMC <= 24.9)
        user_data = UserData("female", 1.65, 60.0, 28)  # IMC ≈ 22.0
        
        workout_plan = self.workout_generator.generate_routine(user_data)
        
        assert isinstance(workout_plan, WorkoutPlan)
        assert workout_plan.goal == "Mantenimiento y Bienestar General"
    
    def test_generate_routine_sobrepeso(self):
        """Test de generación de rutina para sobrepeso"""
        # Usuario con sobrepeso (25.0 <= IMC <= 29.9)
        user_data = UserData("male", 1.75, 80.0, 35)  # IMC ≈ 26.1
        
        workout_plan = self.workout_generator.generate_routine(user_data)
        
        assert isinstance(workout_plan, WorkoutPlan)
        assert workout_plan.goal == "Pérdida de Peso"
    
    def test_generate_routine_obesidad(self):
        """Test de generación de rutina para obesidad"""
        # Usuario con obesidad (IMC >= 30.0)
        user_data = UserData("female", 1.60, 85.0, 40)  # IMC ≈ 33.2
        
        workout_plan = self.workout_generator.generate_routine(user_data)
        
        assert isinstance(workout_plan, WorkoutPlan)
        assert workout_plan.goal == "Pérdida de Peso Progresiva y Salud"
    
    def test_generate_routine_boundary_values(self):
        """Test con valores límite de IMC"""
        # Exactamente en el límite bajo peso/normal
        user_data = UserData("male", 1.70, 53.465, 25)  # IMC = 18.5
        workout_plan = self.workout_generator.generate_routine(user_data)
        assert workout_plan.goal == "Mantenimiento y Bienestar General"
        
        # Exactamente en el límite normal/sobrepeso
        user_data = UserData("female", 1.70, 72.25, 30)  # IMC = 25.0
        workout_plan = self.workout_generator.generate_routine(user_data)
        assert workout_plan.goal == "Pérdida de Peso"
        
        # Exactamente en el límite sobrepeso/obesidad
        user_data = UserData("male", 1.70, 86.7, 25)  # IMC = 30.0
        workout_plan = self.workout_generator.generate_routine(user_data)
        assert workout_plan.goal == "Pérdida de Peso Progresiva y Salud"
    
    def test_generate_routine_consistency_with_imc_calculation(self):
        """Test de consistencia entre cálculo de IMC y generación de rutina"""
        test_users = [
            UserData("male", 1.75, 60.0, 25),    # Bajo peso
            UserData("female", 1.65, 65.0, 30),  # Normal
            UserData("other", 1.80, 85.0, 35),   # Sobrepeso
            UserData("male", 1.70, 95.0, 40),    # Obesidad
        ]
        
        for user in test_users:
            # Calcular IMC manualmente
            imc = self.workout_generator.imc_calculator.calculate_imc(user.weight, user.height)
            expected_category = self.workout_generator.imc_calculator.get_imc_category(imc)
            expected_goal = self.workout_generator.imc_calculator.determine_training_goal(imc)
            
            # Generar rutina
            workout_plan = self.workout_generator.generate_routine(user)
            
            # Verificar consistencia
            assert workout_plan.goal == expected_goal
    
    def test_generate_routine_extreme_values(self):
        """Test con valores extremos de peso/altura"""
        # Peso muy bajo
        user_low = UserData("female", 1.60, 30.0, 25)  # IMC ≈ 11.7
        workout_plan = self.workout_generator.generate_routine(user_low)
        assert workout_plan.goal == "Ganancia de Masa Muscular"
        
        # Peso muy alto
        user_high = UserData("male", 1.70, 150.0, 35)  # IMC ≈ 51.9
        workout_plan = self.workout_generator.generate_routine(user_high)
        assert workout_plan.goal == "Pérdida de Peso Progresiva y Salud"
        
        # Altura muy alta
        user_tall = UserData("male", 2.20, 70.0, 25)  # IMC ≈ 14.5
        workout_plan = self.workout_generator.generate_routine(user_tall)
        assert workout_plan.goal == "Ganancia de Masa Muscular"
    
    def test_generate_routine_plan_properties(self):
        """Test de propiedades del plan generado"""
        user_data = UserData("male", 1.75, 70.0, 30)
        workout_plan = self.workout_generator.generate_routine(user_data)
        
        # Verificar propiedades básicas del plan
        assert hasattr(workout_plan, 'exercises')
        assert hasattr(workout_plan, 'goal')
        assert hasattr(workout_plan, 'duration')
        assert hasattr(workout_plan, 'difficulty_level')
        
        # Verificar que el objetivo es válido
        valid_goals = [
            "Ganancia de Masa Muscular",
            "Mantenimiento y Bienestar General", 
            "Pérdida de Peso",
            "Pérdida de Peso Progresiva y Salud"
        ]
        assert workout_plan.goal in valid_goals
    
    def test_generate_routine_difficulty_level_assignment(self):
        """Test de asignación de nivel de dificultad"""
        user_data = UserData("female", 1.65, 60.0, 25)
        workout_plan = self.workout_generator.generate_routine(user_data)
        
        # Verificar que se asigna un nivel de dificultad válido
        valid_difficulties = ["Principiante", "Intermedio", "Avanzado", "Variable"]
        assert workout_plan.difficulty_level in valid_difficulties
    
    def test_generate_routine_with_no_exercises_available(self):
        """Test cuando no hay ejercicios disponibles para una categoría"""
        # Mock del database manager que no devuelve ejercicios
        class MockDBManager:
            def get_exercises_from_routine_file(self, category):
                return []
        
        generator = WorkoutGenerator(MockDBManager())
        user_data = UserData("male", 1.75, 70.0, 30)
        
        workout_plan = generator.generate_routine(user_data)
        
        # Debe devolver un plan vacío pero válido
        assert isinstance(workout_plan, WorkoutPlan)
        assert workout_plan.exercises == []
        assert workout_plan.difficulty_level == "Variable"
    
    def test_generate_routine_different_genders(self):
        """Test con diferentes géneros"""
        genders = ["male", "female", "other", "masculino", "femenino", "otro"]
        
        for gender in genders:
            user_data = UserData(gender, 1.70, 70.0, 30)
            workout_plan = self.workout_generator.generate_routine(user_data)
            
            # La rutina debe generarse independientemente del género
            assert isinstance(workout_plan, WorkoutPlan)
            assert workout_plan.goal is not None
    
    def test_generate_routine_different_ages(self):
        """Test con diferentes edades"""
        ages = [18, 25, 35, 50, 65, 80]
        
        for age in ages:
            user_data = UserData("male", 1.75, 70.0, age)
            workout_plan = self.workout_generator.generate_routine(user_data)
            
            # La rutina debe generarse independientemente de la edad
            assert isinstance(workout_plan, WorkoutPlan)
            assert workout_plan.goal is not None
    
    def test_generate_routine_imc_calculation_precision(self):
        """Test de precisión en el cálculo de IMC para generación de rutinas"""
        # Casos que podrían causar problemas de precisión en los límites
        edge_cases = [
            (1.75, 56.656),    # IMC ≈ 18.5
            (1.65, 67.731),    # IMC ≈ 24.9  
            (1.80, 81.0),      # IMC ≈ 25.0
            (1.70, 86.67),     # IMC ≈ 29.9
        ]
        
        for height, weight in edge_cases:
            user_data = UserData("male", height, weight, 30)
            workout_plan = self.workout_generator.generate_routine(user_data)
            
            # Debe asignar un objetivo válido incluso en casos límite
            valid_goals = [
                "Ganancia de Masa Muscular",
                "Mantenimiento y Bienestar General",
                "Pérdida de Peso", 
                "Pérdida de Peso Progresiva y Salud"
            ]
            assert workout_plan.goal in valid_goals
    
    def test_generate_routine_plan_summary_completeness(self):
        """Test de completitud del resumen del plan"""
        user_data = UserData("female", 1.60, 55.0, 25)
        workout_plan = self.workout_generator.generate_routine(user_data)
        
        summary = workout_plan.get_plan_summary()
        
        # Verificar que el resumen contiene todos los campos esperados
        required_fields = ["goal", "duration_minutes", "difficulty_level", 
                          "number_of_exercises", "exercises"]
        
        for field in required_fields:
            assert field in summary
            assert summary[field] is not None 