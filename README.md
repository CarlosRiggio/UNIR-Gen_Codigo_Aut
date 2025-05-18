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
## Diagrama de clases
La estructura que tenemos pensada para el proyecto sería la siguiente:
- main.py: este será el programa que se ejecutará y llamará al resto de programas para desplegar la interfaz gráfica y las demás funcionalidades del sistema. Como salida imprimirá por terminal la IP y puerto en la que se lanza nuestra web.
- frontend.py: en este archivo se definen todas las funciones relacionadas con el diseño gráfico de la interfaz gráfica del sistema. 
- backend.py: en este archivo se define la lógica de nuestro sistema, incluyendo las siguientes funcionalidades:
- Calculadora de IMC: en base a los datos de sexo, altura, peso y edad introducidos por el usuario, se calcula su IMC.
- Generación de rutina: a partir del IMC calculado, se extrae de la base de datos de ejercicios aquellos que estén indicados para la finalidad del entrenamiento sugerida por el sistema, como podría ser ganancia de masa muscular, pérdida de peso o mantenimiento. 
- Base de datos: como base de datos tendremos 1 archivo CSV, donde estarán las descripciones de los ejercicios a hacer en función del rango del IMC obtenido. Cada ejercicio estará etiquetado en función del rango
