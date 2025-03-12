# GEMINI PRO

from src.secret import GEMINI_KEY
import requests
import json

import google.generativeai as genai

# Configurar la API de Gemini
genai.configure(api_key=GEMINI_KEY)

def newPrompt(petition):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Usa Gemini Pro
    response = model.generate_content(
        petition
    )
    return response.text  # Extrae el texto de la respuesta

print(newPrompt("Write a short poem"))