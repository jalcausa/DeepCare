from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Permite peticiones desde otros orígenes, como tu frontend en localhost:5173

# Ejemplo de endpoint /chat
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or "mensaje" not in data:
        return jsonify({"error": "No se envió el mensaje"}), 400

    mensaje_usuario = data["mensaje"]

    # Aquí realizamos el procesamiento del mensaje del usuario
    respuesta_modelo = f"Respuesta procesada para: {mensaje_usuario}"

    # Si tenemos que enviar además una imagen, podemos enviar una URL o base64 string
    return jsonify({"respuesta": respuesta_modelo})

if __name__ == '__main__':
    # Ejecuta el servidor en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
