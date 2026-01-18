import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
import pickle
import os

# 1. Cargar el modelo que acabas de entrenar
FICHERO_MODELO = 'Mod/uno/vocales.mod'

if not os.path.exists(FICHERO_MODELO):
    print(f"Error: No encuentro el archivo {FICHERO_MODELO}. ¿Has ejecutado el todo.sh?")
    exit()

with open(FICHERO_MODELO, 'rb') as f:
    datos = pickle.load(f)
    # En MaxEnt, los pesos representan la contribución de cada coeficiente LPC a la clase
    pesos = datos['weights']  # Matriz de (Orden x 5 vocales)
    clases = datos['classes']

# Configuración de la figura (2 filas x 3 columnas)
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

# Colores para la comparativa
colores = ['r', 'g', 'b', 'm', 'c']
frecuencias_hz = np.linspace(0, 4000, 512) # Asumiendo muestreo a 8kHz

# 2. Generar las gráficas
for i, vocal in enumerate(['a', 'e', 'i', 'o', 'u']):
    # Buscar el índice de la vocal en el modelo
    idx = np.where(clases == vocal)[0][0]
    w_vocal = pesos[:, idx]
    
    # Calcular respuesta en frecuencia (Envoltura LPC)
    # El filtro es 1 / (1 - sum(a_k * z^-k))
    # Importante: Usamos los pesos como coeficientes del filtro
    a = np.concatenate(([1], -w_vocal))
    w, h = freqz(1, a, worN=512)
    modulo_db = 20 * np.log10(np.abs(h))
    
    # Gráfica individual
    axes[i].plot(frecuencias_hz, modulo_db, color=colores[i], linewidth=2)
    axes[i].set_title(f'Modelo de la Vocal /{vocal}/', fontsize=14, fontweight='bold')
    axes[i].set_xlabel('Frecuencia (Hz)')
    axes[i].set_ylabel('Ganancia (dB)')
    axes[i].grid(True, alpha=0.3)
    
    # Añadir a la sexta gráfica (comparativa)
    axes[5].plot(frecuencias_hz, modulo_db, color=colores[i], label=f'/{vocal}/', alpha=0.7)

# 3. Configurar la sexta gráfica (Comparativa)
axes[5].set_title('Comparación de las 5 Vocales', fontsize=14, fontweight='bold')
axes[5].set_xlabel('Frecuencia (Hz)')
axes[5].set_ylabel('Ganancia (dB)')
axes[5].legend()
axes[5].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('modelos_vocales_maxent.png')
print("¡Figura guardada como 'modelos_vocales_maxent.png'!")