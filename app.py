from flask import Flask, request, jsonify
import os
import joblib
from nlp_utils import limpiar_y_reforzar, quitar_tildes

app = Flask(__name__)

vectorizador = joblib.load("model/vectorizador.joblib")
modelo = joblib.load("model/modelo.joblib")

def calcular_score_manual(texto: str):
    """Retorna un valor positivo si detecta palabras buenas, negativo si malas."""
    positivas = {"premium", "duradero", "excelente", "rapido", "perfecto", "cumple"}
    negativas = {"defectuoso", "pesadilla", "fria", "tarde", "lento", "dormido", "faltaban", "malo","dañado"}
    
    texto_set = set(quitar_tildes(texto).lower().split())
    score = 0
    score += len(texto_set.intersection(positivas)) * 0.2
    score -= len(texto_set.intersection(negativas)) * 0.2
    return score

def analizar_sentimiento(texto_usuario: str):
    texto_proc = limpiar_y_reforzar(texto_usuario)
    
    # 1. Obtener predicción de la IA
    X = vectorizador.transform([texto_proc])
    probabilidades = modelo.predict_proba(X)[0] # [Neg, Pos]
    
    prob_pos_ia = probabilidades[1]
    
    # 2. Obtener ajuste manual (Diccionario de apoyo)
    ajuste = calcular_score_manual(texto_usuario)
    
    # 3. Probabilidad Final Combinada
    # Sumamos el ajuste manual a la probabilidad de la IA
    prob_final = prob_pos_ia + ajuste
    
    # Limitar entre 0 y 1
    prob_final = max(0, min(1, prob_final))

    # 4. Clasificación Final
    if prob_final >= 0.5:
        return "POSITIVO", round(prob_final, 2)
    else:
        return "NEGATIVO", round(1 - prob_final, 2)


# Home
@app.route('/')
def health_check():
    return jsonify({"status": "API activa localmente"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    if not modelo:
        return jsonify({"error": "Modelo no disponible"}), 500

    data = request.json
    texto = data.get('texto', '')
    
    if len(texto) < 3:
        return jsonify({"error": "Texto demasiado corto"}), 400

    try:
        sentimiento, score = analizar_sentimiento(texto)
        return jsonify({
            "texto": texto,
            "prevision": sentimiento,
            "probabilidad": score
        })
  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    #port = int(os.environ.get("PORT", 7860)) # hagic space
    port = int(os.environ.get("PORT", 8000))# solo local
    app.run(host='0.0.0.0', port=port)

