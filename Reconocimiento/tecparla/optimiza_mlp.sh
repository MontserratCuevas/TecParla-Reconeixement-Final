#!/bin/bash
# optimizar_neuronales.sh

FIC_CSV="resultados_nn.csv"
echo "CAPAS,NEURONAS,ACT,ACC" > $FIC_CSV

# Parámetros fijos de MFCC (los que mejor te funcionaron)
COF=15
FILT=20

# Bucle de optimización
for capas in 1 2 3; do
    for neuronas in 32 64 128; do
        for act in relu sigmoid; do
            echo "----------------------------------------------------"
            echo "PROBANDO MLP: Capas=$capas | Neuronas=$neuronas | Act=$act"
            echo "----------------------------------------------------"
            
            # Ejecutamos todo.sh pasándole los parámetros
            # El orden sería: todo.sh [alpha] [cof] [filt] [n_gauss] [capas] [neuronas] [activacion]
            bash ramses/todo.sh 0.0001 $COF $FILT 0 $capas $neuronas $act
            
            # Extraemos la exactitud del archivo de resultados (insensible a mayúsculas)
            ACC=$(grep -i "exact =" Res/uno.res | grep -oE "[0-9]+\.[0-9]+")
            
            if [ -z "$ACC" ]; then
                ACC="0.0"
            fi
            
            # Guardamos en el CSV
            echo "$capas,$neuronas,$act,$ACC" >> $FIC_CSV
            echo ">>> RESULTADO: $ACC %"
        done
    done
done

echo "----------------------------------------------------"
echo "Optimización finalizada. Datos guardados en $FIC_CSV"