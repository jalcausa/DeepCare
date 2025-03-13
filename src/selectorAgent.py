class AgenteSelector:
    #Sin acabar
    response = client.chat.completions.create(model="bedrock/amazon.titan-embed-text-v2:0", # model to send to the proxy     
                                              messages = [
                                                  {"role": "user",
                                                   "content": "this is a test request, write a short poem"
                                                   }] 
                                            )

    def __init__(self, modelo_llm):
        """
        Constructor del AgenteSelector.
        
        :param modelo_llm: Instancia del modelo LLM utilizado para la selección (como GPT-4).
        """
        self.modelo_llm = modelo_llm
    
    def seleccionar_agentes(self, prompt):
        """
        Analiza el prompt utilizando el modelo LLM y decide qué agentes se deben usar.

        :param prompt: El texto del prompt a analizar.
        :return: Una lista de los agentes a utilizar: ['Graph', 'Stack', 'Archivo'] o una lista vacía.
        """
        # Prompt para el LLM que le pide al modelo interpretar qué agentes utilizar.
        instrucciones = """
        Dado el siguiente prompt, selecciona los agentes que deben ser utilizados:
        - 'Graph' si se requiere generar un gráfico.
        - 'Stack' si se necesita acceder al contexto de preguntas anteriores.
        - 'Archivo' si se necesita consultar los archivos médicos.
        Si no se necesita ninguno de estos, retorna una lista vacía.
        
        Prompt: "{prompt}"
        """

        # Concatenamos las instrucciones y el prompt al modelo
        texto_entrada = instrucciones.format(prompt=prompt)

        # Generamos la respuesta del modelo
        respuesta = self.modelo_llm(texto_entrada)

        # Procesamos la respuesta del modelo, esperamos una lista de agentes
        agentes = self._procesar_respuesta(respuesta)
        
        return agentes
    
    def _procesar_respuesta(self, respuesta):
        """
        Procesa la respuesta del modelo para devolver una lista de agentes.
        
        :param respuesta: Respuesta generada por el modelo LLM.
        :return: Lista de agentes a utilizar.
        """
        # Convertimos la respuesta a una lista de agentes
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

        # Si no se menciona ninguno, retornamos una lista vacía
        return agentes_seleccionados

# Uso del Agente Selector:
# Supón que tenemos una instancia del modelo LLM que puede interpretar prompts.
# Este modelo podría ser un GPT-4 en su versión API o alguna instancia entrenada.

modelo_llm_simulado = lambda prompt: "Graph, Stack"  # Simulación del modelo para pruebas

agente_selector = AgenteSelector(modelo_llm_simulado)

# Ejemplo de prompt
prompt = "Necesito un gráfico para visualizar los datos de los pacientes y el contexto previo de la consulta."

# Obtenemos los agentes a utilizar
agentes_a_utilizar = agente_selector.seleccionar_agentes(prompt)

print(agentes_a_utilizar)  # ['Graph', 'Stack']
