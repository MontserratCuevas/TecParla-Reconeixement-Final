import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Cargar los datos generados por tu script de bash
try:
    df = pd.read_csv('resultados_mfcc.csv')
    
    # 2. Pivotar los datos para crear una matriz (Filas: Coeficientes, Columnas: Filtros)
    # Esto organiza los datos para el mapa de calor
    pivot_table = df.pivot(index='COF', columns='FILT', values='ACC')

    # 3. Crear la figura
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="YlGnBu", 
                cbar_kws={'label': 'Exactitud (Accuracy %)'})

    plt.title('Optimización MFCC: Coeficientes vs. Bandas de Filtro', fontsize=15)
    plt.xlabel('Número de Filtros (nfilt)', fontsize=12)
    plt.ylabel('Número de Coeficientes (num_ceps)', fontsize=12)

    # 4. Guardar la gráfica
    plt.savefig('optimizacion_mfcc_heatmap.png')
    print("Gráfica guardada como 'optimizacion_mfcc_heatmap.png'")
    
    # Mostrar cuál es el mejor resultado por consola
    best = df.loc[df['ACC'].idxmax()]
    print(f"\n--- MEJOR CONFIGURACIÓN ---")
    print(f"Coeficientes: {best['COF']}, Filtros: {best['FILT']}, Accuracy: {best['ACC']}%")

except Exception as e:
    print(f"Error al generar la gráfica: {e}")