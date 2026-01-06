from flask import Flask, request, jsonify
import joblib

# proyecto corriendo desde local, en el futuro se hara desde colap y con Ngrock

# Intentamos cargar los archivos que descargaste de Colab
try:
    modelo = joblib.load('modelo_logistic_sentimiento_v3.joblib') #solicitar modelo al equpipo de data
    vectorizador = joblib.load('vectorizador_tfidf_v3.joblib')#solicitar modelo al equipo de data
    print("✅ Modelo y vectorizador cargados con éxito desde la carpeta local.")
except Exception as e:
    print(f"❌ Error: Asegúrate de que los archivos .pkl estén en esta carpeta. {e}")

app = Flask(__name__)

@app.route('/sentiment', methods=['POST'])
def predict():
    data = request.json
    # Recibimos 'texto' desde tu lista de Java
    texto_usuario = data.get('texto', '')

    if not texto_usuario:
        return jsonify({"error": "No se recibió texto"}), 400

    # Procesar con la IA local
    texto_vectorizado = vectorizador.transform([texto_usuario])
    prediccion = modelo.predict(texto_vectorizado)[0]
    
    # Obtener probabilidad
    probabilidades = modelo.predict_proba(texto_vectorizado)
    probabilidad_max = round(float(max(probabilidades[0])), 2)

    print(f"Análisis: '{texto_usuario}' -> {prediccion}")

    return jsonify({
        "texto": texto_usuario,
        "prevision": str(prediccion),
        "probabilidad": probabilidad_max
    })

if __name__ == '__main__':
    print("🚀 API de Inteligencia Artificial activa en http://localhost:4000")
    app.run(host='0.0.0.0', port=4000)