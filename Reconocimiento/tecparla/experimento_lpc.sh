#!/bin/bash

echo "Orden_LPC,Accuracy" > resultados_lpc.csv
echo -e "Orden\tAccuracy\n-----\t--------" > tabla_lpc.txt

# El orden típico en voz es 2 + (Frec_Muestreo / 1000)
# Probamos un rango amplio para ver el "pico" de rendimiento
for orden in 6 8 10 12 14 16 20 24 30; do
    echo -n "Probando Orden LPC $orden... "
    
    # Llamamos a todo.sh con EPS=0, el Orden actual y la función 'lpc'
    bash ramses/todo.sh 0 $orden lpc > /dev/null 2>&1
    
    # Extraemos el valor
    ACC=$(grep -i "exact =" Res/uno.res | grep -oE "[0-9]+\.[0-9]+")
    
    echo "$orden,$ACC" >> resultados_lpc.csv
    echo -e "$orden\t$ACC%" >> tabla_lpc.txt
    echo "OK ($ACC%)"
done

echo "Resultados listos en resultados_lpc.csv y tabla_lpc.txt"