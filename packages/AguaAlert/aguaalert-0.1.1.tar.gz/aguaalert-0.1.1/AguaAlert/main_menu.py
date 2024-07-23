from AguaAlert.pozos import registrar_ubicacion, registrar_precipitacion
from AguaAlert.analisis import analizar_relacion
from AguaAlert.prediccion import predecir_nivel_agua
from AguaAlert.visualizacion import visualizar_datos
from AguaAlert.reportes import generar_reporte

def menu():
    """
    Muestra el menú principal del sistema de predicción de niveles de aguas subterráneas.
    """
    while True:
        print("Sistema de Predicción de Niveles de Aguas Subterráneas")
        print("1. Registrar una nueva ubicación")
        print("2. Registrar datos de precipitación")
        print("3. Analizar relación precipitación-niveles de agua")
        print("4. Predecir nivel de agua")
        print("5. Visualizar datos")
        print("6. Generar reporte")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Ingrese el nombre de la ubicación: ")
            coordenadas = input("Ingrese las coordenadas (lat, long): ")
            niveles = [float(input(f"Ingrese el nivel de agua para el período {i+1}: ")) for i in range(3)]
            print(registrar_ubicacion(nombre, coordenadas, niveles))
        elif opcion == "2":
            nombre = input("Ingrese el nombre de la ubicación: ")
            precipitaciones = [float(input(f"Ingrese la precipitación para el período {i+1} (mm): ")) for i in range(3)]
            print(registrar_precipitacion(nombre, precipitaciones))
        elif opcion == "3":
            analizar_relacion()
        elif opcion == "4":
            nombre = input("Ingrese el nombre de la ubicación para la predicción: ")
            nueva_lluvia = float(input("Ingrese la precipitación prevista (mm): "))
            prediccion = predecir_nivel_agua(nombre, nueva_lluvia)
            if prediccion is not None:
                print(f"El nivel de agua previsto para una precipitación de {nueva_lluvia} mm es {prediccion:.2f} metros.")
            else:
                print(f"No hay datos suficientes para la ubicación: {nombre}")
        elif opcion == "5":
            visualizar_datos()
        elif opcion == "6":
            print(generar_reporte())
        elif opcion == "7":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.\n")

if __name__ == "__main__":
    menu()
