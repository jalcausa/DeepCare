from secret import API_KEY

from pathlib import Path
import openai # openai v1.0.0+
import pandas as pd
import io
import os


# Obtiene la ruta del directorio donde está el script en ejecución
# __file__ es una variable especial que contiene la ruta absoluta del archivo que está siendo ejecutado.

directorio = Path(__file__).parent  # Si el script está en el mismo directorio que los CSV

# Si los CSV están en una carpeta dentro del repositorio, por ejemplo "data"
# directorio_csv = directorio / "data"



def atributosArchivos(directorio):
	columnas = {}
	for archivo in os.listdir(directorio):        # archivo es el nombre de cada archivo
		if archivo.endswith(".csv"):
			ruta_archivo = os.path.join(directorio, archivo)
			df = pd.read_csv(ruta_archivo, nrows=0)
			columnas[archivo] = df.columns.tolist()     # Cada columna de un DataFrame tiene un nombre (que es una etiqueta) y puedes acceder a una columna específica utilizando ese nombre.
	return columnas


pruebaColumnas = atributosArchivos(directorio)

# print(pruebaColumnas)

#{'nombre archivo': [lista], 'nombre archivo2...'}

texto = str(pruebaColumnas)
#print(texto)


# Simulamos la lectura del archivo CSV
with open("resumen_procedimientos.csv", "r", encoding="utf-8") as f:
    buffer = io.StringIO(f.read())

# Cargar el CSV en un DataFrame desde el buffer
df = pd.read_csv(buffer)
#print(df.to_string)

client = openai.OpenAI(api_key=API_KEY,base_url="https://litellm.dccp.pbu.dedalus.com") # set proxy to base_url
# request sent to model set on litellm proxy, `litellm --model`


def newPrompt(petition):
	response = client.chat.completions.create(model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0", messages = [
	    {
	        "role": "user",
	        "content": petition + "Los atributos que contiene cada archivo vienen en el siguiente diccionario " + str(pruebaColumnas)
	    }
	])
	#  "content": f"Por favor, resume los siguientes datos médicos del paciente:\n\n{document}\n\nResumen:"
	# print(response)
	return(response)

petition = input("Introduzca una pregunta:\n")
consulta = newPrompt(petition)
print(consulta.choices[0].message.content)