import csv
import io
import re
from datetime import datetime

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return list(csv.reader(file))

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%d/%m/%Y')
        except ValueError:
            return None

def validate_numeric(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return None

def validate_range(value, min_val, max_val):
    if value is not None and min_val <= value <= max_val:
        return value
    return None

file_path = '/Users/jcalcausal/Documents/Carrera/DeepCare/back-end/data/resumen_evolucion.csv'
data = read_csv(file_path)

headers = data[0]
result = {}

for i, row in enumerate(data[1:], start=1):
    if len(row) != len(headers):
        result[i] = f"Inconsistent data: {row}"
        continue

    validated_row = []
    for j, value in enumerate(row):
        if headers[j] == 'PacienteID' and value != '2':
            break
        elif headers[j] in ['Fecha', 'Hora']:
            validated_value = value
        elif headers[j] in ['PresionSistolica', 'PresionDiastolica']:
            validated_value = validate_range(validate_numeric(value), 0, 300)
        elif headers[j] == 'FrecuenciaCardiaca':
            validated_value = validate_range(validate_numeric(value), 0, 300)
        elif headers[j] == 'Temperatura':
            validated_value = validate_range(validate_numeric(value), 30, 45)
        elif headers[j] == 'FrecuenciaRespiratoria':
            validated_value = validate_range(validate_numeric(value), 0, 100)
        elif headers[j] == 'SaturacionOxigeno':
            validated_value = validate_range(validate_numeric(value), 0, 100)
        elif headers[j] == 'pH':
            validated_value = validate_range(validate_numeric(value), 6.8, 7.8)
        else:
            validated_value = validate_numeric(value)

        if validated_value is None:
            validated_value = f"Anomaly: {value}"
        validated_row.append(validated_value)

    if len(validated_row) == len(headers):
        result[i] = validated_row