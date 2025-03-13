import boto3
import json
from config import API_KEY

class TitanClient:
    """
    Cliente para interactuar con Amazon Titan a través de Amazon Bedrock.
    """

    def __init__(self):
        """Inicializa el cliente de Bedrock Runtime con las credenciales de AWS."""
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

    def generate_response(self, prompt, max_tokens=500, temperature=0.7, top_p=0.9):
        """
        Envía un prompt a Titan y devuelve la respuesta generada.

        :param prompt: Texto de entrada para el modelo Titan.
        :param max_tokens: Límite de tokens en la respuesta (por defecto 500).
        :param temperature: Controla la aleatoriedad del modelo (0.0 = determinista, 1.0 = creativo).
        :param top_p: Controla la diversidad de la respuesta.
        :return: Texto generado por el modelo Titan.
        """
        payload = {
            "prompt": prompt,
            "maxTokens": max_tokens,
            "temperature": temperature,
            "topP": top_p
        }

        try:
            response = self.client.invoke_model(
                modelId="amazon.titan-text-express-v1",
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )

            response_body = json.loads(response["body"].read().decode("utf-8"))
            return response_body["results"][0]["outputText"].strip()

        except Exception as e:
            print(f" Error al llamar a Titan: {e}")
            return None  # Retorna None si hay error

    def generate_response_with_columns(self, prompt, columns, **kwargs):
        """
        Envía un prompt a Titan incluyendo una lista de atributos de archivos.

        :param prompt: Texto de entrada para el modelo Titan.
        :param columns: Lista de nombres de columnas a incluir en el prompt.
        :param kwargs: Parámetros opcionales (max_tokens, temperature, top_p).
        :return: Texto generado por el modelo Titan.
        """
        full_prompt = f"{prompt} Los atributos de los archivos son: {', '.join(columns)}."
        return self.generate_response(full_prompt, **kwargs)

#  Ejemplo de uso:
titan = TitanClient()

prompt = "Explica la importancia de los datos en la salud."
respuesta = titan.generate_response(prompt)
print("Titan dice:", respuesta)

columnas = ["Nombre", "Edad", "Diagnóstico"]
respuesta_columnas = titan.generate_response_with_columns("Analiza estos datos médicos.", columnas)
print("Análisis de datos médicos:", respuesta_columnas)
