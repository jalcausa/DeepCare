from flask import jsonify
from data_handler import atributos_archivos, directorio
from anthropic_api_calls import AnthropicClient
from prompt_stack import PromptStack
from graph_generator import GraphicAgent
from selector_agent import SelectorAgent
from file_agent import FileAgent
from summary_agent import SummaryAgent
from pathlib import Path
from lector_csv2 import obtenerDatosPaciente

# Obtener columnas de los CSV
prueba_columnas = atributos_archivos(directorio)
#agente_grafico = GraphicAgent()
#peticion = input("Quieres ver algún gráfico?")

directorio = Path(__file__).parent/"data"
directorio_csv = directorio / "data"
#print("Columnas de los archivos:", prueba_columnas)

class ProcesadorInput:
    def __init__(self):
        self.gestorStack = PromptStack()
        self.agenteGrafico = GraphicAgent()
        self.client = AnthropicClient()
        self.selector = SelectorAgent()
        self.fileAgent = FileAgent()
        self.summaryAgent = SummaryAgent()
        
    def procesarInput(self, input):
        prompt = self.gestorStack.hacer_pregunta(input)
        prompt_encadenado = self.gestorStack.construirPromptEncadenado(prompt)
        # consultarAnterior = gestorStack.verPromptAnterior(prompt)
        selectAgentAnswer = self.selector.seleccionarAgente(prompt_encadenado)
        agent = selectAgentAnswer[0]
        patient = selectAgentAnswer[1]
        files = self.fileAgent.getFiles(prompt_encadenado)
        print("Agente seleccionado: " + agent.strip())
        if (files != "NO" and agent != "SummaryAgent"):
            data = self.fileAgent.getInfo(prompt_encadenado)
        else:
            data = None
        if (agent.strip().split(',') == "GraphGenerator"):
            codigo = self.agenteGrafico.generar_codigo(prompt_encadenado, data)
            respuesta= self.agenteGrafico.ejecutar_codigo(codigo)
            respuesta_json = jsonify({"tipo": "grafico", "grafico": respuesta})
        elif (agent.strip() == "ChatAgent"):
            respuesta = self.client.get_response(prompt_encadenado, data)
            respuesta_json = jsonify({"tipo": "texto", "texto": respuesta})
        elif (agent.strip() == "SummaryAgent"):
            data = obtenerDatosPaciente(patient)
            respuesta = self.summaryAgent.generate_report(prompt_encadenado, data)
            respuesta_json = jsonify({"tipo": "texto", "texto": respuesta})
                
        return(respuesta_json)
