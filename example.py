from dotenv import load_dotenv
import os
from pathlib import Path
# Hay que instalar openai y pandas
import openai # openai v1.0.0+
import google.generativeai as genai # google-generative-ai
import pandas as pd
import io
import os

load_dotenv(override=True)
API_KEY = os.getenv("API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Obtiene la ruta del directorio donde está el script en ejecución
# __file__ es una variable especial que contiene la ruta absoluta del archivo que está siendo ejecutado.

directorio = Path(__file__).parent/"data"

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
# with open("resumen_procedimientos.csv", "r", encoding="utf-8") as f:
#     buffer = io.StringIO(f.read())

# Cargar el CSV en un DataFrame desde el buffer
#df = pd.read_csv(buffer)
#print(df.to_string)

#client = openai.OpenAI(api_key=API_KEY,base_url="https://litellm.dccp.pbu.dedalus.com") # set proxy to base_url
# request sent to model set on litellm proxy, `litellm --model`

'''
def newBedrockPrompt(petition):
	response = client.chat.completions.create(model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0", messages = [
	    {
	        "role": "user",
	        "content": petition + "Los atributos que contiene cada archivo vienen en el siguiente diccionario " + str(pruebaColumnas)
	    }
	])
	#  "content": f"Por favor, resume los siguientes datos médicos del paciente:\n\n{document}\n\nResumen:"
	# print(response)
	return(response)
'''

def newGeminiPromptArchivos(petition):
	# Configurar la API Key
	genai.configure(api_key=GEMINI_API_KEY)

	# Seleccionar el modelo
	model = genai.GenerativeModel("gemini-2.0-flash")

	# Generar la respuesta
	response = model.generate_content(petition + "Los atributos que contiene cada archivo vienen en el siguiente diccionario " + str(pruebaColumnas))
	return(response.text)

def newGeminiPrompt(petition):
	# Configurar la API Key
	genai.configure(api_key=GEMINI_API_KEY)

	# Seleccionar el modelo
	model = genai.GenerativeModel("gemini-2.0-flash")

	# Generar la respuesta
	response = model.generate_content(petition)
	return(response.text)


#petition = input("Introduzca una pregunta:\n")
#consulta = newGeminiPrompt(petition)
#print(consulta)
#print(consulta.choices[0].message.content)


###########################

class AsistenteResumenes:
    contador = 0
    def __init__(self):
        self.historial_preguntas = []  # Usamos una lista como pila

    def hacer_pregunta(self, pregunta):
        """Añade la pregunta a la pila y la retorna."""
        self.historial_preguntas.append(pregunta)
        self.contador = self.contador + 1
        return pregunta

    def obtener_penultima_pregunta(self):
        """Obtiene la última pregunta sin eliminarla de la pila."""
        if self.contador > 1:
            return self.historial_preguntas[-2]  # Accede al último elemento
        else:
            return ""  # No hay preguntas en el historial
    
    def obtener_ultima_pregunta(self):
        """Obtiene la última pregunta sin eliminarla de la pila."""
        if self.historial_preguntas:
            return self.historial_preguntas[-1]  # Accede al último elemento
        else:
            return None  # No hay preguntas en el historial

    def deshacer_pregunta(self):
        if (self.historial_preguntas > 2):
            self.contador = self.contador - 1
            return self.historial_preguntas.pop()
        else:
            return None
	
    def imprimir_historial(self):
        """Imprime el historial de preguntas."""
        print("Historial de Preguntas:")
        for i, pregunta in enumerate(self.historial_preguntas):
            print(f"{i+1}: {pregunta}")


# Ejemplo de uso
asistente = AsistenteResumenes()


def verPromptAnterior(petition):
	consulta = newGeminiPrompt("Se ha realizado la siguiente pregunta: " + petition + "Crees que es necesario consultar la pregunta que el usuario realizó previamente para entender el contexto del que se habla? Responde SI en caso afirmativo, NO en caso negativo.")
	return consulta


prompt = input("¿En qué puedo ayudarte?\n")

while (prompt!="No"):
	prompt = asistente.hacer_pregunta(prompt)
	consultarAnterior = verPromptAnterior(prompt)
	respuesta = ""
	si = "SI"
	if consultarAnterior.strip() =='SI':
		respuesta = newGeminiPrompt(". La pregunta realizada previamente, en caso de necesitar saber el contexto, fue: " + asistente.obtener_penultima_pregunta() + ". Esta pregunta ya ha sido respondida. La siguiente que debes responder es: " + prompt)
	else:
		respuesta = newGeminiPrompt(prompt)
	
	print(respuesta)
	prompt = input("¿Algo más?\n")
	ultima_pregunta = prompt
