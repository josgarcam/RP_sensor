#!/usr/bin/env python3
from datetime import datetime
from Rp_sensor_misc import sensor_process, config, db_update
from multiprocessing import Process
from time import sleep
import signal
import os
import board
import adafruit_dht


# Se obtienen los objetos sensores
sensors = dict()
for sensor in config['Sensors']:
    sensors.update({int(sensor): adafruit_dht.DHT11(getattr(board, config['Sensors'][sensor]))})


print('Para detener el proceso pulse Ctrl+C \n\n')


# Se genera un proceso para volcar la base de datos en local
processes = {}
proc = Process(target=db_update, name='Process_Db_Update')
proc.start()
processes.update({'DB': proc})

# Se genera un proceso por cada sensor
for (id_sensor, obj_sensor) in sensors.items():
    proc = Process(target=sensor_process, args=(id_sensor, obj_sensor, processes['DB'].pid), name='Process_Sensor_'+str(id_sensor))
    sleep(2)
    proc.start()
    processes.update({id_sensor: proc})

try:
    # Espera a que llegue la fecha de finalización de todos los procesos de sensores
    for (key, proc) in processes.items():
        if not key == 'DB':
            proc.join()
            print(f'[{str(datetime.now())[:19]}] - El proceso', proc.name, 'ha terminado')

    # Termina del proceso de volcado de la base de datos
    os.kill(processes['DB'].pid, signal.SIGINT)
    processes['DB'].join()

except KeyboardInterrupt:
    print('\033[91m' + f'[{str(datetime.now())[:19]}] - Proceso interrumpido' + '\033[0m')

    # Notifica al resto de procesos que deben terminar
    for proc in processes.values():
        os.kill(proc.pid, signal.SIGINT)
    print(f'[{str(datetime.now())[:19]}] - Procesos notificados para terminar')

    # Espera que todos los procesos terminen
    for proc in processes.values():
        print(f'[{str(datetime.now())[:19]}] - Esperando a que termine el procesos:', proc.name)
        proc.join()
        print(f'[{str(datetime.now())[:19]}] - El proceso', proc.name, 'ha terminado')

finally:
    print(f'[{str(datetime.now())[:19]}] - Todos los procesos han terminado')
    print(f'[{str(datetime.now())[:19]}] - Desconexión de los sensores')
    for obj_sensor in sensors.values():
        obj_sensor.exit()



