#!/bin/bash

echo "Iniciando API"
lxterminal --working-directory=/home/pi/RP_sensor/API/controller/ --command="python3 main.py"
echo "Esperando para empezar a medir"
sleep 10
echo "Iniciando sensores"
lxterminal --working-directory=/home/pi/RP_sensor/Measurement/ --command="python3 main.py"
echo "Fin"