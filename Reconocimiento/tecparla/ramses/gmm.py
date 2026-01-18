import numpy as np
from scipy.stats import multivariate_normal
import pickle
import os

class GMM:
    def __init__(self, **kwargs):
        # Parámetro a optimizar
        self.n_gauss = int(kwargs.get('n_gauss', 4))
        
        # Estructuras para acumular datos y guardar el modelo
        self.X_list = []
        self.y_list = []
        self.models = {} 
        self.classes = None

        # Carga automática si el fichero de modelo existe
        pathMod = kwargs.get('pathMod', None)
        if pathMod and os.path.exists(pathMod):
            self.lecMod(pathMod)

    def inicMod(self):
        """Limpia los datos acumulados para un nuevo entrenamiento."""
        self.X_list = []
        self.y_list = []

    def __iadd__(self, data):
        """Ramses añade datos con el operador += """
        prm, unidad = data
        # Aseguramos que prm sea 2D (varias tramas por segmento) o promediado
        self.X_list.append(prm)
        self.y_list.append(unidad)
        return self

    def calcMod(self):
        """Entrena el modelo GMM con la inicialización propuesta."""
        X = np.vstack(self.X_list)
        y = np.array(self.y_list)
        self.classes = np.unique(y)
        
        for vocal in self.classes:
            X_vocal = X[y == vocal]
            
            # 1. Covarianza diagonal global de la vocal (punto 5.4 apuntes)
            cov_diag = np.var(X_vocal, axis=0) + 1e-6 
            
            # 2. Inicialización: N señales aleatorias como medias
            # replace=False asegura que no elijamos la misma muestra dos veces
            n_muestras = len(X_vocal)
            n_elegir = min(self.n_gauss, n_muestras)
            indices = np.random.choice(n_muestras, n_elegir, replace=False)
            means = X_vocal[indices]
            
            self.models[vocal] = {
                'means': means, 
                'cov': cov_diag,
                'weight': 1.0 / n_elegir # Peso uniforme para cada gaussiana
            }
        print(f"Modelo GMM entrenado con {self.n_gauss} gaussianas por vocal.")

    def __call__(self, X):
        """Fase de reconocimiento: Clasifica un segmento de audio."""
        if not self.models or self.classes is None:
            return 'a'

        # Aseguramos que X sea al menos 2D para que multivariate_normal no falle
        # (Si es un vector MFCC, lo convierte en una matriz de 1 fila)
        if X.ndim == 1:
            X = X[np.newaxis, :]

        log_probs = np.zeros(len(self.classes))
        
        for i, vocal in enumerate(self.classes):
            m = self.models[vocal]
            
            # Calculamos la probabilidad de cada gaussiana para todas las tramas de X
            # probs_componentes tendrá forma (n_gauss, n_tramas)
            probs_componentes = []
            for mu in m['means']:
                p = multivariate_normal.pdf(X, mean=mu, cov=m['cov'], allow_singular=True)
                probs_componentes.append(p)
            
            # Probabilidad media de la mezcla para cada trama
            # p_mezcla tendrá forma (n_tramas,)
            p_mezcla = np.mean(probs_componentes, axis=0)
            
            # Sumamos log-verosimilitudes de todas las tramas del segmento
            # Añadimos un suelo (1e-20) para evitar log(0)
            log_probs[i] = np.sum(np.log(p_mezcla + 1e-20))
            
        return self.classes[np.argmax(log_probs)]

    def escMod(self, filename):
        """Guarda el modelo en disco."""
        with open(filename, 'wb') as f:
            pickle.dump({'models': self.models, 'classes': self.classes, 'n_gauss': self.n_gauss}, f)

    def lecMod(self, filename):
        """Carga el modelo desde disco."""
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            self.models = data['models']
            self.classes = data['classes']
            self.n_gauss = data['n_gauss']