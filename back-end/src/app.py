from flask import Flask, request, jsonify
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from main import ProcesadorInput
from graph_generator import GraphicAgent

app = Flask(__name__)
CORS(app)  # Permite peticiones desde otros orígenes, como tu frontend en localhost:5173

# Ejemplo de endpoint /chat
# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.get_json()
#     if not data or "mensaje" not in data:
#         return jsonify({"error": "No se envió el mensaje"}), 400

#     mensaje_usuario = data["mensaje"]
#     # Aquí realizamos el procesamiento del mensaje del usuario
#     client = procesarInput()
#     respuesta_modelo = client.procesarInput(mensaje_usuario)
#     # 
#     # Si tenemos que enviar además una imagen, podemos enviar una URL o base64 string
#     return jsonify({"respuesta": respuesta_modelo})

agentProcesor = ProcesadorInput()

# Ejemplo de endpoint /generar_grafico
agentProcesor = ProcesadorInput()
@app.route('/chat', methods=['POST'])
def chat():
    # # Extraer la petición del cuerpo de la solicitud JSON
    # data = request.get_json()
    # peticion = data.get('peticion', '')  # Si no hay "peticion", se asigna un valor por defecto vacío

    # if not peticion:
    #     return jsonify({"error": "No se recibió una petición válida"}), 400
    data = request.get_json()
    mensaje_usuario = data.get('peticion', '')
    
    # Aquí realizamos el procesamiento del mensaje del usuario
    return agentProcesor.procesarInput(mensaje_usuario)

if __name__ == '__main__':
    # Ejecuta el servidor en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
