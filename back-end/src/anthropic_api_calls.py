import openai
from config import API_KEY

class AnthropicClient:
    """
    Cliente para interactuar con Amazon Titan a través de Amazon Bedrock.
    """
    def __init__(self):
        """Inicializa el cliente de Bedrock Runtime."""
        self.client = openai.OpenAI(api_key=API_KEY, base_url="https://litellm.dccp.pbu.dedalus.com")

    def get_response(self, text, data=None):
        """
        Envía un prompt a Anthropic y devuelve la respuesta generada.
                
        """
        if data:
            text = "If you need to consult any data here you have it" + str(data)
        response = self.client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages = [
		    {
		        "role": "user",
		        "content": text
		    }
			]
        )
        
        return response.choices[0].message.content # Devuelve solo el contenido del mensaje

""" #  Ejemplo de uso:
client = AnthropicClient()
response = client.get_response("Dime las 3 capitales europeas más importantes.")
print(response)  # Muestra los primeros valores del embedding """

