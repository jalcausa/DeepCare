from data_handler import atributos_archivos, directorio
from api_calls import new_gemini_prompt
from assistant import AsistentePreguntas
import graph_generator

# Obtener columnas de los CSV
prueba_columnas = atributos_archivos(directorio)
#print("Columnas de los archivos:", prueba_columnas)

# Ejemplo de uso
asistente = AsistentePreguntas()


def verPromptAnterior(petition):
	consulta = new_gemini_prompt("Se ha realizado la siguiente pregunta: " + petition + "Crees que es necesario consultar la pregunta que el usuario realizó previamente para entender el contexto del que se habla? Responde SI en caso afirmativo, NO en caso negativo.")
	return consulta


prompt = input("¿En qué puedo ayudarte?\n")

while (prompt!="No"):
	prompt = asistente.hacer_pregunta(prompt)
	consultarAnterior = verPromptAnterior(prompt)
	respuesta = ""
	if consultarAnterior.strip() =='SI':
		respuesta = new_gemini_prompt(". La pregunta realizada previamente, en caso de necesitar saber el contexto, fue: " + asistente.obtener_penultima_pregunta() + ". Esta pregunta ya ha sido respondida. La siguiente que debes responder es: " + prompt)
	else:
		respuesta = new_gemini_prompt(prompt)
	
	print(respuesta)
	prompt = input("¿Algo más?\n")
