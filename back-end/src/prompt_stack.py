from anthropic_api_calls import AnthropicClient

class PromptStack:
    contador = 0
    client = AnthropicClient()
    def __init__(self):
        self.historial_preguntas = []  # Usamos una lista como pila

    def hacer_pregunta(self, pregunta):
        """Añade la pregunta a la pila y la retorna."""
        self.historial_preguntas.append(pregunta)
        self.contador = self.contador + 1
        return pregunta

    def verPromptAnterior(self, petition):
        prompt = prompt = f"""
        YOUR RESPONSE TO THIS QUERY MUST BE A SINGLE NUMBER. No explanations, no additional text—just the number.

        The following instructions will guide your reasoning before responding.

        A user has asked the following question:
        "{petition}"

        If you believe that additional context is necessary to accurately answer this question, here is the stack of recent questions that have been asked:
        {" ::: ".join(self.historial_preguntas)}

        ### How to determine your response:
        1. **First, think step by step:**
           - Can you confidently answer the current question without any additional context?
           - If yes, your response is **0**.

        2. **If not, analyze the previous questions one by one (starting from the most recent):**
            - Look at the last question in the stack. If that context helps you understand the current question, increase your counter by **1**.
            - If you still don't have enough context, move to the previous question in the stack and increase your counter again.
            - Repeat this process until you have enough context to accurately answer the current question. 
            How can you know if you have enough context? Let me break it down to you:
                2.1. **Identify the Key Theme**: Look at the current question to identify the key theme. 
                For example, if the current question is "Can you summarize the evolution of patient 4?", 
                the theme is "evolution summary" and "patient 4".
            Now go back to the user's question. Can you identify the Key Theme? Are you sure? If not, you 
            definetely need more context.

        3. **Your final response must be ONLY the total number of past questions you had to check to gain sufficient context.**

### Example:
Imagine the current prompt is: "Do the same for number 4"
And the recent prompt stack is: ["Please summarize the evolution of patient 1" ::: "Now, summarize the evolution of patient 2" ::: "Now, patient 3"]

First, initialize to 0 the counter.
You can't answer "Do the same for number 4" without context. So, check the last prompt: 'Now, patient 3' → Increase counter to 1.
This still doesn't provide enough context. Check the previous prompt: 'Now, summarize the evolution of patient 2' → Increase counter to 2.
Now, you understand that the user is asking for the evolution summaries of specific patients. You can confidently answer. So your answer
is the value of the counter, which is 2 in this example.
 **Final response of this example: 2**

Use the example as a way to understand and answer correctly.

**REMEMBER: Your response must be a single number. No explanations, no extra text. Just the number.**
"""

        consulta = PromptStack.client.get_response(prompt)
        print("\n Stack de preguntas: " + " ::: ".join(self.historial_preguntas))
        print("\n Número de preguntas a consultar: " + consulta.strip() + "\n")
        return int(consulta.strip())

    def construirPromptEncadenado(self, petition):
        number = self.verPromptAnterior(petition)
        consulta = self.historial_preguntas[len(self.historial_preguntas) - number - 1:]
        print("\n La consulta de preguntas es: " + "::".join(consulta))
        encadenado = f"""You must respond only to the following question. Do not include any 
            information about what you have consulted to obtain the context in your response: "{petition}". 
            To have more context about what this question refers to, here is 
            the list of previously asked questions: {" ::: ".join(consulta)}"""
        print("Prompt encadenado: " + encadenado)
        return encadenado
    
    def construirPromptEncadenado2(self, petition):
        number = self.verPromptAnterior(petition)
        consulta = self.historial_preguntas[len(self.historial_preguntas) - number - 1:]
        return consulta

    def obtener_penultima_pregunta(self):
        """Obtiene la última pregunta sin eliminarla de la pila."""
        if self.contador > 1:
            return self.historial_preguntas[-2]  # Accede al último elemento
        else:
            return ""  # No hay preguntas en el historial
    
    def obtener_ultima_pregunta(self):
        """Obtiene la última pregunta sin eliminarla de la pila."""
        if self.historial_preguntas:
            return self.historial_preguntas[-1]  # Accede al último elemento
        else:
            return None  # No hay preguntas en el historial

    def deshacer_pregunta(self):
        if (self.historial_preguntas > 2):
            self.contador = self.contador - 1
            return self.historial_preguntas.pop()
        else:
            return None
	
    def imprimir_historial(self):
        """Imprime el historial de preguntas."""
        print("Historial de Preguntas:")
        for i, pregunta in enumerate(self.historial_preguntas):
            print(f"{i+1}: {pregunta}")