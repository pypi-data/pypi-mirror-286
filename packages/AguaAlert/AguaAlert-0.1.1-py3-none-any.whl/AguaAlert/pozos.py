import pandas as pd
import os

def registrar_ubicacion(nombre, coordenadas, niveles):
    """
    Registra una nueva ubicación y sus niveles de agua.

    :param nombre: str - Nombre de la ubicación.
    :param coordenadas: str - Coordenadas de la ubicación (latitud, longitud).
    :param niveles: list - Lista de niveles históricos de agua (3 valores).
    :return: str - Mensaje de éxito.
    """
    file_path = 'data/ubicaciones.csv'
    new_data = pd.DataFrame([[nombre, coordenadas] + niveles], columns=["nombre", "coordenadas", "nivel1", "nivel2", "nivel3"])
    
    if not os.path.isfile(file_path):
        new_data.to_csv(file_path, mode='w', header=True, index=False)
    else:
        new_data.to_csv(file_path, mode='a', header=False, index=False)
    
    return f"Ubicación '{nombre}' registrada exitosamente."

def registrar_precipitacion(nombre, precipitaciones):
    """
    Registra datos históricos de precipitación para una ubicación.

    :param nombre: str - Nombre de la ubicación.
    :param precipitaciones: list - Lista de datos históricos de precipitación (3 valores).
    :return: str - Mensaje de éxito.
    """
    file_path = 'data/precipitacion.csv'
    new_data = pd.DataFrame([[nombre] + precipitaciones], columns=["nombre", "precip1", "precip2", "precip3"])
    
    if not os.path.isfile(file_path):
        new_data.to_csv(file_path, mode='w', header=True, index=False)
    else:
        new_data.to_csv(file_path, mode='a', header=False, index=False)
    
    return f"Datos de precipitación para '{nombre}' registrados."
