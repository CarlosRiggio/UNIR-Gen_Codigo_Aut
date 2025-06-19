import pytest
import sys
import os

# Agregar el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.backend import Exercise

class TestExercise:
    """Test suite para la clase Exercise"""
    
    def test_init_valid_exercise(self):
        """Test de inicialización con datos válidos"""
        exercise = Exercise(
            id=1,
            name="Push-ups",
            description="Ejercicio de fuerza para pecho",
            imc_range="Normal",
            difficulty="Intermedio",
            category="Fuerza",
            gender_specific="Any",
            equipment_needed=["Mat"]
        )
        
        assert exercise.id == 1
        assert exercise.name == "Push-ups"
        assert exercise.description == "Ejercicio de fuerza para pecho"
        assert exercise.imc_range == "Normal"
        assert exercise.difficulty == "Intermedio"
        assert exercise.category == "Fuerza"
        assert exercise.gender_specific == "Any"
        assert exercise.equipment_needed == ["Mat"]
    
    def test_init_with_empty_equipment(self):
        """Test de inicialización con lista de equipamiento vacía"""
        exercise = Exercise(
            id=2,
            name="Correr",
            description="Ejercicio cardiovascular",
            imc_range="Sobrepeso",
            difficulty="Principiante",
            category="Cardio",
            gender_specific="Any",
            equipment_needed=[]
        )
        
        assert exercise.equipment_needed == []
    
    def test_init_with_multiple_equipment(self):
        """Test de inicialización con múltiple equipamiento"""
        equipment = ["Mancuernas", "Banco", "Mat"]
        exercise = Exercise(
            id=3,
            name="Bench Press",
            description="Ejercicio de fuerza para pecho",
            imc_range="Bajo Peso",
            difficulty="Avanzado",
            category="Fuerza",
            gender_specific="Any",
            equipment_needed=equipment
        )
        
        assert exercise.equipment_needed == equipment
        assert len(exercise.equipment_needed) == 3
    
    def test_to_dict_complete(self):
        """Test de conversión a diccionario con todos los campos"""
        exercise = Exercise(
            id=4,
            name="Squats",
            description="Ejercicio para piernas",
            imc_range="Normal",
            difficulty="Intermedio",
            category="Fuerza",
            gender_specific="Any",
            equipment_needed=["Pesas"]
        )
        
        expected_dict = {
            'id': 4,
            'name': 'Squats',
            'description': 'Ejercicio para piernas',
            'imc_range': 'Normal',
            'difficulty': 'Intermedio',
            'category': 'Fuerza',
            'gender_specific': 'Any',
            'equipment_needed': ['Pesas']
        }
        
        assert exercise.to_dict() == expected_dict
    
    def test_to_dict_with_empty_equipment(self):
        """Test de conversión a diccionario con equipamiento vacío"""
        exercise = Exercise(
            id=5,
            name="Jumping Jacks",
            description="Ejercicio cardiovascular",
            imc_range="Obesidad",
            difficulty="Principiante",
            category="Cardio",
            gender_specific="Any",
            equipment_needed=[]
        )
        
        result_dict = exercise.to_dict()
        assert result_dict['equipment_needed'] == []
        assert 'id' in result_dict
        assert 'name' in result_dict
    
    def test_init_with_different_categories(self):
        """Test con diferentes categorías de ejercicio"""
        categories = ["Fuerza", "Cardio", "Flexibilidad", "Equilibrio"]
        
        for i, category in enumerate(categories):
            exercise = Exercise(
                id=i,
                name=f"Exercise {i}",
                description=f"Description {i}",
                imc_range="Normal",
                difficulty="Intermedio",
                category=category,
                gender_specific="Any",
                equipment_needed=[]
            )
            assert exercise.category == category
    
    def test_init_with_different_difficulties(self):
        """Test con diferentes niveles de dificultad"""
        difficulties = ["Principiante", "Intermedio", "Avanzado"]
        
        for i, difficulty in enumerate(difficulties):
            exercise = Exercise(
                id=i,
                name=f"Exercise {i}",
                description=f"Description {i}",
                imc_range="Normal",
                difficulty=difficulty,
                category="Fuerza",
                gender_specific="Any",
                equipment_needed=[]
            )
            assert exercise.difficulty == difficulty
    
    def test_init_with_different_imc_ranges(self):
        """Test con diferentes rangos de IMC"""
        imc_ranges = ["Bajo Peso", "Normal", "Sobrepeso", "Obesidad"]
        
        for i, imc_range in enumerate(imc_ranges):
            exercise = Exercise(
                id=i,
                name=f"Exercise {i}",
                description=f"Description {i}",
                imc_range=imc_range,
                difficulty="Intermedio",
                category="Fuerza",
                gender_specific="Any",
                equipment_needed=[]
            )
            assert exercise.imc_range == imc_range
    
    def test_init_with_different_gender_specific(self):
        """Test con diferentes especificaciones de género"""
        gender_options = ["Any", "Male", "Female"]
        
        for i, gender in enumerate(gender_options):
            exercise = Exercise(
                id=i,
                name=f"Exercise {i}",
                description=f"Description {i}",
                imc_range="Normal",
                difficulty="Intermedio",
                category="Fuerza",
                gender_specific=gender,
                equipment_needed=[]
            )
            assert exercise.gender_specific == gender
    
    def test_init_with_integer_and_string_ids(self):
        """Test con diferentes tipos de ID"""
        # ID como entero
        exercise1 = Exercise(
            id=10,
            name="Exercise 1",
            description="Description 1",
            imc_range="Normal",
            difficulty="Intermedio",
            category="Fuerza",
            gender_specific="Any",
            equipment_needed=[]
        )
        assert exercise1.id == 10
        assert isinstance(exercise1.id, int)
    
    def test_to_dict_preserves_data_types(self):
        """Test que to_dict preserva los tipos de datos"""
        exercise = Exercise(
            id=99,
            name="Test Exercise",
            description="Test Description",
            imc_range="Normal",
            difficulty="Intermedio",
            category="Fuerza",
            gender_specific="Any",
            equipment_needed=["Item1", "Item2"]
        )
        
        result = exercise.to_dict()
        
        assert isinstance(result['id'], int)
        assert isinstance(result['name'], str)
        assert isinstance(result['description'], str)
        assert isinstance(result['equipment_needed'], list)
        assert all(isinstance(item, str) for item in result['equipment_needed'])
    
    def test_exercise_equality_through_dict(self):
        """Test de igualdad a través de comparación de diccionarios"""
        exercise1 = Exercise(1, "Test", "Desc", "Normal", "Inter", "Fuerza", "Any", [])
        exercise2 = Exercise(1, "Test", "Desc", "Normal", "Inter", "Fuerza", "Any", [])
        
        assert exercise1.to_dict() == exercise2.to_dict()
    
    def test_exercise_with_special_characters(self):
        """Test con caracteres especiales en texto"""
        exercise = Exercise(
            id=1,
            name="Ejercício com acentõs",
            description="Descripción con ñ, á, é, í, ó, ú",
            imc_range="Normal",
            difficulty="Intermedio",
            category="Fuerza",
            gender_specific="Any",
            equipment_needed=["Equipación especial"]
        )
        
        result = exercise.to_dict()
        assert "ñ" in result['description']
        assert "õ" in result['name'] 