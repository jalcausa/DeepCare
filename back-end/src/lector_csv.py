import csv
import io
import os
from datetime import datetime
import re
from data_handler import ruta_archivos, directorio
import unicodedata


def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = {i: row for i, row in enumerate(reader)}
    return headers, data

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        return f"ANOMALY: Invalid date format - {date_str}"

def validate_numeric(value):
    try:
        float_value = float(value.replace(',', '.'))
        return str(float_value)
    except ValueError:
        return f"ANOMALY: Non-numeric value - {value}"

def validate_row(row, expected_columns):
    if len(row) > expected_columns:
        return f"ANOMALY: Extra columns detected - {row[expected_columns:]}"
    elif len(row) < expected_columns:
        return f"ANOMALY: Missing columns - Expected {expected_columns}, got {len(row)}"
    return None


# Define the file paths relative to the base directory of the project
file_paths = ruta_archivos(directorio)
result = {}

for file_key, file_path in file_paths.items():
    headers, data = read_csv(file_path)
    result[file_key] = {'headers': headers, 'data': {}}

    for row_num, row in data.items():
        validated_row = []
        anomaly = validate_row(row, len(headers))

        if anomaly:
            validated_row = [anomaly]
        else:
            for i, value in enumerate(row):
                if headers[i].lower() in ['fecha', 'fechaingreso']:
                    validated_row.append(validate_date(value))
                elif headers[i].lower() in ['presionsistolica', 'presiondiastolica', 'frecuenciacardiaca', 'temperatura', 'frecuenciarespiratoria', 'saturacionoxigeno', 'glucosa', 'leucocitos', 'hemoglobina', 'plaquetas', 'colesterol', 'hdl', 'ldl', 'trigliceridos', 'sodio', 'potasio', 'cloro', 'creatinina', 'urea', 'ast', 'alt', 'bilirrubina', 'ph', 'pco2', 'po2', 'hco3', 'lactato', 'cetonas', 'amilasa']:
                    validated_row.append(validate_numeric(value))
                else:
                    validated_row.append(value)

        result[file_key]['data'][row_num] = validated_row

# Filter data for patient number
def obtenerDatosPaciente(patientID):
    patient_data = {file_key: {'headers': file_data['headers'], 'data': {row_num: row for row_num, row in file_data['data'].items() if row[0] == patientID}} for file_key, file_data in result.items()}

    return patient_data

# Filter data for patient name
def obtenerPacienteID(patientName):
    # Definir la ruta al archivo resumen_pacientes.csv
    ruta = os.path.join(directorio, "resumen_pacientes.csv")

    # Leer el archivo resumen_pacientes.csv
    with open(ruta, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Si hay una fila de cabecera, la saltamos
        nombre = quitar_tildes(patientName.lower())
        # Buscar el PatientID que corresponde al nombre
        for row in reader:
            if quitar_tildes(row[1].lower()) == nombre:  # Comparar en minúsculas para evitar problemas de mayúsculas/minúsculas
                return row[0]  # El PatientID está en la primera columna

    return f"ANOMALY: Patient with name '{patientName}' not found"  # Si no se encuentra el paciente

def quitar_tildes(texto):
    # Normalizar el texto a la forma de decomposición de caracteres y luego filtrar solo los caracteres ASCII
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'
    )