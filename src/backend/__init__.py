"""
Módulo backend del generador de rutinas de ejercicio.
Contiene todas las clases de dominio y lógica de negocio.
"""

from .models import UserData, Exercise, WorkoutPlan
from .calculator import IMCCalculator
from .database import DatabaseManager
from .generator import WorkoutGenerator

__all__ = [
    'UserData', 'Exercise', 'WorkoutPlan',
    'IMCCalculator', 'DatabaseManager', 'WorkoutGenerator'
] 