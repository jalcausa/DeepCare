from gemini_api_calls import new_gemini_prompt

class PromptStack:
    contador = 0
    def __init__(self):
        self.historial_preguntas = []  # Usamos una lista como pila

    def hacer_pregunta(self, pregunta):
        """Añade la pregunta a la pila y la retorna."""
        self.historial_preguntas.append(pregunta)
        self.contador = self.contador + 1
        return pregunta

    def verPromptAnterior(self, petition):
        consulta = new_gemini_prompt("Se ha realizado la siguiente pregunta: " + petition + 
                                     "Si crees que es necesario obtener más información sobre el contexto de la pregunta, aquí te dejo el stack de preguntas que se han hecho recientemente." + " ::: ".join(self.historial_preguntas) +
                                     ". Tu respuesta a esta consulta debe ser única y exclusivamente el número de preguntas anteriores que deben ser consultadas para poder responder a la pregunta actual de forma correcta." +
                                     " Primero, piensa paso a paso. ¿Crees que serías capaz de responder con precisión a la pregunta, sin necesidad de contexto adicional? Si la respuesta es no, piensa inductivamente. Mira la pregunta que se hizo anteriormente " +
                                     "en el stack de preguntas que te he pasado. Con el contexto en el que se hizo esa pregunta, serías capaz de responder ahora a la pregunta actual? Si la respuesta es no, vuelve a mirar otra pregunta, hasta que creas que "
                                     "puedes responder con precisión. Ve contando cuántas preguntas has tenido que consultar, y responde únicamente con ese número. " +
                                     "Te pongo un ejemplo. Imagina que la pregunta actual es: ¿Y la de Portugal?. Imagina que el stack de preguntas anteriores es: [Cuántas ruedas tiene un coche? ::: Cuál es la capital de Francia? ::: Y la de España?]" + 
                                     ". Entonces como no puedes responder a la pregunta ¿Y la de Portugal? sin un contexto previo, miras la pregunta anterior. "+ 
                                     "En este caso, la pregunta anterior es: Y la de España? Subes el contador a 1. Sin embargo todavía no tienes contexto suficiente para " + 
                                     "responder acertadamente. Por lo tanto, consultas la pregunta anterior: Cuál es la capital de Francia? Subes el contador a 2. Ahora puedes entender que " + 
                                     "el usuario está preguntando por las capitales, luego podrías responder acertadamente su pregunta ¿Y la de Portugal? Por tanto, tu respuesta es: 2")
       # print("\n Stack de preguntas: " + " ::: ".join(self.historial_preguntas))
       # print("\n Número de preguntas a consultar: " + consulta.strip() + "\n")
        return int(consulta.strip())

    def construirPromptEncadenado(self, petition):
        number = self.verPromptAnterior(petition)
        consulta = self.historial_preguntas[len(self.historial_preguntas) - number - 1:]
       # print("\n La consulta de preguntas es: " + "::".join(consulta))
        encadenado = "Debes responder únicamente a la siguiente pregunta: " + petition + ". Para tener más contexto sobre a lo que se refiere esta pregunta, aquí tienes la lista de preguntas que se han realizado anteriormente: " + " ::: ".join(consulta)
       # print("Prompt encadenado: " + encadenado)
        return encadenado

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