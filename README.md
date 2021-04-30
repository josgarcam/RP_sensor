#Monitorización de la temperatura y humedad con RP

## Configuración
* Clonar el repositorio en `home/pi/`. El resultado sería: `/home/pi/RP_sensor`.
* Ejecutar el archivo **configuration.sh**. Este instalará todas las dependencias necesarias además de configurar el arranque automático de la API y el script de medición.
* Editar el fichero **"/RP_sensor/Measurement/config.ini"**:
    * EndTime hace referencia a la fecha en la que se detendrá la medición.
    * EndPoint incluye la URL en la que la API recibe los datos.
    * Period es el tiempo de espera entre medición en segundos.
    * IDs es el indentificador de la RP con el que se guardarán las mediciones.
    * Sensors incluye el identificador de cada sensor y los pines GPIO de la placa en los que están conectados.
    
    ![GPIO](https://3.bp.blogspot.com/-JP3Tk-L49Ek/WDGfB2wxXnI/AAAAAAAABGI/RIDVDTBtnjgtEZ22QlaKzyrCKrzSuMkrQCEw/s1600/GPIO-RP3.png)

## Notas
* Para evitar que el programa arranque en el inicio tan solo es necesario eliminar el fichero `/home/pi/.config/autostart/xyz.desktop`.
* Para iniciarlo manualmente se puede ejecutar `RP_sensor/start.sh`.