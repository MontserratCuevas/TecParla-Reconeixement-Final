#!/bin/bash

# Función de extracción mejorada para tu estilo de salida
    # Buscamos la línea que contiene 'exact', extraemos el número decimal y cambiamos coma por punto
    # Cambia la función get_acc en tu experimento.sh por esta:
get_acc() {
    # Busca la línea con 'exact =', captura el número con punto y quita el %
    grep -i "exact =" Res/uno.res | grep -oE "[0-9]+\.[0-9]+"
}


echo "--- EXPERIMENTO EPS ---"
echo "EPS Accuracy" > datos_eps.txt

# Valores de EPS para la gráfica
for e in  1000 100 10 1 0.1 0.01 0.001 0.0001; do
    echo "Ejecutando EPS: $e"
    # Llamamos a tu todo.sh. Redirigimos a /dev/null para no saturar la pantalla
    bash ramses/todo.sh $e 13 > /dev/null 2>&1
    
    ACC=$(get_acc)
    echo "$e $ACC" >> datos_eps.txt
    echo "   -> Accuracy: $ACC%"
done

echo "--- EXPERIMENTO COEFICIENTES ---"
echo "COEF Accuracy" > datos_coef.txt

# Valores de Coeficientes para la gráfica
for c in 2 5 10 15 20 30 50 80; do
    echo "Ejecutando COEF: $c"
    bash ramses/todo.sh 0.0001 $c > /dev/null 2>&1
    
    ACC=$(get_acc)
    echo "$c $ACC" >> datos_coef.txt
    echo "   -> Accuracy: $ACC%"
done