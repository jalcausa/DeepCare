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
        Given the following request: "{input}", and considering the files "{files}", generate Python code using pandas to read and extract the relevant information. The content of the files is {self.atributos}. ONLY USE THE FILES GIVEN, don't make up any new file.
        Assume the files are in CSV format and that they are located inside {directorio}. The code should return the extracted information in a dictionary format. Don't include any explanations, just the code. The code must start with import.
        """
        
        codigo_generado = self.client.get_response(prompt)
        codigo_generado = self.limpiar_codigo(codigo_generado)
        # Crear un entorno seguro para la ejecución
        entorno_seguro = {"pd": pd, "io": io, "base64": base64}
        try:
            #print(codigo_generado)
            exec(codigo_generado, entorno_seguro)
            return entorno_seguro.get("result", "No result found")
        except Exception as e:
            return f"Error al ejecutar código generado: {e}"

# fileAgent = FileAgent()
# info = fileAgent.getInfo("Dame un resumen de los procedimientos del paciente 1")
# print(info)