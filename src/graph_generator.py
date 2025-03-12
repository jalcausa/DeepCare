import re
import matplotlib.pyplot as plt
import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv(override=True)
API_KEY = os.getenv("API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Seleccionar el modelo
model = genai.GenerativeModel("gemini-2.0-flash")

def generar_codigo_grafico(peticion):
    """Genera un código en Python basado en la petición del usuario usando Gemini"""
    
    prompt = f"""Genera un código en Python que grafique datos.
    La petición del usuario es: {peticion}.
    
    Usa pandas para leer el archivo y seaborn/matplotlib para graficar.
    Asegúrate de que el código sea ejecutable y claro.
    No incluyas explicaciones, solo el código. La primera línea debe empezar con import.
    """

    respuesta = model.generate_content(prompt)
    return respuesta.text  # Extraer solo el código generado


def limpiar_codigo(codigo):
    """Elimina etiquetas de código Markdown como ```python y ```"""
    return re.sub(r"```[a-z]*\n|```", "", codigo).strip()


def ejecutar_codigo(codigo):
    """Ejecuta el código generado dinámicamente"""
    
    # Definir un espacio de ejecución seguro
    entorno_seguro = {}

    try:
        exec(codigo, entorno_seguro)
        print("Código ejecutado exitosamente.")
    except Exception as e:
        print(f"Error al ejecutar el código: {e}")

'''
# Ejemplo de uso:
peticion_usuario = input("¿Qué quieres visualizar?")
codigo_generado = generar_codigo_grafico(peticion_usuario)
codigo_limpio = limpiar_codigo(codigo_generado)

print("Código generado:\n", codigo_generado)
print("Código limpio:\n ", codigo_limpio)

ejecutar_codigo(codigo_limpio)
'''