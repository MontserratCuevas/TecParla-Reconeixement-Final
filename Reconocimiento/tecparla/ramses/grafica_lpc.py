import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar los datos
try:
    df = pd.read_csv('resultados_lpc.csv')
except FileNotFoundError:
    print("Error: No se encuentra 'resultados_lpc.csv'. Ejecuta primero el experimento.")
    exit()

# 2. Configurar la estética
plt.figure(figsize=(10, 6))
plt.plot(df['Orden_LPC'], df['Accuracy'], marker='o', linestyle='-', color='#2c3e50', linewidth=2, markersize=8)

# 3. Añadir títulos y etiquetas
plt.title('Optimización del Orden LPC para Reconocimiento de Vocales (MaxEnt)', fontsize=14)
plt.xlabel('Orden del Análisis LPC (p)', fontsize=12)
plt.ylabel('Exactitud (Accuracy %)', fontsize=12)

# 4. Personalizar el eje y cuadrícula
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(df['Orden_LPC']) # Asegura que se vean todos los órdenes probados

# 5. Guardar e informar
plt.savefig('grafica_lpc.png', dpi=300)
print("¡Gráfica generada con éxito como 'grafica_lpc.png'!")