import signal
import os
from time import sleep, time
from datetime import datetime
from configparser import ConfigParser
#import ping3
import requests
import sqlite3

SUCCESSFUL_POST = 1
UNSUCCESSFUL_POST = 2

config = ConfigParser()
config.read("config.ini")

end_date = datetime(year=config.getint('EndTime', 'Year'),
                    month=config.getint('EndTime', 'Month'),
                    day=config.getint('EndTime', 'Day'),
                    hour=config.getint('EndTime', 'Hour'),
                    minute=config.getint('EndTime', 'Minute'),
                    second=config.getint('EndTime', 'Second'))

#ping3.EXCEPTIONS = True


def read(id_sensor, obj_sensor):
    temperature, humidity = None, None
    while temperature is None or humidity is None:
        try:
            temperature, humidity = obj_sensor.temperature, obj_sensor.humidity
            sleep(0.1)

        except ValueError:
            sleep(0.1)

        except RuntimeError as error:
            #print(f'[{str(datetime.now())[:19]}] - ', error.args[0])
            temperature, humidity = None, None

    data = {"id_rp": config.getint('IDs', 'RP'),
            "id_sensor": id_sensor,
            "temperature": temperature,
            "humidity": humidity,
            "measured_date": datetime.now()}
    print('\033[94m', f'[{str(datetime.now())[:19]}] - Sensor: ', id_sensor, ' - Lectura tomada:     ', data, '\033[0m')

    return data


def send(data, check_ping=True):
    try:
        #if check_ping:
            #ping3.ping(config['Database']['IP_DB_Postgres'])
        response = requests.post(config['EndPoint']['url'], data, timeout=3)
        response.raise_for_status()
        
        if response.status_code == requests.codes.ok:
            return SUCCESSFUL_POST
        else:
            return UNSUCCESSFUL_POST

    #except (requests.exceptions.RequestException, ping3.errors.PingError):
    except (requests.exceptions.RequestException): 
        return UNSUCCESSFUL_POST


def sensor_process(id_sensor, obj_sensor, process_db_pid):

    try:
        while datetime.now() < end_date:

            start = time()
            data = read(id_sensor, obj_sensor)

            signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGINT])

            response = send(data)
            if response == SUCCESSFUL_POST:
                print('\033[92m' + f'[{str(datetime.now())[:19]}] - Sensor: ', id_sensor,
                      ' - Lectura enviada con éxito' + '\033[0m')
                os.kill(process_db_pid, signal.SIGALRM)

            elif response == UNSUCCESSFUL_POST:
                db_save(data)
                print('\033[93m' + f'[{str(datetime.now())[:19]}] - Sensor: ', id_sensor,
                      ' - Envío sin éxito: lectura guardada en local' + '\033[0m')

            signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGINT])

            sleep(config.getfloat('Period', 't') - (time() - start))

    except KeyboardInterrupt:
        return


def db_save(data):
    con = sqlite3.connect(config['Database']['DB_File'])
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO dht11(timestamp, id_rp, id_sensor, temperature, humidity) VALUES(?, ?, ?, ?, ?)",
                      (data["measured_date"], data["id_rp"], data["id_sensor"], data["temperature"], data["humidity"]))
    con.commit()
    cursorObj.close()


def db_update():
    signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGALRM])
    con = sqlite3.connect(config['Database']['DB_File'])
    

    try:
        while datetime.now() < end_date:
            
            signum = signal.sigwait([signal.SIGALRM, signal.SIGINT])
            if signum == signal.SIGINT:
                return
            
            cursorObj = con.cursor()
            cursorObj.execute("SELECT * from dht11 ORDER BY id_measurement")
            rows = cursorObj.fetchall()

            if rows:
                print('\033[92m' + f'[{str(datetime.now())[:19]}] - Transmitiendo datos en local' + '\033[0m')
                for row in rows:
                    sleep(0.5)
                    data = {"measured_date": row[1],
                            "id_rp": row[2],
                            "id_sensor": row[3],
                            "temperature": row[4],
                            "humidity": row[5]}

                    signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGINT])

                    response = send(data, check_ping=False)
                    if response == SUCCESSFUL_POST:
                        cursorObj.execute("DELETE FROM dht11 WHERE id_measurement=?", (row[0],))
                        con.commit()
                        print(f'[{str(datetime.now())[:19]}] - Lectura recuperada: ', data)

                    elif response == UNSUCCESSFUL_POST:
                        cursorObj.close()
                        print(
                            '\033[93m' + f'[{str(datetime.now())[:19]}] - Transmisión incompleta de los datos en local' + '\033[0m')
                        return

                    signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGINT])

                print('\033[92m' + f'[{str(datetime.now())[:19]}] - Transmisión completa de los datos en local con éxito' + '\033[0m')

            cursorObj.close()
            
        return

    except KeyboardInterrupt:
        cursorObj.close()
        return
