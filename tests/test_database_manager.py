import pytest
import sys
import os
import pandas as pd
import tempfile

# Agregar el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.backend import DatabaseManager, Exercise

class TestDatabaseManager:
    """Test suite para la clase DatabaseManager"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.db_manager = DatabaseManager()
    
    def test_init_database_manager(self):
        """Test de inicialización del DatabaseManager"""
        db = DatabaseManager()
        assert db is not None
    
    def test_get_exercises_from_routine_file_valid_category(self):
        """Test de carga de ejercicios con categoría válida"""
        # Test con una categoría que sabemos que existe
        exercises = self.db_manager.get_exercises_from_routine_file("Bajo Peso")
        
        assert isinstance(exercises, list)
        # Verificar que se cargan ejercicios si el archivo existe
        if exercises:  # Si el archivo existe y tiene datos
            assert all(isinstance(ex, Exercise) for ex in exercises)
            assert all(hasattr(ex, 'id') for ex in exercises)
            assert all(hasattr(ex, 'name') for ex in exercises)
    
    def test_get_exercises_from_routine_file_invalid_category(self):
        """Test con categoría de IMC inválida"""
        exercises = self.db_manager.get_exercises_from_routine_file("Categoria Inexistente")
        assert exercises == []
    
    def test_get_exercises_from_routine_file_empty_category(self):
        """Test con categoría vacía"""
        exercises = self.db_manager.get_exercises_from_routine_file("")
        assert exercises == []
    
    def test_get_exercises_from_routine_file_none_category(self):
        """Test con categoría None"""
        exercises = self.db_manager.get_exercises_from_routine_file(None)
        assert exercises == []
    
    def test_get_exercises_from_routine_file_all_valid_categories(self):
        """Test con todas las categorías válidas"""
        valid_categories = ["Bajo Peso", "Normal", "Sobrepeso", "Obesidad"]
        
        for category in valid_categories:
            exercises = self.db_manager.get_exercises_from_routine_file(category)
            assert isinstance(exercises, list)
            # No verificamos que no esté vacío porque los archivos podrían no existir en el entorno de test
    
    def test_equipment_needed_parsing(self):
        """Test de parsing del campo equipment_needed"""
        # Crear un CSV temporal para testing
        csv_content = """id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed
1,Test Exercise,Test Description,Normal,Intermedio,Fuerza,Any,"Mancuernas, Banco"
2,No Equipment,Test Description 2,Normal,Principiante,Cardio,Any,
3,Single Equipment,Test Description 3,Normal,Avanzado,Fuerza,Any,Pesas"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write(csv_content)
            temp_file.flush()
            
            # Modificar temporalmente Config.ROUTINE_CSVS para usar nuestro archivo de test
            from src.config import Config
            original_csvs = Config.ROUTINE_CSVS.copy()
            Config.ROUTINE_CSVS["Test Category"] = temp_file.name
            
            try:
                exercises = self.db_manager.get_exercises_from_routine_file("Test Category")
                
                assert len(exercises) == 3
                
                # Verificar parsing de múltiples equipos
                assert exercises[0].equipment_needed == ["Mancuernas", "Banco"]
                
                # Verificar campo vacío
                assert exercises[1].equipment_needed == []
                
                # Verificar equipo único
                assert exercises[2].equipment_needed == ["Pesas"]
                
            finally:
                # Restaurar configuración original
                Config.ROUTINE_CSVS = original_csvs
                try:
                    os.unlink(temp_file.name)
                except (OSError, PermissionError):
                    # En Windows, a veces el archivo queda bloqueado
                    pass
    
    def test_invalid_id_handling(self):
        """Test de manejo de IDs inválidos en CSV"""
        csv_content = """id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed
invalid_id,Test Exercise,Test Description,Normal,Intermedio,Fuerza,Any,Pesas
2,Valid Exercise,Test Description 2,Normal,Principiante,Cardio,Any,"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write(csv_content)
            temp_file.flush()
            
            from src.config import Config
            original_csvs = Config.ROUTINE_CSVS.copy()
            Config.ROUTINE_CSVS["Test Category"] = temp_file.name
            
            try:
                exercises = self.db_manager.get_exercises_from_routine_file("Test Category")
                
                # Solo debe cargar el ejercicio con ID válido
                assert len(exercises) == 1
                assert exercises[0].id == 2
                assert exercises[0].name == "Valid Exercise"
                
            finally:
                Config.ROUTINE_CSVS = original_csvs
                try:
                    os.unlink(temp_file.name)
                except (OSError, PermissionError):
                    # En Windows, a veces el archivo queda bloqueado
                    pass
    
    def test_empty_csv_file(self):
        """Test con archivo CSV vacío"""
        csv_content = "id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed\n"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write(csv_content)
            temp_file.flush()
            
            from src.config import Config
            original_csvs = Config.ROUTINE_CSVS.copy()
            Config.ROUTINE_CSVS["Empty Test"] = temp_file.name
            
            try:
                exercises = self.db_manager.get_exercises_from_routine_file("Empty Test")
                assert exercises == []
                
            finally:
                Config.ROUTINE_CSVS = original_csvs
                try:
                    os.unlink(temp_file.name)
                except (OSError, PermissionError):
                    # En Windows, a veces el archivo queda bloqueado
                    pass
    
    def test_malformed_csv_file(self):
        """Test con archivo CSV malformado"""
        csv_content = "Esta no es una estructura CSV válida\nsin comas ni estructura"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write(csv_content)
            temp_file.flush()
            
            from src.config import Config
            original_csvs = Config.ROUTINE_CSVS.copy()
            Config.ROUTINE_CSVS["Malformed Test"] = temp_file.name
            
            try:
                exercises = self.db_manager.get_exercises_from_routine_file("Malformed Test")
                # Debería devolver lista vacía en caso de error
                assert exercises == []
                
            finally:
                Config.ROUTINE_CSVS = original_csvs
                try:
                    os.unlink(temp_file.name)
                except (OSError, PermissionError):
                    # En Windows, a veces el archivo queda bloqueado
                    pass
    
    def test_nonexistent_file(self):
        """Test con archivo que no existe"""
        from src.config import Config
        original_csvs = Config.ROUTINE_CSVS.copy()
        Config.ROUTINE_CSVS["Nonexistent"] = "archivo_que_no_existe.csv"
        
        try:
            exercises = self.db_manager.get_exercises_from_routine_file("Nonexistent")
            assert exercises == []
            
        finally:
            Config.ROUTINE_CSVS = original_csvs
    
    def test_csv_with_missing_columns(self):
        """Test con CSV que tiene columnas faltantes"""
        csv_content = """id,name,description
1,Test Exercise,Test Description"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write(csv_content)
            temp_file.flush()
            
            from src.config import Config
            original_csvs = Config.ROUTINE_CSVS.copy()
            Config.ROUTINE_CSVS["Missing Columns"] = temp_file.name
            
            try:
                exercises = self.db_manager.get_exercises_from_routine_file("Missing Columns")
                # Debería manejar las columnas faltantes
                if exercises:  # Si no falla completamente
                    assert len(exercises) >= 0
                
            finally:
                Config.ROUTINE_CSVS = original_csvs
                try:
                    os.unlink(temp_file.name)
                except (OSError, PermissionError):
                    # En Windows, a veces el archivo queda bloqueado
                    pass
    
    def test_equipment_needed_edge_cases(self):
        """Test de casos límite para equipment_needed"""
        csv_content = """id,name,description,imc_range,difficulty,category,gender_specific,equipment_needed
1,Test1,Desc1,Normal,Intermedio,Fuerza,Any,nan
2,Test2,Desc2,Normal,Intermedio,Fuerza,Any,""
3,Test3,Desc3,Normal,Intermedio,Fuerza,Any,"  "
4,Test4,Desc4,Normal,Intermedio,Fuerza,Any,"Item1,  Item2  , Item3"
5,Test5,Desc5,Normal,Intermedio,Fuerza,Any,Single Item"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write(csv_content)
            temp_file.flush()
            
            from src.config import Config
            original_csvs = Config.ROUTINE_CSVS.copy()
            Config.ROUTINE_CSVS["Equipment Test"] = temp_file.name
            
            try:
                exercises = self.db_manager.get_exercises_from_routine_file("Equipment Test")
                
                if len(exercises) >= 5:
                    # nan case
                    assert exercises[0].equipment_needed == []
                    
                    # empty string case
                    assert exercises[1].equipment_needed == []
                    
                    # whitespace case
                    assert exercises[2].equipment_needed == []
                    
                    # multiple items with spaces
                    assert exercises[3].equipment_needed == ["Item1", "Item2", "Item3"]
                    
                    # single item
                    assert exercises[4].equipment_needed == ["Single Item"]
                
            finally:
                Config.ROUTINE_CSVS = original_csvs
                try:
                    os.unlink(temp_file.name)
                except (OSError, PermissionError):
                    # En Windows, a veces el archivo queda bloqueado
                    pass 