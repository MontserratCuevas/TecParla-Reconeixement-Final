import pandas as pd
import matplotlib.pyplot as plt

try:
    # 1. Cargar y ordenar datos
    df = pd.read_csv('resultados_gmm.csv')
    df = df.sort_values('N_GAUSS')

    # 2. Crear la figura
    plt.figure(figsize=(10, 6))
    colores = ['#3498db' if (x < df['ACC'].max()) else '#e74c3c' for x in df['ACC']]
    
    bars = plt.bar(df['N_GAUSS'].astype(str), df['ACC'], color=colores, edgecolor='black', alpha=0.8)

    # 3. Añadir etiquetas de texto sobre las barras
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval}%', 
                 ha='center', va='bottom', fontweight='bold')

    # 4. Estética
    plt.title('Comparativa de Exactitud según el Número de Gaussianas (GMM)', fontsize=14)
    plt.xlabel('Número de Gaussianas (N)', fontsize=12)
    plt.ylabel('Exactitud (Accuracy %)', fontsize=12)
    plt.ylim(0, max(df['ACC']) + 10) # Dar espacio arriba para las etiquetas
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 5. Leyenda personalizada
    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], color='#3498db', lw=4),
                    Line2D([0], [0], color='#e74c3c', lw=4)]
    plt.legend(custom_lines, ['Configuración GMM', 'Mejor Resultado'])

    plt.savefig('grafica_gmm_barras.png', dpi=300)
    print("Gráfica de barras guardada como 'grafica_gmm_barras.png'")

except Exception as e:
    print(f"Error: {e}")