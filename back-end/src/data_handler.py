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
