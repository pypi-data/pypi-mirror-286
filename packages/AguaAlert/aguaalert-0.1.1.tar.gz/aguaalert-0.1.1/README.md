# AguaAlertEC

![](logo.png)

AguaAlert está dirigido a los Gobiernos Autónomos Descentralizados Municipales, universidades y demás instituciones que necesiten una evaluación rápida de los principales cauces de una ciudad afectada por las lluvias intensas y con la cual podrán generar acciones inmediatas y a largo plazo para la recuperación de estas zonas frente a las afectaciones identificadas.

Es un paquete para la gestión y análisis de datos de niveles de aguas subterráneas y precipitaciones. Incluye funcionalidades para registrar datos, analizarlos y realizar predicciones basadas en modelos de regresión.

## Instalación

Puedes instalar el paquete usando:
!pip install AguaAlert

## Funcionamiento de los módulos
* pozos.py

Registra una nueva ubicación y sus niveles de agua históricos.

Registra datos históricos de precipitación para una ubicación.

* analisis.py

Convierte los datos de un archivo CSV a una matriz de Numpy.

Analiza la relación entre la precipitación y los niveles de agua.

* prediccion.py

Convierte los datos de un archivo CSV a una matriz de Numpy.

Predice el nivel de agua para una precipitación prevista en una ubicación específica.

* reportes.py

Genera un reporte con un resumen de los datos registrados.

* visualizacion.py

Visualiza los datos registrados mediante gráficos.

* main_menu.py

Muestra el menú principal del sistema de predicción de niveles de aguas subterráneas.