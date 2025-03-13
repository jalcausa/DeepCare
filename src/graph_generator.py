import re
import matplotlib.pyplot as plt
import google.generativeai as genai
from config import API_KEY, GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

# Seleccionar el modelo
model = genai.GenerativeModel("gemini-2.0-flash")

def generar_codigo_grafico(peticion):

    
    prompt = f"""Genera un código en Python que grafique datos.  
	La petición del usuario es: {peticion}.  

	Usa pandas para leer el archivo. Ten en cuenta que puede haber filas con columnas sin valores y debes manejarlo correctamente. Usa `na_values=[""]` y `keep_default_na=False` para tratar los valores vacíos correctamente.  

	Asegúrate de que la columna de ID de paciente se llame `PacienteID` y que `Fecha` y `Hora` se combinen en una nueva columna `fecha_hora` con `pd.to_datetime()`.
    
    Si alguna línea tiene más campos de los que debería considerala no válida y no la incluyas en el gráfico.
	Usa seaborn/matplotlib para graficar los datos.  

	Asegúrate de que el código sea ejecutable y claro.  
	No incluyas explicaciones, solo el código. La primera línea debe empezar con `import`.  

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


# Ejemplo de uso:
peticion_usuario = input("¿Qué quieres visualizar?\n")
codigo_generado = generar_codigo_grafico(peticion_usuario)
codigo_limpio = limpiar_codigo(codigo_generado)

#print("Código generado:\n", codigo_generado)
#print("Código limpio:\n ", codigo_limpio)

ejecutar_codigo(codigo_limpio)

