from config import API_KEY
from anthropic_api_calls import AnthropicClient

class SelectorAgent:
    client = AnthropicClient()

    def procesarInput(self, input):
        respuesta = self.client.get_response(input)	
        return(respuesta)
    
    def seleccionarAgente(self, petition):
        agentes = self.client.get_response(
            '''
            You are a planning agent.
            Your job is to break down complex tasks into smaller, manageable subtasks.
            The task is: ''' + petition + '''\n
            Your team members are:

            GraphGenerator: Responsible for generating graphs based on project needs.
            SummaryAgent: Responsible for creating medical reports with total accuracy and precision.
            ChatAgent: Responsible for answering any other questions.
            
            You only plan and delegate tasks — you do not execute them yourself.

            Answer EXCLUSIVELY with the name of the agent you think is more likely to solve the problem.
            
            The prompt : ''' + petition)
        
        #print(agentes)
        return agentes
    
# agenteSelector = SelectorAgent()

# prompt = input("Qué tarea quieres hacer?")
# print(agenteSelector.seleccionarAgente(prompt))