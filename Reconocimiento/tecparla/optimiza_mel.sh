#!/bin/bash
# optimiza_mel.sh

FIC_CSV="resultados_mfcc.csv"
echo "COF,FILT,ACC" > $FIC_CSV

for nc in 10 13 15 20; do
    for nf in 20 26 32 40; do
        if [ $nf -gt $nc ]; then
            echo "--- Ejecutando: Coefs=$nc, Filtros=$nf ---"
            
            # Ejecutamos tu todo.sh
            bash ramses/todo.sh 0.0001 $nc $nf
            
            # 1. Verificamos si el archivo existe
            if [ -f "Res/uno.res" ]; then
                # 2. Buscamos CUALQUIER número que esté cerca de un símbolo de %
                # Esto es más seguro si "Exact =" no aparece exactamente así
                ACC=$(grep "%" Res/uno.res | head -n 1 | grep -oE "[0-9]+\.[0-9]+")
                
                # Si sigue vacío, probamos a buscar la palabra Exact
                if [ -z "$ACC" ]; then
                    ACC=$(grep "Exact" Res/uno.res | grep -oE "[0-9]+\.[0-9]+")
                fi
            else
                echo "ERROR: No encuentro el archivo Res/uno.res"
                ACC=""
            fi

            # 3. Si al final está vacío, ponemos 0.0
            if [ -z "$ACC" ]; then
                ACC="0.0"
            fi
            
            echo "$nc,$nf,$ACC" >> $FIC_CSV
            echo "Logrado: $ACC %"
        fi
    done
done