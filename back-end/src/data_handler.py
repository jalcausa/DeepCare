import os
import pandas as pd
from pathlib import Path

directorio = Path(__file__).parent.parent / "data"

def atributos_archivos(directorio):
    columnas = {}
    for archivo in os.listdir(directorio):
        if archivo.endswith(".csv"):
            ruta_archivo = os.path.join(directorio, archivo)
            df = pd.read_csv(ruta_archivo, nrows=0)
            columnas[archivo] = df.columns.tolist()
    return columnas

def ruta_archivos(directorio):
    """
    Returns a dictionary where the keys are the filenames and the values are the full file paths
    for the CSV files in the specified directory.
    """
    rutas = {}
    for archivo in os.listdir(directorio):
        if archivo.endswith(".csv"):
            ruta_archivo = os.path.join(directorio, archivo)
            rutas[archivo] = ruta_archivo
    return rutas
# columnas = atributos_archivos(directorio)
# print(columnas)