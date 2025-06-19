import pytest
import sys
import os

# Agregar el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.backend import UserData

class TestUserData:
    """Test suite para la clase UserData"""
    
    def test_init_valid_data(self):
        """Test de inicialización con datos válidos"""
        user = UserData("masculino", 1.75, 70.5, 25)
        assert user.gender == "masculino"
        assert user.height == 1.75
        assert user.weight == 70.5
        assert user.age == 25
    
    def test_init_with_different_gender_formats(self):
        """Test con diferentes formatos de género"""
        valid_genders = ["male", "female", "other", "masculino", "femenino", "otro"]
        for gender in valid_genders:
            user = UserData(gender, 1.70, 65.0, 30)
            assert user.gender == gender
    
    def test_validate_data_valid_cases(self):
        """Test de validación con casos válidos"""
        valid_cases = [
            ("male", 1.80, 80.0, 25),
            ("female", 1.60, 55.5, 30),
            ("masculino", 2.0, 100.0, 18),
            ("femenino", 1.50, 45.0, 65),
        ]
        
        for gender, height, weight, age in valid_cases:
            user = UserData(gender, height, weight, age)
            assert user.validate_data() == True
    
    def test_validate_data_invalid_gender(self):
        """Test de validación con géneros inválidos"""
        invalid_genders = ["", "unknown", "N/A", "hombre", "mujer", 123, None]
        
        for gender in invalid_genders:
            user = UserData(gender, 1.70, 70.0, 25)
            assert user.validate_data() == False
    
    def test_validate_data_invalid_height(self):
        """Test de validación con alturas inválidas"""
        invalid_heights = [0, -1.70, -0.1, "1.70", None]
        
        for height in invalid_heights:
            user = UserData("male", height, 70.0, 25)
            assert user.validate_data() == False
    
    def test_validate_data_invalid_weight(self):
        """Test de validación con pesos inválidos"""
        invalid_weights = [0, -70.0, -0.1, "70", None]
        
        for weight in invalid_weights:
            user = UserData("female", 1.70, weight, 25)
            assert user.validate_data() == False
    
    def test_validate_data_invalid_age(self):
        """Test de validación con edades inválidas"""
        invalid_ages = [0, -25, -1, 25.5, "25", None]
        
        for age in invalid_ages:
            user = UserData("other", 1.70, 70.0, age)
            assert user.validate_data() == False
    
    def test_validate_data_missing_fields(self):
        """Test de validación con campos faltantes"""
        user = UserData("", 1.70, 70.0, 25)
        assert user.validate_data() == False
        
        user = UserData(None, 1.70, 70.0, 25)
        assert user.validate_data() == False
    
    def test_to_dict(self):
        """Test de conversión a diccionario"""
        user = UserData("masculino", 1.75, 70.5, 25)
        expected_dict = {
            'gender': 'masculino',
            'height': 1.75,
            'weight': 70.5,
            'age': 25
        }
        assert user.to_dict() == expected_dict
    
    def test_edge_cases_extreme_values(self):
        """Test con valores extremos pero técnicamente válidos"""
        # Altura muy baja pero positiva
        user = UserData("male", 0.01, 70.0, 25)
        assert user.validate_data() == True
        
        # Altura muy alta
        user = UserData("female", 3.0, 70.0, 25)
        assert user.validate_data() == True
        
        # Peso muy bajo pero positivo
        user = UserData("other", 1.70, 0.1, 25)
        assert user.validate_data() == True
        
        # Peso muy alto
        user = UserData("masculino", 1.70, 500.0, 25)
        assert user.validate_data() == True
        
        # Edad muy alta
        user = UserData("femenino", 1.70, 70.0, 150)
        assert user.validate_data() == True
    
    def test_data_types_consistency(self):
        """Test de consistencia de tipos de datos"""
        user = UserData("male", 1.75, 70, 25)  # weight como int
        assert isinstance(user.weight, int)
        assert user.validate_data() == True
        
        user = UserData("female", 2, 70.5, 25)  # height como int
        assert isinstance(user.height, int)
        assert user.validate_data() == True 