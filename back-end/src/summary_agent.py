import re
from anthropic_api_calls import AnthropicClient

class SummaryAgent:
    def __init__(self):
        self.client = AnthropicClient()
    
    def generate_report(self, request, patient_data=None):
        """Generates a precise medical report based on the user's request and optional patient data."""
        prompt = f"""Generate a detailed medical report based on the following user request:
        CRITICAL INSTRUCTIONS:
        1. The response must be precise, clear, and based on clinical data.
        2. Use a professional and structured tone.
        3. If patient data is provided, integrate it appropriately into the report.
        4. Do not invent information; if data is insufficient, mention the limitation.

        User request: {request}
        """
        print(str(patient_data))
        if patient_data:
            prompt += f"\nPatient clinical data:\n{patient_data}"
        
        response = self.client.get_response(prompt)
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