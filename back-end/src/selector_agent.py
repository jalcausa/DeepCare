
from config import API_KEY
from prompt_stack import PromptStack
from graph_generator import GraphicAgent
from anthropic_api_calls import AnthropicClient

class SelectorAgent:
	gestorStack = PromptStack()
	agenteGrafico = GraphicAgent()
	client = AnthropicClient()
	@staticmethod
	def procesarInput(input):
		prompt = SelectorAgent.gestorStack.hacer_pregunta(input)
		# consultarAnterior = gestorStack.verPromptAnterior(prompt)
		respuesta = SelectorAgent.client.get_response(SelectorAgent.gestorStack.construirPromptEncadenado(prompt))	
		return(respuesta)
