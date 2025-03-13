import re
import matplotlib.pyplot as plt
import google.generativeai as genai
from config import API_KEY, GEMINI_API_KEY


class GraphicAgent:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
    
    def generar_codigo_grafico(self, peticion, archivo_csv=None):
        """Genera código Python para graficar según la petición del usuario, opcionalmente usando un archivo CSV."""
        prompt = f"""Genera un código en Python que grafique datos.
        La petición del usuario es: {peticion}.
        Si se proporciona un archivo CSV, lee los datos con pandas y usa seaborn/matplotlib para graficar.
        Asegúrate de que el código sea ejecutable y claro.
        No incluyas explicaciones, solo el código. La primera línea debe empezar con import.
        """
        
        if archivo_csv:
            prompt += f"""
            El archivo CSV a utilizar es: {archivo_csv}. 
            Asegúrate de incluir el código para leer este archivo y seleccionar las columnas adecuadas.
            """
        
        respuesta = self.model.generate_content(prompt)
        return respuesta.text  # Extraer solo el código generado
    

    def limpiar_codigo(self, codigo):
        """Elimina etiquetas de código Markdown como ```python y ```"""
        return re.sub(r"```[a-z]*\n|```", "", codigo).strip()

    def ejecutar_codigo(self, codigo):
        """Ejecuta el código generado dinámicamente en un entorno seguro."""
        entorno_seguro = {}
        try:
            codigo = self.limpiar_codigo(codigo)
            exec(codigo, entorno_seguro)
            print("Código ejecutado exitosamente.")
        except Exception as e:
            print(f"Error al ejecutar el código: {e}")
