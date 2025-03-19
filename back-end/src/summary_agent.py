import re
import os
import pandas as pd
from anthropic_api_calls import AnthropicClient
from data_handler import directorio

class SummaryAgent:
    def __init__(self):
        self.client = AnthropicClient()
    
    def generate_report(self, request, patient_data=None):
        """Generates a precise medical report based on the user's request and optional patient data."""
        prompt = f"""Imagine that you are a very competent doctor that needs to generate a detailed medical report ç
        for a patient that is being discharged based on the following user request:
        CRITICAL INSTRUCTIONS:
        1. The response must be precise, clear, and based on clinical data.
        2. Use a professional and structured tone.
        3. If patient data is provided, integrate it appropriately into the report.
        4. Do not invent information; if data is insufficient, mention the limitation.
        5. Make some recommendations based on the set of rules given above that best match the patien profile and that could be 
        extremely important to follow. If there are none that match the rules add some general recommendatios at the end of the
        report.
        6. **HIGHLIGHT TITLES** and **Highlight important medical terms in bold** by surrounding them with double asterisks (**example**).
        7. NEVER finish the summary with lines like:    
                    Dr. [Nombre del Médico]
                    Colegiado Nº [Número de Colegiado]
                    Servicio de Cirugía General

        
        User request: {request}
        """
        print(str(patient_data))
        if patient_data:
            prompt += f"\nPatient clinical data:\n{patient_data}"
        recommendations_path = os.path.join(directorio, "recomendaciones.csv")
        df = pd.read_csv(recommendations_path)
        recommendations = df.to_string(index=False)
        prompt += f"\nSET OF RECOMMENDATIONS TO FOLLOW:\n{recommendations}"
        response = self.client.get_response(prompt)
        print("SummaryAgent, línea 40")
        return response.strip()
    
'''
# Create an instance of the agent
summary_agent = SummaryAgent()

# User request
request = "Generate an evolutionary report for patient ID 12345 based on their latest lab results."

# Simulated patient data
patient_data = """
Patient ID: 12345
Age: 56 years
Diagnosis: Type 2 Diabetes
Latest lab results:
  - Blood glucose: 180 mg/dL
  - Hemoglobin A1c: 7.5%
  - Blood pressure: 140/90 mmHg
"""

# Generate the medical report
generated_report = summary_agent.generate_report(request, patient_data)

# Display the generated report
print("Generated report by the Summary Agent:")
print(generated_report)

'''

'''
I would like you to give me a set of rules that could be used by a LLM to make recomendations base in the values of these fields: Edad,Sexo,Alergias,MotivoIngreso,DiagnosticoPrincipal,CondicionesPrevias,FechaIngreso,Servicio,EstadoAlIngreso. For example if MotivoIngreso is fiebre recommend taking some medicine to fix that. Generate at least 100 rules you can think for these fields in a csv format where the fields are "if" and "then". The id field must contain which of the fields or fields given was taken into consideration and there value to make the recomendation and "then" must contain the recomendations made in base of the "if" values.
'''


'''

        6. <strong>Highlight important medical terms in bold</strong> by surrounding them with <strong> and </strong> (<strong>example</strong>).
        7. USE HTML FORMAT FOR YOUR ANSWER. Use indentations to make it look better, and don't add
        innecessary blank lines. For example:
            Motivo de Ingreso:
            (blank line)
            (indentation)    Disnea en aumento, tos productiva con esputo purulento
            (blank line)
            Diagnóstico Principal:
            (blank line)
            (indentation)   Exacerbación de EPOC (Código CIE-10: 195951007)
'''