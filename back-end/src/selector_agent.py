from config import API_KEY
from prompt_stack import PromptStack
from graph_generator import GraphicAgent
from anthropic_api_calls import AnthropicClient

class SelectorAgent:
    gestorStack = PromptStack()
    agenteGrafico = GraphicAgent()
    client = AnthropicClient()

    def procesarInput(self, input):
        prompt = self.gestorStack.hacer_pregunta(input)
        # consultarAnterior = gestorStack.verPromptAnterior(prompt)
        respuesta = self.client.get_response(SelectorAgent.gestorStack.construirPromptEncadenado2(prompt))	
        return(respuesta)
    
    def seleccionarAgente(self, petition):
        agentes = self.client.get_response(
            '''
            You are a planning agent.
            Your job is to break down complex tasks into smaller, manageable subtasks.
            The task is: ''' + petition + '''\n
            Your team members are:

            GraphGeneratorAgent: Responsible for generating graphs based on project needs.
            EvolutionSummaryAgent: Responsible for creating medical reports with total accuracy and precision.
            AIEthicsAgent: Responsible for reviewing AI ethics, privacy, and bias issues.
            
            You only plan and delegate tasks — you do not execute them yourself.

            Use only the necessary team members to solve the task, you do not need to use all of them always.
            When assigning tasks, use this format:	<agent>: <task>
            
            The prompt : ''' + self.procesarInput(petition))
        
        return agentes
    
# agenteSelector = SelectorAgent()

# prompt = input("Qué tarea quieres hacer?")
# print(agenteSelector.seleccionarAgente(prompt))