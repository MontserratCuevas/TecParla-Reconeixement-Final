import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar los datos desde tu archivo
try:
    df = pd.read_csv('resultados_nn.csv')
    # Limpiamos posibles espacios en los nombres de las columnas
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    print("Error: No se encuentra 'resultados_nn.csv'.")
    exit()

# Configuramos el estilo visual
sns.set_theme(style="whitegrid")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

# --- GRÁFICA 1: Evolución por Activación y Neuronas ---
# Mostramos cómo crecen Relu y Sigmoid según el tamaño de la red
sns.lineplot(data=df, x='NEURONAS', y='ACC', hue='ACT', style='CAPAS', 
             markers=True, dashes=False, linewidth=2.5, ax=ax1)

ax1.set_title('Evolución de Precisión: Neuronas vs Capas', fontsize=15, pad=15)
ax1.set_xlabel('Neuronas por Capa', fontsize=12)
ax1.set_ylabel('Accuracy (%)', fontsize=12)
ax1.legend(title='Activación / Capas', bbox_to_anchor=(1.05, 1), loc='upper left')

# --- GRÁFICA 2: Heatmap de Rendimiento (Solo para ReLU) ---
# El Heatmap es ideal para ver la "zona caliente" de mejores resultados
df_relu = df[df['ACT'] == 'relu'].pivot(index="CAPAS", columns="NEURONAS", values="ACC")
sns.heatmap(df_relu, annot=True, fmt=".2f", cmap="YlGnBu", ax=ax2, cbar_kws={'label': 'Accuracy %'})

ax2.set_title('Mapa de Calor: Rendimiento ReLU (Capas vs Neuronas)', fontsize=15, pad=15)
ax2.set_xlabel('Neuronas por Capa', fontsize=12)
ax2.set_ylabel('Número de Capas', fontsize=12)

plt.tight_layout()
plt.savefig('analisis_mlp_profesional.png', dpi=300)
print("¡Hecho! Gráficas guardadas en 'analisis_mlp_profesional.png'")
plt.show()