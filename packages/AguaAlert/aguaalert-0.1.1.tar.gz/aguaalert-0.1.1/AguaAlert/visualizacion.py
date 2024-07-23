import pandas as pd
import matplotlib.pyplot as plt

def visualizar_datos():
    """
    Visualiza los datos de precipitación y niveles de agua.
    """
    ubicaciones = pd.read_csv('data/ubicaciones.csv')
    precipitacion = pd.read_csv('data/precipitacion.csv')
    
    for nombre in ubicaciones['nombre'].unique():
        niveles = ubicaciones[ubicaciones['nombre'] == nombre].iloc[:, 2:].values.flatten()
        lluvias = precipitacion[precipitacion['nombre'] == nombre].iloc[:, 1:].values.flatten()
        
        plt.plot(lluvias, niveles, 'o-', label=f"Ubicación: {nombre}")
    
    plt.xlabel("Precipitación (mm)")
    plt.ylabel("Nivel de Agua (metros)")
    plt.legend()
    plt.show()

