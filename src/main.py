from data_handler import atributos_archivos, directorio
from gemini_api_calls import new_gemini_prompt
from promptStack import PromptStack
from graph_generator import GraphicAgent

# Obtener columnas de los CSV
prueba_columnas = atributos_archivos(directorio)
#print("Columnas de los archivos:", prueba_columnas)


gestorStack = PromptStack()
agenteGrafico = GraphicAgent()


prompt = input("¿En qué puedo ayudarte?\n")

while (prompt!="No"):
	prompt = gestorStack.hacer_pregunta(prompt)
	consultarAnterior = gestorStack.verPromptAnterior(prompt)
	respuesta = ""
	if consultarAnterior.strip() =='SI':
		respuesta = new_gemini_prompt(". La pregunta realizada previamente, en caso de necesitar saber el contexto, fue: " + gestorStack.obtener_penultima_pregunta() + ". Esta pregunta ya ha sido respondida. La siguiente que debes responder es: " + prompt)
	else:
		respuesta = new_gemini_prompt(prompt)
	
	print(respuesta)
	prompt = input("¿Algo más?\n")
