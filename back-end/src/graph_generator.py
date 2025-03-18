import requests
import os
import re
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from config import API_KEY
from data_handler import directorio
from anthropic_api_calls import AnthropicClient

matplotlib.use('Agg')

class GraphicAgent:
    def __init__(self):
        self.client = AnthropicClient()

    def generar_codigo(self, peticion, data=None):
        """Genera código Python para graficar según la petición del usuario, opcionalmente usando un archivo CSV."""
        prompt = f"""Generate Python code to create a chart and, if the user request says so, add the necessary
        code lines to save it as PNG, using the command line:
        fig.savefig("name.png", dpi=300), where "name" is the name that you choose for the file.

        CRITICAL INSTRUCTIONS:  
        1. DO NOT use plt.show()  
        2. Make sure to create a figure with plt.figure()  
        3. Use plt.savefig() to save it to BytesIO  
        4. Include the necessary imports  
        5. Do not include explanations, only code. The first line must start with import.  
        6. If data is included, use ONLY that data; do not attempt to access non-existent files.
        User request: {peticion}
        """  

        if data:
            prompt += f"""
            The data available are: {data}.
            """
        respuesta = self.client.get_response(prompt)
        return respuesta

    def limpiar_codigo(self, codigo):
        """Elimina etiquetas de código Markdown como ```python y ```"""
        return re.sub(r"```[a-z]*\n|```", "", codigo).strip()

    def ejecutar_codigo(self, codigo, user_id, conversation_id):
        """Ejecuta el código generado dinámicamente en un entorno seguro."""
        entorno_seguro = {}
        try:
            codigo = self.limpiar_codigo(codigo)
            exec(codigo, entorno_seguro)
            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png', bbox_inches='tight')
            plt.close()  # Limpiar memoria
            img_buf.seek(0)
            img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
            
            # Enviar el gráfico generado al backend con la relación usuario y conversación
            self.guardar_en_backend(img_base64, user_id, conversation_id)
            
            return img_base64
        except Exception as e:
            print(f"Error al ejecutar el código: {e}")

    def guardar_en_backend(self, img_base64, user_id, conversation_id):
        """Envía el gráfico generado al backend para ser guardado en la base de datos con relación a usuario y conversación."""
        url = 'http://127.0.0.1:5000/guardar_grafico'  # URL del endpoint en Flask
        data = {
            'image_base64': img_base64,
            'nombre': 'grafico_generado',  # Puedes personalizar el nombre aquí
            'user_id': user_id,  # ID del usuario
            'conversation_id': conversation_id  # ID de la conversación
        }
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print("Gráfico guardado en la base de datos correctamente.")
        else:
            print("Error al guardar el gráfico:", response.json())
