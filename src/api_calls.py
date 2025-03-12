import openai
import google.generativeai as genai
from config import API_KEY, GEMINI_API_KEY

def new_gemini_prompt(petition):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(petition)
    return response.text

def new_gemini_prompt_archivos(petition, prueba_columnas):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(petition + "Los atributos de los archivos son: " + str(prueba_columnas))
    return response.text
