import re
from anthropic_api_calls import AnthropicClient

class SummaryAgent:
    def __init__(self):
        self.client = AnthropicClient()
    
    def generar_informe(self, peticion, datos_paciente=None):
        """Genera un informe médico preciso basado en la petición del usuario y los datos del paciente (opcional)."""
        prompt = f"""Genera un informe médico detallado basado en la siguiente solicitud del usuario:
        INSTRUCCIONES CRÍTICAS:
        1. La respuesta debe ser precisa, clara y basada en datos clínicos.
        2. Utiliza un tono profesional y estructurado.
        3. Si se proporcionan datos del paciente, intégralos de manera adecuada en el informe.
        4. No inventes información; si no hay datos suficientes, menciona la limitación.
        
        Petición del usuario: {peticion}
        """
        
        if datos_paciente:
            prompt += f"\nDatos clínicos del paciente:\n{datos_paciente}"
        
        respuesta = self.client.get_response(prompt)
        return respuesta.strip()
    
    def limpiar_informe(self, informe):
        """Elimina etiquetas no deseadas o formato incorrecto en el informe generado."""
        return re.sub(r"```[a-z]*\n|```", "", informe).strip()

