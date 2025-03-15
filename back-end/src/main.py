from data_handler import atributos_archivos, directorio
from anthropic_api_calls import AnthropicClient
from prompt_stack import PromptStack
from graph_generator import GraphicAgent
from selector_agent import SelectorAgent
from pathlib import Path

# Obtener columnas de los CSV
prueba_columnas = atributos_archivos(directorio)
#agente_grafico = GraphicAgent()
#peticion = input("Quieres ver algún gráfico?")

directorio = Path(__file__).parent/"data"
directorio_csv = directorio / "data"
#print("Columnas de los archivos:", prueba_columnas)

class procesarInput:
	gestorStack = PromptStack()
	# agenteGrafico = GraphicAgent()
	client = AnthropicClient()
	@staticmethod
	def procesarInput(input):
		prompt = procesarInput.gestorStack.hacer_pregunta(input)
		# consultarAnterior = gestorStack.verPromptAnterior(prompt)
		respuesta = procesarInput.client.get_response(procesarInput.gestorStack.construirPromptEncadenado(prompt))	
		return(respuesta)
