class AsistentePreguntas:
    contador = 0
    def __init__(self):
        self.historial_preguntas = []  # Usamos una lista como pila

    def hacer_pregunta(self, pregunta):
        """Añade la pregunta a la pila y la retorna."""
        self.historial_preguntas.append(pregunta)
        self.contador = self.contador + 1
        return pregunta

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