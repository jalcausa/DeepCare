import os
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import google.generativeai as genai
from anthropic_api_calls import AnthropicClient
import io
import base64
from config import API_KEY
from data_handler import directorio


class GraphicAgent:
    def __init__(self):
        self.client = AnthropicClient()
    
    # def generar_codigo_grafico(self, peticion, archivo_csv=None):
    #     """Genera código Python para graficar según la petición del usuario, opcionalmente usando un archivo CSV."""
    #     prompt = f"""Genera un código en Python que grafique datos.
    #     La petición del usuario es: {peticion}.
    #     Si se proporciona un archivo CSV, lee los datos con pandas y usa seaborn/matplotlib para graficar.
    #     Asegúrate de que el código sea ejecutable y claro.
    #     No incluyas explicaciones, solo el código. La primera línea debe empezar con import.
    #     """
        
    #     if archivo_csv:
    #         prompt += f"""
    #         El archivo CSV a utilizar es: {archivo_csv}. 
    #         Asegúrate de incluir el código para leer este archivo y seleccionar las columnas adecuadas.
    #         """
    #     respuesta = self.client.get_response(prompt)
    #     return respuesta
    
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

    # def ejecutar_codigo(self, codigo):
    #     """Ejecuta el código generado dinámicamente en un entorno seguro."""
    #     entorno_seguro = {}
    #     try:
    #         codigo = self.limpiar_codigo(codigo)
    #         exec(codigo, entorno_seguro)
    #         print("Código ejecutado exitosamente.")
    #     except Exception as e:
    #         print(f"Error al ejecutar el código: {e}")

    def ejecutar_codigo(self, codigo):
        """Ejecuta el código generado dinámicamente en un entorno seguro."""
        entorno_seguro = {}
        try:
            codigo = self.limpiar_codigo(codigo)
            # print("Código ejecutado:")
            # print(codigo)
            exec(codigo, entorno_seguro)
            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png', bbox_inches='tight')
            plt.close()  # Limpiar memoria
            img_buf.seek(0)
            return base64.b64encode(img_buf.read()).decode('utf-8')
        except Exception as e:
            print(f"Error al ejecutar el código: {e}")        

'''
# Ejemplo de uso
agente_grafico = GraphicAgent()

# Define una petición de ejemplo
peticion = "Genera un gráfico de barras con los datos de glucosa de los diferentes PacienteID"

# Ruta absoluta al archivo CSV
archivo_csv = os.path.join(os.path.abspath("../data"), "resumen_lab_iniciales.csv")

# Generar código gráfico
codigo_generado = agente_grafico.generar_codigo_grafico(peticion, archivo_csv)

# Mostrar el código generado
print("Código generado por el agente gráfico:")
print(codigo_generado)

# Ejecutar el código generado (esto generará el gráfico)
agente_grafico.ejecutar_codigo(codigo_generado)
'''