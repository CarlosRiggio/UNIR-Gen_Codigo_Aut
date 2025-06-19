# Desarrollo de un proyecto software mediante IA
Autores:
- Carlos Calvo Moa
- Carlos Riggio Diéguez
- Henar Mariño Bodelón
- Jorge Florentino Serra
## Descripción del proyecto
El objetivo de nuestro proyecto es el desarrollo de una página web para la generación de rutinas de ejercicios personalizadas en función de la condición física del usuario. 
En la interfaz gráfica el cliente introducirá datos como su sexo, altura, el peso y edad. Con esta información, el sistema calculará el Índice de Masa Corporal (IMC).
Según el resultado del IMC, el sistema proporcionará una rutina de ejercicios personalizada. Por ejemplo, si el IMC indica bajo peso, se sugerirá una rutina enfocada en ganar masa muscular. Si el IMC es normal, se recomendará una rutina de mantenimiento y bienestar general. Para valores elevados de IMC, las rutinas estarán orientadas a la pérdida de peso, con ejercicios de cardio y fuerza progresiva.
## Análisis de requisitos
Los requisitos a tener en cuenta son:
- El SO para el que vamos a desarrollar el proyecto será Linux.
- El lenguaje de programación que utilizaremos para las funciones del backend será Python debido a su facilidad de uso. 
- Debido a su compatibilidad con Python, el frontend será implementado usando Flask
- A la hora de la generación de código, se emplearán distintas herramientas de IA generativa, como son Chatgpt, Gemini, Copilot o Claude.
- Para el desarrollo del código se utilizará el IDE de Visual Studio Code o Cursor, ya que ofrecen herramientas colaborativas y de gran utilidad, como LiveShare o chats integrados directamente con los modelos de IA.. 
- Para la implementación de la base de datos utilizaremos un archivo CSV.
## Estructura del proyecto
El proyecto está organizado de la siguiente manera:
- `main.py`: punto de entrada principal que ejecuta la aplicación Flask
- `src/`: directorio principal del código fuente
  - `app.py`: configuración principal de la aplicación Flask
  - `config.py`: configuración de la aplicación
  - `frontend/`: módulo del frontend con controladores web
  - `backend/`: módulo del backend con la lógica de negocio
    - `models.py`: clases de dominio (UserData, Exercise, WorkoutPlan)
    - `calculator.py`: calculadora de IMC
    - `database.py`: gestor de base de datos CSV
    - `generator.py`: generador de rutinas de ejercicio
- `templates/`: plantillas HTML de la interfaz web
- `data/`: archivos CSV con rutinas de ejercicio
- `tests/`: suite completa de tests unitarios y de integración

## Instalación y ejecución

### Prerrequisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Ejecución de la aplicación
Para ejecutar la aplicación web:
```bash
python main.py
```

La aplicación estará disponible en:
- `http://localhost:5000`
- `http://127.0.0.1:5000`
- También se mostrará la IP local de tu red para acceso desde otros dispositivos

### Ejecución de tests
Para ejecutar todos los tests:
```bash
cd tests
python -m pytest -v
```

Para ejecutar tests con cobertura:
```bash
cd tests
python -m pytest --cov=src --cov-report=html -v
```

Para ejecutar un test específico:
```bash
cd tests
python -m pytest test_flask_app.py -v
```

## Funcionalidades
- **Calculadora de IMC**: calcula el Índice de Masa Corporal basado en datos del usuario
- **Generación de rutinas personalizadas**: recomienda ejercicios según el IMC calculado
- **Interfaz web intuitiva**: formulario fácil de usar para introducir datos
- **Base de datos de ejercicios**: rutinas específicas para diferentes objetivos:
  - Ganancia de masa muscular (bajo peso)
  - Mantenimiento y bienestar general (peso normal)
  - Pérdida de peso (sobrepeso)
  - Pérdida de peso progresiva (obesidad)
