import pandas as pd

def generar_reporte():
    """
    Genera un reporte de los datos de ubicaciones y precipitaciones.

    :return: str - Mensaje de éxito.
    """
    ubicaciones = pd.read_csv('data/ubicaciones.csv')
    precipitacion = pd.read_csv('data/precipitacion.csv')
    
    with pd.ExcelWriter('reporte.xlsx') as writer:
        ubicaciones.to_excel(writer, sheet_name='Ubicaciones', index=False)
        precipitacion.to_excel(writer, sheet_name='Precipitacion', index=False)
    
    return "Reporte generado con éxito."

