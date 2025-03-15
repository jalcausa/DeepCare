import requests
from config import API_KEY

class AgenteSelector:
    def __init__(self, api_key, endpoint):
        """
        Constructor del AgenteSelector.

        :param api_key: La clave de API para acceder al modelo.
        :param endpoint: La URL del endpoint para hacer la consulta.
        """
        self.api_key = api_key
        self.endpoint = endpoint

    def seleccionar_agentes(self, prompt):
        """
        Analiza el prompt utilizando el modelo y decide qué agentes se deben usar.

        :param prompt: El texto del prompt a analizar.
        :return: Una lista de los agentes a utilizar: ['Graph', 'Stack', 'Archivo'] o una lista vacía.
        """
        # Construir la solicitud para el modelo Titan
        texto_entrada = f"""
        Dado el siguiente prompt, selecciona los agentes que deben ser utilizados:
        - 'Graph' si se requiere generar un gráfico.
        - 'Stack' si se necesita acceder al contexto de preguntas anteriores.
        - 'Archivo' si se necesita consultar los archivos médicos.
        Si no se necesita ninguno de estos, retorna una lista vacía.

        Prompt: "{prompt}"
        """

        # Realizamos la solicitud a Titan
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        # Realizamos el POST request al modelo
        payload = {
            "model": "titan",  # Aquí colocas el nombre correcto del modelo Titan
            "messages": [
                {"role": "user", "content": texto_entrada}
            ]
        }

        # Llamada a la API de Titan (esto puede cambiar dependiendo de la documentación de Titan)
        response = requests.post(self.endpoint, json=payload, headers=headers)

        # Comprobamos que la solicitud se haya realizado correctamente
        if response.status_code == 200:
            respuesta = response.json()
            return self._procesar_respuesta(respuesta['choices'][0]['message']['content'])
        else:
            print("Error en la llamada a la API:", response.status_code)
            return []

    def _procesar_respuesta(self, respuesta):
        """
        Procesa la respuesta del modelo para devolver una lista de agentes.

        :param respuesta: Respuesta generada por el modelo LLM (Titan).
        :return: Lista de agentes a utilizar.
        """
        respuesta = respuesta.strip().lower()

        # Definimos los agentes disponibles
        agentes_disponibles = ['graph', 'stack', 'archivo']

        # Lista que contendrá los agentes seleccionados
        agentes_seleccionados = []

        # Si la respuesta menciona algún agente, lo añadimos a la lista
        if 'graph' in respuesta:
            agentes_seleccionados.append('Graph')
        if 'stack' in respuesta:
            agentes_seleccionados.append('Stack')
        if 'archivo' in respuesta:
            agentes_seleccionados.append('Archivo')

        return agentes_seleccionados


# Uso del Agente Selector:
# Debes reemplazar 'YOUR_API_KEY' con la clave real de tu API de Titan y el endpoint correspondiente.


endpoint = 'https://api.titan.com/v1/completions'  # Este es un ejemplo del endpoint, ajústalo según la documentación de Titan.

agente_selector = AgenteSelector(API_KEY, endpoint)

# Ejemplo de prompt
prompt = "Necesito un gráfico para visualizar los datos de los pacientes y el contexto previo de la consulta."

# Obtenemos los agentes a utilizar
agentes_a_utilizar = agente_selector.seleccionar_agentes(prompt)

print(agentes_a_utilizar)  # ['Graph', 'Stack']
