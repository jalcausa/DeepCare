from config import API_KEY
from anthropic_api_calls import AnthropicClient

class SelectorAgent:
    client = AnthropicClient()

    def procesarInput(self, input):
        respuesta = self.client.get_response(input)	
        return(respuesta)
    
    def seleccionarAgente(self, petition):
        respuesta = self.client.get_response(
            '''
            You are a planning agent.
            Your job is to break down complex tasks into smaller, manageable subtasks.
            The task is: ''' + petition + '''\n
            Your team members are:

            GraphGenerator: Responsible for generating graphs based on project needs.
            SummaryAgent: Responsible for creating medical reports with total accuracy and precision. This agent should
                    be the one used for asking questions like: 'What's wrong with Juan García?, as Juan García could
                    be the name of a patient. All questions like 'Qué le pasa a "nombre"?' should be managed by this
                    agent.
            ChatAgent: Responsible for answering any other questions.
            
            You only plan and delegate tasks — you do not execute them yourself.

            ###EXTREMELY IMPORTANT###
            Your response must be exclusively of this type 'agent,number,full name' , where the first position is the 
            name of the agent to use The second position is the patient number you 
            were asked about. If no specific patient number was mentioned, or if more than one 
            patient was asked about at once, return -1 as the second position. The third position should be the 
            mentioned name, in case that a name was mentioned, (for example, if the petition was 'Qué le pasa a
            Juan García?', the third position of your answer should be 'Juan García'). If no name was mentioned, 
            the third position must be 'no'.

            
            The prompt : ''' + petition)
        
        agentes = respuesta.split(',')
        #print(agentes)
        return agentes
    
# agenteSelector = SelectorAgent()

# prompt = input("Qué tarea quieres hacer?")
# print(agenteSelector.seleccionarAgente(prompt))