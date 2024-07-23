import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

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

def analizar_relacion():
    """
    Analiza la relación entre la precipitación y los niveles de agua.

    :return: tuple - Coeficiente y intercepto de la regresión lineal.
    """
    ubicaciones_matriz = convertir_a_matriz('data/ubicaciones.csv', ['nivel1', 'nivel2', 'nivel3'])
    precipitacion_matriz = convertir_a_matriz('data/precipitacion.csv', ['precip1', 'precip2', 'precip3'])
    
    niveles = ubicaciones_matriz.flatten()
    lluvias = precipitacion_matriz.flatten()
    
    X = lluvias.reshape(-1, 1)
    y = niveles
    reg = LinearRegression().fit(X, y)
    
    plt.scatter(lluvias, niveles, label="Datos")
    plt.plot(lluvias, reg.predict(X), label="Tendencia", color="red")
    plt.xlabel("Precipitación (mm)")
    plt.ylabel("Nivel de Agua (metros)")
    plt.legend()
    plt.show()
    
    return reg.coef_[0], reg.intercept_

