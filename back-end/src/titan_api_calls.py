import openai
import math
from config import API_KEY

class TitanClient:
    """
    Cliente para interactuar con Amazon Titan a través de Amazon Bedrock.
    """
    def __init__(self):
        """Inicializa el cliente de Bedrock Runtime con las credenciales de AWS."""
        self.client = openai.OpenAI(api_key=API_KEY, base_url="https://litellm.dccp.pbu.dedalus.com")

    def get_embedding(self, text):
        """
        Envía un prompt a Titan y devuelve la respuesta generada.
                
        """
        response = self.client.embeddings.create(
            model="bedrock/amazon.titan-embed-text-v2:0",
            input=text,  # Se usa "prompt", no "messages"
            encoding_format=None
        )
        
        return response.data[0].embedding  # Devuelve el vector de embedding

    # def generate_response_with_columns(self, prompt, columns, **kwargs):
    #     """
    #     Envía un prompt a Titan incluyendo una lista de atributos de archivos.

    #     :param prompt: Texto de entrada para el modelo Titan.
    #     :param columns: Lista de nombres de columnas a incluir en el prompt.
    #     :param kwargs: Parámetros opcionales (max_tokens, temperature, top_p).
    #     :return: Texto generado por el modelo Titan.
    #     """
    #     full_prompt = f"{prompt} Los atributos de los archivos son: {', '.join(columns)}."
    #     return self.generate_response(full_prompt, **kwargs)

#  Ejemplo de uso:
titan = TitanClient()
embedding1 = titan.get_embedding("Huevo")
embedding2 = titan.get_embedding("Gallina")
print(embedding1[:5])  # Muestra los primeros valores del embedding
print(embedding2[:5])

def cosine_similarity_basic(vec1, vec2):
    # Producto punto
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # Norma de los vectores
    norm_vec1 = math.sqrt(sum(a * a for a in vec1))
    norm_vec2 = math.sqrt(sum(b * b for b in vec2))
    
    # Similitud del coseno
    return dot_product / (norm_vec1 * norm_vec2)

# Comparar los embeddings de "perro" y "gato" usando la similitud del coseno
similarity = cosine_similarity_basic(embedding1, embedding2)
print("Similitud entre 'perro' y 'gato':", similarity)



""" columnas = ["Nombre", "Edad", "Diagnóstico"]
respuesta_columnas = titan.generate_response_with_columns("Analiza estos datos médicos.", columnas)
print("Análisis de datos médicos:", respuesta_columnas) """
