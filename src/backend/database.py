"""
Gestor de base de datos y carga de ejercicios desde archivos CSV.
"""

import pandas as pd
import os
from typing import List
from .models import Exercise
from ..config import Config


class DatabaseManager:
    """Gestor de datos para la carga de ejercicios desde archivos CSV."""
    
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
                    lambda x: [item.strip() for item in str(x).split(',') if item.strip()] 
                    if pd.notna(x) and str(x).strip().lower() not in ['', 'nan'] else []
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
                    imc_range=str(row['imc_range']),  # Esta columna podría ser redundante ahora
                    difficulty=str(row['difficulty']),
                    category=str(row['category']),
                    gender_specific=str(row['gender_specific']),  # Podría ser redundante
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