#!/bin/bash

# Solicitamos al usuario de forma interactiva el tiempo de ejecucion en segundos
read -p "Indique el tiempo de captura en segundos (default: 10): " SEGUNDOS

# Si el usuario pulsa ENTER sin introducir un numero, asignamos 10 segundos por defecto
SEGUNDOS=${SEGUNDOS:-10}

# Definimos el nombre del archivo donde se almacenaran las salidas del programa
LOG_FILE="mqtt_capture.log"

# Mostramos por pantalla los datos de la ejecucion que va a comenzar
echo "[1/4] Ejecutando ./mqtt_subscribe_emqx y guardando salida en $LOG_FILE durante ${SEGUNDOS}s..."

# Lanzamos el ejecutable en segundo plano usando el caracter &
# Redirigimos la salida estandar y la de errores al archivo de log (2>&1)
./mqtt_subscribe_emqx > "$LOG_FILE" 2>&1 &

# Capturamos inmediatamente el identificador de proceso (PID) del programa que acabamos de lanzar
BIN_PID=$!

# Imprimimos el PID capturado para tener constancia del proceso en el sistema
echo "[INFO] BIN_PID=$BIN_PID"

# Inicializamos una variable contador para controlar la duracion del bucle
SEGUNDOS_TRANSCURRIDOS=0

# Bucle de control: se repite segundo a segundo hasta alcanzar el tiempo solicitado
while [ $SEGUNDOS_TRANSCURRIDOS -lt $SEGUNDOS ]; do
    # Pausamos la ejecucion del script durante 1 segundo
    sleep 1
    
    # Comprobamos si el proceso sigue vivo enviando la senal 0
    # Si kill devuelve un codigo de error, significa que el proceso se ha caido solo
    if ! kill -0 $BIN_PID 2>/dev/null; then
        echo "[ALERTA] El proceso con PID $BIN_PID termino inesperadamente antes de tiempo."
        break
    fi
    
    # Incrementamos el contador en una unidad
    ((SEGUNDOS_TRANSCURRIDOS++))
done

# Iniciamos la fase de finalizacion controlada del proceso del sensor
echo "[2/4] Deteniendo proceso (pid=$BIN_PID)..."

# Verificamos si el proceso sigue en ejecucion antes de enviarle senales de terminacion
if kill -0 $BIN_PID 2>/dev/null; then
    # Enviamos una senal SIGINT (equivalente a pulsar Ctrl+C) para un cierre limpio
    kill -2 $BIN_PID 2>/dev/null
    sleep 0.5
    
    # Si el proceso no ha respondido a la primera senal, enviamos un SIGTERM (terminacion estandar)
    if kill -0 $BIN_PID 2>/dev/null; then
        kill -15 $BIN_PID 2>/dev/null
        sleep 0.5
        
        # Si el proceso sigue bloqueado o no responde, forzamos su cierre inmediato con SIGKILL
        if kill -0 $BIN_PID 2>/dev/null; then
            kill -9 $BIN_PID 2>/dev/null
        fi
    fi
fi

# Mostramos el mensaje indicando que comienza el procesamiento de los datos guardados
echo "[3/4] Parseando datos desde '$LOG_FILE' y graficando en terminal..."

# Bloque incrustado de Python requerido por la practica para demostrar la integracion de lenguajes
python3 <<'PY'
print("Hola mundo desde Python ejecutado dentro de Bash")
PY

# Invocamos el script externo de Python que realizara el analisis matematico y los graficos
python3 plot_mqtt.py

# Mensajes de cierre para confirmar que toda la automatizacion ha concluido con exito
echo "[4/4] Listo"
echo "Log guardado en: $LOG_FILE"