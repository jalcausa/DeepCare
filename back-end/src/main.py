from data_handler import atributos_archivos, directorio
from gemini_api_calls import new_gemini_prompt
from prompt_stack import PromptStack
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
	respuesta = new_gemini_prompt(gestorStack.construirPromptEncadenado(prompt))	
	print(respuesta)
	prompt = input("¿Algo más?\n")
