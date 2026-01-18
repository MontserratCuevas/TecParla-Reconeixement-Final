#!/bin/bash
# optimiza_gmm.sh

FIC_CSV="resultados_gmm.csv"
echo "N_GAUSS,ACC" > $FIC_CSV

for ng in 1 2 4 8 16 32; do
    echo "--- Probando GMM con $ng Gaussianas ---"
    
    # Ejecución
    bash ramses/todo.sh 0.0001 15 20 $ng
    
    # Esperamos un segundo para asegurar que el archivo se ha cerrado
    sleep 1
    
    # Intentamos localizar el archivo uno.res dinámicamente
    # Esto busca el archivo más reciente llamado uno.res en cualquier subdirectorio
    RES_PATH=$(find . -name "uno.res" -path "*/Res/*" | head -n 1)

    if [ -n "$RES_PATH" ]; then
        # Extraemos el número que va después de "Exact ="
        # Usamos grep -oP para capturar solo el número decimal
        ACC=$(grep "exact =" "$RES_PATH" | grep -oE "[0-9]+\.[0-9]+")
    else
        ACC="0.0"
    fi

    if [ -z "$ACC" ]; then ACC="0.0"; fi
    
    echo "$ng,$ACC" >> $FIC_CSV
    echo "N_Gauss: $ng -> Accuracy: $ACC % (Leído de: $RES_PATH)"
done

echo "Optimización GMM completada. Datos en $FIC_CSV"