"""
Calculadora de IMC y determinación de objetivos de entrenamiento.
"""

from typing import Dict


class IMCCalculator:
    """Calculadora de Índice de Masa Corporal y objetivos de entrenamiento."""
    
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