import pytest
import sys
import os

# Agregar el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.backend import IMCCalculator

class TestIMCCalculator:
    """Test suite para la clase IMCCalculator"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.calculator = IMCCalculator()
    
    def test_calculate_imc_normal_cases(self):
        """Test de cálculo de IMC con casos normales"""
        # Casos conocidos para verificar el cálculo
        test_cases = [
            (70.0, 1.75, 22.86),  # Normal
            (50.0, 1.60, 19.53),  # Normal bajo
            (90.0, 1.80, 27.78),  # Sobrepeso
            (45.0, 1.70, 15.57),  # Bajo peso
            (120.0, 1.75, 39.18), # Obesidad
        ]
        
        for weight, height, expected_imc in test_cases:
            result = self.calculator.calculate_imc(weight, height)
            assert abs(result - expected_imc) < 0.01, f"IMC calculado: {result}, esperado: {expected_imc}"
    
    def test_calculate_imc_precision(self):
        """Test de precisión del cálculo (2 decimales)"""
        result = self.calculator.calculate_imc(70.123, 1.756)
        assert isinstance(result, float)
        # Verificar que tiene máximo 2 decimales
        assert len(str(result).split('.')[-1]) <= 2
    
    def test_calculate_imc_zero_height_error(self):
        """Test de error cuando la altura es cero"""
        with pytest.raises(ValueError, match="La altura debe ser mayor que cero"):
            self.calculator.calculate_imc(70.0, 0)
    
    def test_calculate_imc_negative_height_error(self):
        """Test de error cuando la altura es negativa"""
        with pytest.raises(ValueError, match="La altura debe ser mayor que cero"):
            self.calculator.calculate_imc(70.0, -1.75)
    
    def test_get_imc_category_bajo_peso(self):
        """Test de categorización: Bajo Peso"""
        bajo_peso_values = [15.0, 17.5, 18.4]
        for imc in bajo_peso_values:
            assert self.calculator.get_imc_category(imc) == "Bajo Peso"
    
    def test_get_imc_category_normal(self):
        """Test de categorización: Normal"""
        normal_values = [18.5, 20.0, 22.5, 24.9]
        for imc in normal_values:
            assert self.calculator.get_imc_category(imc) == "Normal"
    
    def test_get_imc_category_sobrepeso(self):
        """Test de categorización: Sobrepeso"""
        sobrepeso_values = [25.0, 27.5, 29.9]
        for imc in sobrepeso_values:
            assert self.calculator.get_imc_category(imc) == "Sobrepeso"
    
    def test_get_imc_category_obesidad(self):
        """Test de categorización: Obesidad"""
        obesidad_values = [30.0, 35.0, 40.0, 50.0]
        for imc in obesidad_values:
            assert self.calculator.get_imc_category(imc) == "Obesidad"
    
    def test_get_imc_category_boundary_values(self):
        """Test de valores límite de categorías"""
        # Valores exactos en los límites
        assert self.calculator.get_imc_category(18.49) == "Bajo Peso"
        assert self.calculator.get_imc_category(18.5) == "Normal"
        assert self.calculator.get_imc_category(24.9) == "Normal"
        assert self.calculator.get_imc_category(25.0) == "Sobrepeso"
        assert self.calculator.get_imc_category(29.9) == "Sobrepeso"
        assert self.calculator.get_imc_category(30.0) == "Obesidad"
    
    def test_determine_training_goal_mapping(self):
        """Test de mapeo de IMC a objetivos de entrenamiento"""
        test_cases = [
            (15.0, "Ganancia de Masa Muscular"),  # Bajo Peso
            (22.0, "Mantenimiento y Bienestar General"),  # Normal
            (27.0, "Pérdida de Peso"),  # Sobrepeso
            (35.0, "Pérdida de Peso Progresiva y Salud"),  # Obesidad
        ]
        
        for imc, expected_goal in test_cases:
            result = self.calculator.determine_training_goal(imc)
            assert result == expected_goal
    
    def test_get_all_training_goals_with_imc_categories(self):
        """Test del mapeo completo de objetivos y categorías"""
        mapping = self.calculator.get_all_training_goals_with_imc_categories()
        
        expected_mapping = {
            "Ganancia de Masa Muscular": "Bajo Peso",
            "Mantenimiento y Bienestar General": "Normal",
            "Pérdida de Peso": "Sobrepeso",
            "Pérdida de Peso Progresiva y Salud": "Obesidad"
        }
        
        assert mapping == expected_mapping
        assert len(mapping) == 4
    
    def test_calculate_imc_extreme_values(self):
        """Test con valores extremos pero válidos"""
        # Valores muy bajos
        result = self.calculator.calculate_imc(1.0, 2.0)
        assert result == 0.25
        
        # Valores muy altos
        result = self.calculator.calculate_imc(500.0, 1.5)
        assert result == 222.22
    
    def test_consistency_between_methods(self):
        """Test de consistencia entre métodos"""
        test_imcs = [15.0, 20.0, 27.0, 35.0]
        
        for imc in test_imcs:
            category = self.calculator.get_imc_category(imc)
            goal = self.calculator.determine_training_goal(imc)
            mapping = self.calculator.get_all_training_goals_with_imc_categories()
            
            # Verificar que la categoría y el objetivo sean consistentes
            assert goal in mapping
            assert mapping[goal] == category
    
    def test_threshold_constants_consistency(self):
        """Test de consistencia de las constantes de umbral"""
        calc = self.calculator
        
        # Verificar que los umbrales son lógicos
        assert calc.UNDERWEIGHT_THRESHOLD > 0
        assert calc.NORMAL_THRESHOLD_LOWER == calc.UNDERWEIGHT_THRESHOLD
        assert calc.NORMAL_THRESHOLD_UPPER > calc.NORMAL_THRESHOLD_LOWER
        assert calc.OVERWEIGHT_THRESHOLD_LOWER > calc.NORMAL_THRESHOLD_UPPER
        assert calc.OVERWEIGHT_THRESHOLD_UPPER > calc.OVERWEIGHT_THRESHOLD_LOWER
    
    def test_imc_category_edge_case_floating_point(self):
        """Test de casos límite con precisión de punto flotante"""
        # Casos que podrían causar problemas de precisión
        edge_cases = [18.50000001, 24.99999999, 25.00000001, 29.99999999]
        
        for imc in edge_cases:
            category = self.calculator.get_imc_category(imc)
            assert category in ["Bajo Peso", "Normal", "Sobrepeso", "Obesidad"] 