from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from models import db, User, Conversation, Message, Chart
from graph_generator import GraphicAgent
from main import ProcesadorInput

matplotlib.use('Agg')  # Para evitar errores con entornos gráficos en servidores sin GUI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deepcare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()

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
    user_id = data.get('user_id', '')
    conversation_id = data.get('conversation_id', '')
    # Aquí realizamos el procesamiento del mensaje del usuario
    return agentProcesor.procesarInput(mensaje_usuario, user_id, conversation_id)

# ... (rutas de registro y login existentes)

@app.route('/users/<username>/conversations', methods=['GET'])
def get_user_conversations(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    conversations = Conversation.query.filter_by(user_id=user.id).order_by(Conversation.created_at.desc()).all()
    
    resultado = [
        {
            "id": conv.id,
            "created_at": conv.created_at.isoformat(),
            "preview": conv.messages[-1].content[:50] + "..." if conv.messages else "Nueva conversación"
        }
        for conv in conversations
    ]
    
    return jsonify(resultado), 200

@app.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({"error": "Conversación no encontrada"}), 404
    
    messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.timestamp.asc()).all()
    charts = Chart.query.filter_by(conversation_id=conversation.id).all()
    
    resultado = []
    for msg in messages:
        resultado.append({
            "role": msg.sender,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat()
        })
    
    for chart in charts:
        resultado.append({
            "role": "bot",
            "content": f'<img src="data:image/png;base64,{chart.image_base64}" class="chart-image" />',
            "timestamp": chart.created_at.isoformat()
        })
    
    return jsonify(resultado), 200

# Ruta para registrar un nuevo usuario
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    if not username or not password:
        return jsonify({"error": "El nombre de usuario y la contraseña son obligatorios"}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"error": "El usuario ya existe"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201

# Ruta para iniciar sesión (solo para validar usuario y contraseña)
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        return jsonify({"id": user.id, "username": user.username})  # <-- Devolver también el ID
    
    return jsonify({"error": "Credenciales incorrectas"}), 401

# Ruta para crear una nueva conversación
@app.route('/start_conversation', methods=['POST'])
def start_conversation():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "Se requiere el ID del usuario"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    new_conversation = Conversation(user_id=user.id)
    db.session.add(new_conversation)
    db.session.commit()

    return jsonify({"message": "Conversación iniciada", "conversation_id": new_conversation.id}), 201

# Ruta para enviar un mensaje dentro de una conversación
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    conversation_id = data.get('conversation_id')
    sender = data.get('sender')  # Puede ser 'user' o 'bot'
    content = data.get('content')

    if not conversation_id or not sender or not content:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({"error": "Conversación no encontrada"}), 404

    new_message = Message(conversation_id=conversation.id, sender=sender, content=content)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Mensaje enviado exitosamente"}), 201



# Ruta para generar y guardar el gráfico en base64
@app.route('/guardar_grafico', methods=['POST'])
def guardar_grafico():
    data = request.get_json()
    img_base64 = data.get('image_base64')
    nombre = data.get('nombre', 'grafico_generado')
    user_id = data.get('user_id')
    conversation_id = data.get('conversation_id')
    
    # if not peticion:
    #     return jsonify({"error": "No se recibió la petición para el gráfico"}), 400
    
    if not user_id or not conversation_id:
        return jsonify({"error": "Faltan user_id o conversation_id"}), 400

    # Instanciar el agente gráfico
    # agente = GraphicAgent()
    # # Generar código para el gráfico
    # codigo_generado = agente.generar_codigo(peticion)
    # img_base64 = agente.ejecutar_codigo(codigo_generado, user_id, conversation_id)
    
    # if img_base64 is None:
    #     return jsonify({"error": "Error al generar el gráfico"}), 500
    
    # Crear un nuevo registro en la base de datos con la imagen en base64
    nuevo_grafico = Chart(name=nombre, image_base64=img_base64, user_id=user_id, conversation_id=conversation_id)
    db.session.add(nuevo_grafico)
    db.session.commit()
    
    return jsonify({
        "message": "Gráfico guardado exitosamente",
        "chart_id": nuevo_grafico.id,
        "nombre": nuevo_grafico.name
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
