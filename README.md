# Practica 1: Sistema de Captura, Analisis y Visualizacion de Datos MQTT

Este proyecto implementa un flujo completo para automatizar la monitorizacion de sensores ambientales utilizando el protocolo MQTT. El sistema permite controlar la captura de datos en tiempo real mediante un script en Bash, simulando dispositivos o conectandose a un broker oficial, para posteriormente procesar los registros y generar representaciones graficas tanto en texto plano (consola) como en imagenes estasisticas (PNG).

---

## Descripcion de los Componentes

El repositorio esta organizado con los siguientes archivos:

1. capture.mqtt.sh: Es el script principal de automatizacion en Bash. Solicita al usuario el tiempo de ejecucion, gestiona el proceso del sensor en segundo plano de manera segura mediante el control de senales del sistema (SIGINT, SIGTERM, SIGKILL) y al terminar ejecuta el procesado final de los datos.
2. mqtt_subscribe_emqx: Script escrito en Python que sirve para emular de forma continua el envio de payloads de prueba para sensores de gas (sensor/data/gas_sensor) and particulas (sensor/data/sen55). Es muy util para hacer pruebas en local sin necesidad de un sensor fisico.
3. mqtt_subscribe_emqx.cpp: Cliente escrito en C++ que utiliza la libreria Eclipse Paho MQTT para conectarse al broker publico de EMQX (tcp://broker.emqx.io:1883) y consumir las lecturas reales de los canales de los sensores.
4. plot_mqtt.py: Modulo encargado del analisis y la visualizacion. Lee de forma segura el archivo de texto con las trazas, genera un grafico de dispersion en formato ASCII directo por la terminal y exporta de manera automatica una grafica estadistica lineal utilizando matplotlib.
5. mqtt_capture.log: Archivo de registro historico que almacena de forma temporal o permanente las capturas ordenadas por topicos y payloads durante la monitorizacion activa.

---

## Instrucciones de Ejecucion

### 1. Requisitos Previos

Es necesario contar con las dependencias instaladas en el entorno de desarrollo:

* Python 3.x con la libreria de graficas matplotlib:
  pip install matplotlib

* Compilador C++ y biblioteca Paho MQTT C++ en caso de utilizar el programa nativo.

* Permisos de ejecucion para el script Bash:
  chmod +x capture.mqtt.sh

### 2. Flujo de Trabajo Automatizado

Para iniciar todo el ciclo del sistema (captura, almacenamiento, parseo y renderizado), se ejecuta el script automatizado desde la terminal:

./capture.mqtt.sh

Pasos internos que realiza el script de manera autonoma:
1. Configuracion del Tiempo: Solicita en consola la duracion de la captura en segundos (al pulsar ENTER usa el valor por defecto de 10 segundos).
2. Captura Desacoplada: Lanza el programa suscriptor en segundo plano redirigiendo la salida estandar y de errores al archivo mqtt_capture.log.
3. Control de Vida del Proceso: Monitoriza segundo a segundo que el cliente MQTT siga activo mediante senales de control.
4. Cierre Seguro: Al cumplirse el tiempo, envia de forma escalonada senales de terminacion garantizando que el proceso finalice de forma limpia sin dejar tareas colgadas en el sistema.
5. Generacion de Graficos: Invoca a plot_mqtt.py para visualizar en consola los ultimos valores e inmortalizar el historico en la imagen estadistica.

---

## Visualizacion de Resultados

### Grafica en Terminal (ASCII)
El parseador genera un volcado visual directamente en la linea de comandos tras cada ejecucion exitosa para comprobar los datos rapido sin salir de la consola:

MQTT Payload Plot (ASCII)
muestras 20
y_min=1  y_max=102 | archivo mqtt_capture.log

 102 | * * * * * * |
     |
     |
   1 |   * * * * * * * * +------------------------------------------------------------
       0                                                        19

Ultimos valores: 102, 1, 102, 102, 1, 102, 1, 102, 102, 1

### Grafica Estadistica Profesional
De manera paralela, las metricas completas del sensor de particulas se guardan automaticamente en la carpeta plots bajo el nombre mqtt_plot.png. Esta imagen incluye el trazado lineal completo, leyendas, marcas de puntos por muestra y rejillas de dispersion estilizadas.

---

## Tecnologías Utilizadas
* Bash Linux Scripting: Control de concurrencia, captura de PID y gestion de senales del kernel.
* Python 3: Expresiones regulares (re) para parseado de logs y matplotlib para analitica visual.
* C++11: Cliente Paho MQTT con patrones de consumo sincrono bloqueante.
