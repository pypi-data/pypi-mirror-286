import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def convertir_a_matriz(archivo, columnas):
    """
    Convierte los datos de un archivo CSV a una matriz de Numpy.

    :param archivo: str - Ruta del archivo CSV.
    :param columnas: list - Lista de nombres de columnas a incluir en la matriz.
    :return: np.array - Matriz de Numpy con los datos seleccionados.
    """
    df = pd.read_csv(archivo)
    matriz = df[columnas].values
    return matriz

def predecir_nivel_agua(nombre, nueva_lluvia):
    """
    Predice el nivel de agua para una precipitación prevista en una ubicación específica.

    :param nombre: str - Nombre de la ubicación.
    :param nueva_lluvia: float - Precipitación prevista (mm).
    :return: float - Nivel de agua previsto (metros).
    """
    precipitacion_matriz = convertir_a_matriz('data/precipitacion.csv', ['precip1', 'precip2', 'precip3'])
    ubicaciones_matriz = convertir_a_matriz('data/ubicaciones.csv', ['nivel1', 'nivel2', 'nivel3'])
    
    lluvias = precipitacion_matriz.flatten()
    niveles = ubicaciones_matriz.flatten()
    
    interpolador = interp1d(lluvias, niveles, fill_value="extrapolate")
    prediccion = interpolador(nueva_lluvia)
    return prediccion

