#include <iostream>
#include <string>
#include <chrono>
#include <thread>
#include <cstdlib>
#include <mqtt/client.h> // Inclusion de la libreria cliente de Eclipse Paho MQTT C++

// Definicion de la direccion del broker publico y los parametros de conexion
const std::string SERVER_ADDRESS("tcp://broker.emqx.io:1883");
const std::string CLIENT_ID("cpp_sub_sensors_legacy");

// Declaracion de los topicos oficiales indicados en el PDF de la practica
const std::string TOPIC_GAS("sensor/data/gas_sensor");
const std::string TOPIC_SEN("sensor/data/sen55");

int main(int argc, char* argv[]) {
    // Inicializacion del objeto cliente de MQTT con la configuracion del servidor
    mqtt::client client(SERVER_ADDRESS, CLIENT_ID);
    mqtt::connect_options connOpts;
    
    // Configuramos los intervalos de mantenimiento de conexion activa
    connOpts.set_keep_alive_interval(20);
    connOpts.set_clean_session(true);

    try {
        // Establecemos la conexion inicial con el broker MQTT
        client.connect(connOpts);
        
        // Nos suscribimos de manera explicita a los dos canales de datos de los sensores
        client.subscribe(TOPIC_GAS, 1);
        client.subscribe(TOPIC_SEN, 1);

        // Bucle de ejecucion indefinida que simula el bloqueo del software legado
        while (true) {
            // Bloqueamos la ejecucion hasta que llegue un nuevo mensaje desde el broker
            auto msg = client.consume_message();
            
            // Si el mensaje es valido y se ha recibido correctamente, lo procesamos
            if (msg) {
                // Imprimimos el topico de origen por la salida estandar
                std::cout << "[MSG] Topic: " << msg->get_topic() << std::endl;
                // Imprimimos el contenido del mensaje recibido (payload) por la salida estandar
                std::cout << "Payload: " << msg->to_string() << std::endl;
            }
        }
    }
    catch (const mqtt::exception& exc) {
        // Captura de errores criticos en caso de caida de red o fallo de comunicacion
        std::cerr << "Error de MQTT: " << exc.what() << std::endl;
        return 1;
    }

    return 0;
}