#!/usr/bin/env python3
import os
import re
import matplotlib.pyplot as plt

def procesar_log():
    """Lee el archivo log linea por linea y extrae los datos del sensor sen55."""
    valores = []
    log_path = "mqtt_capture.log"

    # Validamos que el archivo de log exista para evitar excepciones en la lectura
    if not os.path.exists(log_path):
        print(f"Error: No se encuentra el archivo {log_path}")
        return []

    # Abrimos el archivo en modo lectura de forma segura
    with open(log_path, "r") as archivo:
        lineas = archivo.readlines()

    # Recorremos el contenido buscando el topico sen55
    for i in range(len(lineas)):
        if "sensor/data/sen55" in lineas[i]:
            # Si encontramos el topico, comprobamos que la siguiente linea sea el Payload
            if i + 1 < len(lineas) and "Payload:" in lineas[i+1]:
                payload = lineas[i+1]
                # Buscamos el patron numerico despues de la clave MassConcentrationPm1p0
                match = re.search(r'"MassConcentrationPm1p0":\s*([-+]?\d*\.\d+|\d+)', payload)
                if match:
                    # Convertimos el texto a flotante y lo agregamos a nuestra lista de datos
                    valores.append(float(match.group(1)))
    return valores

def generar_grafica_ascii(valores):
    """Genera la representacion en texto plano de las ultimas 20 muestras capturadas."""
    if not valores:
        print("No hay datos disponibles para graficar en ASCII.")
        return

    # Extraemos unicamente las ultimas 20 muestras de la lista para la visualizacion
    muestras = valores[-20:]
    y_min = int(min(muestras))
    y_max = int(max(muestras))

    # Imprimimos las cabeceras de texto requeridas por el formato de entrega
    print("\nMQTT Payload Plot (ASCII)")
    print(f"muestras {len(muestras)}")
    print(f"y_min={y_min}  y_max={y_max} | archivo mqtt_capture.log\n")

    # Imprimimos la linea superior correspondiente al valor maximo del grafico
    print(f" {y_max:3d} |", end="")
    for v in muestras:
        # Si el valor actual es mayor que 50, se dibuja el asterisco arriba
        print(" * " if v > 50 else "   ", end="")
    print()

    # Generamos lineas vacias intermedias para simular la altura de la grafica en la terminal
    for _ in range(3):
        print("     |")

    # Imprimimos la linea inferior correspondiente al valor minimo del grafico
    print(f"   {y_min:d} |", end="")
    for v in muestras:
        # Si el valor actual es menor o igual a 50, se dibuja el asterisco abajo
        print(" * " if v <= 50 else "   ", end="")
    print()

    # Dibujamos el eje X de tiempo de manera proporcional al numero de muestras
    print("     +" + "-" * (len(muestras) * 3))
    print(f"       0" + " " * (len(muestras) * 3 - 9) + f"{len(muestras)-1:2d}\n")

    # Formateamos y mostramos la coleccion con los ultimos 10 valores de la lista
    ultimos_10 = [int(x) for x in muestras[-10:]]
    print(f"Ultimos valores: {', '.join(map(str, ultimos_10))}")

def guardar_grafica_png(valores):
    """Crea una grafica estadistica profesional utilizando matplotlib y la guarda en disco."""
    if not valores:
        return

    # Nos aseguramos de crear el directorio plots/ en caso de que no exista previamente
    os.makedirs("plots", exist_ok=True)

    # Inicializamos una nueva figura estableciendo sus dimensiones en pulgadas
    plt.figure(figsize=(8, 4))
    
    # Trazamos la linea de datos definiendo el color, marcador de puntos y etiqueta
    plt.plot(valores, marker='o', linestyle='-', color='b', label='MassConcentrationPm1p0')
    
    # Configuramos los titulos, etiquetas de los ejes y la cuadricula de fondo
    plt.title('Historico de Datos Capturados via MQTT (SEN55)')
    plt.xlabel('Indice de Muestra')
    plt.ylabel('Valor (PM1.0)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    # Ajustamos los margenes de la imagen de forma automatica para que no se corten los textos
    plt.tight_layout()
    
    # Guardamos el grafico resultante en la ruta establecida y cerramos la instancia de memoria
    plt.savefig("plots/mqtt_plot.png")
    plt.close()

if __name__ == "__main__":
    # Hilo principal de ejecucion: se procesan los logs, se pinta en consola y se genera el archivo png
    datos = procesar_log()
    generar_grafica_ascii(datos)
    guardar_grafica_png(datos)