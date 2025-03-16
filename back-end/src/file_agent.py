import pandas as pd
import io
import base64
import re
from data_handler import *
from anthropic_api_calls import AnthropicClient

class FileAgent:
    def __init__(self):
        self.client = AnthropicClient()
        self.atributos = atributos_archivos(directorio)
    def getFiles(self, input):
        prompt = f"""I need you to determine whether you need to consult the data stored in some files to answer this prompt: {input}. Here you have the atributes that store each file: {self.atributos}. It is extremely important that you strictly only answer with the name of the files you consider more likely would be needed to consult, separated by commas. Include the .csv in the name. If you think you don't need to consult any file answer NO
        """
        return self.client.get_response(prompt).strip()
    
    def limpiar_codigo(self, codigo):
        """Elimina etiquetas de código Markdown como ```python y ```"""
        return re.sub(r"```[a-z]*\n|```", "", codigo).strip()
    
    def getInfo(self, input):
        files = self.getFiles(input)
        if (files == "NO"):
            return "No files needed."
        prompt = f"""
Given the following request: "{input}", and considering the files "{files}", generate Python code using pandas to read, process, and extract the relevant information. 
The content of the files is {self.atributos}. 

### Instructions:
- **ONLY USE THE FILES GIVEN.** Do not invent new file names.
- Assume all files are in CSV format and are located inside {directorio}.
- The extracted data must be stored in a dictionary where:
  - The **KEY** corresponds to the row number.
  - The **VALUE** is a list containing all column values for that row.
- **DO NOT use `pd.read_csv()`.** Instead, implement manual file reading using Python's built-in functions.
- Ensure that column headers (first row) are properly stored, allowing access to values based on their column index.
- The final extracted information must be stored in a variable named `result`.
- **The code must strictly start with `import` and contain no explanations.**
- Use io.StringIO instead of pd.compat.StringIO, if necessary.
- Be careful with errors like: "Error executing generated code: 'charmap' codec can't decode byte 0x81 in position 1435: character maps to <undefined>"
- Be careful with errors like: "list index out of range"
-Be careful with errors like: "Error tokenizing data. C error: Expected 30 fields in line 3, saw 31"


### Data Validation Requirements:
Your code must also be capable of detecting and handling potential data anomalies, including:

1. **Out-of-range values**:  
   - Identify any values that exceed plausible limits (e.g., temperatures above 50°C, pH levels higher than the physiological range, etc.).  
   - Flag these values as anomalies in the final output.  

2. **Empty columns**:  
   - Detect columns that contain no data.  
   - Explicitly indicate that no information is available for those parameters.  

3. **Extra columns and data shifts**:  
   - If a row contains more columns than expected, determine whether:  
     a) The extra columns are erroneous and should be ignored.  
     b) A data shift has occurred (e.g., values appear displaced across columns). In this case, attempt to realign the data correctly.  
   - If realignment is not possible, flag the row as containing inconsistent data.  

4. **Incorrect formatting of dates and decimals**:  
   - Standardize date formats if multiple formats are detected.  
   - Ensure numerical values (e.g., decimals) follow a consistent format (either using `.` or `,`).  

Ensure that all detected anomalies are clearly flagged in the final result. REMEMBER: **The code must strictly start with `import` and contain no explanations.** 
"""

        
        codigo_generado = self.client.get_response(prompt)
        codigo_generado = self.limpiar_codigo(codigo_generado)
        # Crear un entorno seguro para la ejecución
        entorno_seguro = {"pd": pd, "io": io, "base64": base64}
        try:
            print(codigo_generado)
            exec(codigo_generado, entorno_seguro)
            return entorno_seguro.get("result", "No result found")
        except Exception as e:
            return f"Error al ejecutar código generado: {e}"

#fileAgent = FileAgent()
#info = fileAgent.getInfo("Dame un resumen de los procedimientos del paciente 1")
#print(info)