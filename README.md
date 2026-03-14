## API de Análisis de Sentimientos

 ### 📌 Descripción
API Flask para análisis de sentimientos que combina Machine Learning con reglas heurísticas avanzadas para clasificar texto como POSITIVO o NEGATIVO. El sistema está optimizado para entender expresiones complejas, negaciones y lenguaje informal.

### 📊 Arquitectura del Modelo
#### Componentes:
 * Vectorizador: TF-IDF con n-grams (1,2)

 * Modelo ML: Clasificador (probablemente SVM o Logistic Regression)

 * Pipeline: Preprocesamiento + clasificación

### 🚀 Características Principales
 * ✅ Predicción basada en ML con modelo pre-entrenado

 * ✅ Reglas heurísticas para casos específicos

 * ✅ Procesamiento avanzado de texto (limpieza, negaciones, traducción semántica)

 * ✅ API RESTful con endpoint /predict

 * ✅ Compatibilidad con clientes Java y otras tecnologías

 * ✅ Umbral configurable de confianza



### 🔍 Lógica de Procesamiento
#### Flujo de análisis:
 * 1 Limpieza inicial: Normalización de texto, eliminación de acentos
 * 2 Traducción semántica: Conversión de términos de productos a términos de cine
 * 3 Detección de negaciones: Unión de palabras negadas (ej: "no_bueno")
 * 4 Aplicación de reglas: 
   * Reglas positivas explícitas
   * Reglas negativas duras
   * Detección de palabras clave reforzadoras
 * 5 Predicción ML: Uso del modelo pre-entrenado
 * 6 Ajuste final: Modificación de probabilidades basada en tokens especiales

#### Tokens especiales:
  * NEGATIVO_FUERTE: Aumenta probabilidad negativa (+0.35)
  * POSITIVO_SUAVE: Aumenta probabilidad positiva (+0.10)
  * NEGATIVO_SUAVE: Fuerza clasificación negativa

### 📂 Estructura del Proyecto
````
IA-sentimentAPI/
├── model/
│   ├── modelo.joblib       # Modelo ML entrenado
│   └── vectorizador.joblib # Vectorizador para texto
├── app.py                  # Aplicación Flask principal
├── nlp_utils.py            # Funciones de procesamiento de lenguaje
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
````
### 🔧 Prerrequisitos
 #### Para Linux/Mac:

````
# Python 3.8 o superior
python3 --version

# pip actualizado
pip3 install --upgrade pip

# virtualenv (opcional pero recomendado)
pip3 install virtualenv

````

#### Para Windows:
````
# Python 3.8 o superior
python --version

# pip actualizado
python -m pip install --upgrade pip

# virtualenv
pip install virtualenv
````

### 📥 Instalación
### Opción 1: Clonar y configurar (Recomendada)
#### Linux/Mac:
````
# 1. Clonar repositorio
git clone https://github.com/rlipac31/API-PYTHON_sentimentAPI.git
cd API-PYTHON_sentimentAPI

# 2. Crear entorno virtual
python3 -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
````
#### Windows:
````
:: 1. Clonar repositorio
git clone <tu-repositorio-url>
cd proyecto-sentimientos

:: 2. Crear entorno virtual
python -m venv venv

:: 3. Activar entorno virtual
venv\Scripts\activate

:: 4. Instalar dependencias
pip install -r requirements.txt
````
### Opción 2: Instalación directa
````
# Instalar Flask y dependencias principales
pip install flask joblib scikit-learn pandas gunicorn
````
### 🚀 Ejecución Local
#### Linux/Mac:
````
# Asegúrate de estar en el directorio del proyecto
cd proyecto-sentimientos

# Activar entorno virtual (si usaste virtualenv)
source venv/bin/activate

# Ejecutar la aplicación
python3 app.py

# O con puerto específico
PORT=5000 python3 app.py
````

#### windows:
````
:: Navegar al directorio del proyecto
cd proyecto-sentimientos

:: Activar entorno virtual (si usaste virtualenv)
venv\Scripts\activate

:: Ejecutar la aplicación
python app.py

:: O con puerto específico (en PowerShell)
$env:PORT=5000; python app.py
````
### Verificar que el servidor esté funcionando:
````
# La API estará disponible en:
# http://localhost:8000 (puerto por defecto)
# http://localhost:5000 (si especificaste PORT=5000)
````

### 📡 Endpoints de la API
#### 1. Health Check
````
GET http://localhost:8000/
````
#### Respuesta: 
````
{
"status": "API activa desde huggins Face"
}
````

#### 2. Predicción de Sentimiento
````
POST http://localhost:8000/predict
Content-Type: application/json

{
  "texto": "El producto es excelente, me encantó la calidad"
}
````
#### Respuesta exitosa
````
{
"texto": "El producto es excelente, me encantó la calidad",
"prevision": "POSITIVO",
"probabilidad": 0.92
}
````

#### Respuesta de error:
````
{
  "error": "No se recibió texto"
}
````
