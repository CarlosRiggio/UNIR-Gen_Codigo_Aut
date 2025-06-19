#!/usr/bin/env python3
"""
Script para ejecutar todos los tests del proyecto
Desarrollado para la entrega final del banco de pruebas
"""

import sys
import os
import subprocess
import time

def run_tests():
    """Ejecuta todos los tests y genera reportes"""
    
    print("=" * 60)
    print("BANCO DE PRUEBAS - GENERADOR DE RUTINAS DE EJERCICIO")
    print("=" * 60)
    print("Ejecutando tests unitarios e integración...")
    print()
    
    # Lista de archivos de test
    test_files = [
        "test_user_data.py",
        "test_imc_calculator.py", 
        "test_exercise.py",
        "test_database_manager.py",
        "test_workout_plan.py",
        "test_workout_generator.py",
        "test_frontend_controller.py",
        "test_flask_app.py",
        "test_integration.py"
    ]
    
    total_start_time = time.time()
    
    # Verificar que pytest está disponible
    try:
        subprocess.run(['pytest', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: pytest no está instalado.")
        print("Instale pytest con: pip install pytest")
        return False
    
    # Ejecutar tests individuales
    results = {}
    
    for test_file in test_files:
        # Si ejecutamos desde la raiz, buscar en tests/
        test_path = test_file if os.path.exists(test_file) else os.path.join('tests', test_file)
        if os.path.exists(test_path):
            print(f"Ejecutando {test_file}...")
            start_time = time.time()
            
            try:
                result = subprocess.run(
                    ['pytest', test_path, '-v'],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                results[test_file] = {
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'execution_time': execution_time
                }
                
                if result.returncode == 0:
                    print(f"  ✓ PASADO ({execution_time:.2f}s)")
                else:
                    print(f"  ✗ FALLOS ({execution_time:.2f}s)")
                    
            except subprocess.TimeoutExpired:
                print(f"  ⚠ TIMEOUT (>60s)")
                results[test_file] = {
                    'returncode': -1,
                    'stdout': '',
                    'stderr': 'Test timeout',
                    'execution_time': 60
                }
                
        else:
            print(f"  ⚠ {test_file} no encontrado")
    
    # Ejecutar todos los tests juntos
    print("\nEjecutando suite completa...")
    try:
        # Ejecutar todos los tests desde el directorio correcto
        test_dir = 'tests' if os.path.exists('tests') and not os.getcwd().endswith('tests') else '.'
        all_tests_result = subprocess.run(
            ['pytest', test_dir, '-v', '--tb=short'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        total_end_time = time.time()
        total_execution_time = total_end_time - total_start_time
        
        print(f"Suite completa terminada ({total_execution_time:.2f}s)")
        
    except subprocess.TimeoutExpired:
        print("⚠ TIMEOUT en suite completa (>300s)")
        all_tests_result = None
    
    # Generar reporte
    print("\n" + "=" * 60)
    print("REPORTE DE RESULTADOS")
    print("=" * 60)
    
    passed_tests = 0
    failed_tests = 0
    total_time = 0
    
    for test_file, result in results.items():
        status = "PASADO" if result['returncode'] == 0 else "FALLOS"
        print(f"{test_file:<30} {status:<8} ({result['execution_time']:.2f}s)")
        
        if result['returncode'] == 0:
            passed_tests += 1
        else:
            failed_tests += 1
            
        total_time += result['execution_time']
    
    print("-" * 60)
    print(f"Tests ejecutados: {len(results)}")
    print(f"Tests pasados:    {passed_tests}")
    print(f"Tests fallidos:   {failed_tests}")
    print(f"Tiempo total:     {total_time:.2f}s")
    
    # Mostrar detalles de fallos si los hay
    if failed_tests > 0:
        print("\n" + "=" * 60)
        print("DETALLES DE FALLOS")
        print("=" * 60)
        
        for test_file, result in results.items():
            if result['returncode'] != 0:
                print(f"\n--- {test_file} ---")
                if result['stderr']:
                    print("STDERR:")
                    print(result['stderr'])
                if result['stdout']:
                    print("STDOUT:")
                    print(result['stdout'])
    
    # Conclusión
    success_rate = (passed_tests / len(results)) * 100 if results else 0
    
    print("\n" + "=" * 60)
    print("CONCLUSIÓN")
    print("=" * 60)
    print(f"Tasa de éxito: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("✓ Excelente cobertura de testing")
    elif success_rate >= 70:
        print("⚠ Buena cobertura, algunos tests necesitan atención")
    else:
        print("✗ Cobertura insuficiente, revisar implementación")
    
    return failed_tests == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 