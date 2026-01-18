import matplotlib.pyplot as plt

def generar_grafica(archivo, titulo, xlabel, es_log=False):
    x, y = [], []
    with open(archivo, 'r') as f:
        next(f) # Saltar cabecera
        for line in f:
            parts = line.split()
            if len(parts) == 2:
                x.append(float(parts[0]))
                y.append(float(parts[1]))
    
    plt.figure()
    if es_log: plt.xscale('log')
    plt.plot(x, y, marker='o', linestyle='-')
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel('Accuracy (%)')
    plt.grid(True)
    plt.savefig(archivo.replace('.txt', '.png'))

generar_grafica('datos_coef.txt', 'Efecto de Coeficientes', 'Número de Coeficientes')
generar_grafica('datos_eps.txt', 'Efecto de EPS (Escala Log)', 'Valor de EPS', es_log=True)
print("Gráficas generadas: datos_coef.png y datos_eps.png")