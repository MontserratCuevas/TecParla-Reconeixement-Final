import numpy as np
from scipy.optimize import fmin_l_bfgs_b
from scipy.special import logsumexp
import pickle
import os

class MaxEnt:
    def __init__(self, **kwargs):
        self.weights = None
        self.classes = None
        self.X_list = []
        self.y_list = []
        pathMod = kwargs.get('pathMod', None)
        if pathMod and os.path.exists(pathMod):
            self.lecMod(pathMod)

    def inicMod(self):
        self.X_list = []
        self.y_list = []

    def __iadd__(self, data):
        prm, unidad = data
        # prm debe ser un vector (1D), no una matriz
        self.X_list.append(prm)
        self.y_list.append(unidad)
        return self

    def calcMod(self):
        if not self.X_list: return
        X = np.vstack(self.X_list)
        y = np.array(self.y_list)
        self.classes, y_indices = np.unique(y, return_inverse=True)
        n_features = X.shape[1]
        n_classes = len(self.classes)
        initial_weights = np.zeros(n_features * n_classes)
        res = fmin_l_bfgs_b(self._cost_function, initial_weights, 
                           args=(X, y_indices, n_classes), approx_grad=True, maxiter=100)
        self.weights = res[0].reshape((n_features, n_classes))
        print(f"Entrenamiento finalizado. Clases: {self.classes}")

    def _cost_function(self, w_flat, X, y_indices, n_classes):
        X = np.atleast_2d(X)
        n_samples, n_features = X.shape
        w = w_flat.reshape((n_features, n_classes))
        scores = np.dot(X, w)
        log_prob_matrix = scores - logsumexp(scores, axis=1, keepdims=True)
        return -np.mean(log_prob_matrix[np.arange(n_samples), y_indices])

    def predict_log_proba(self, X):
        X = np.atleast_2d(X)
        if self.weights is None:
            return np.zeros((X.shape[0], len(self.classes) if self.classes is not None else 5))
        scores = np.dot(X, self.weights)
        if scores.ndim == 1: scores = scores.reshape(1, -1)
        return scores - logsumexp(scores, axis=1, keepdims=True)

    def __call__(self, X):
        if self.classes is None:
            self.classes = np.array(['a', 'e', 'i', 'o', 'u'])
        if X is None or len(X) == 0:
            return self.classes[0]
        log_probs = self.predict_log_proba(X)
        total_log_probs = np.sum(log_probs, axis=0)
        return self.classes[np.argmax(total_log_probs)]

    def escMod(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump({'weights': self.weights, 'classes': self.classes}, f)

    def lecMod(self, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            self.weights = data['weights']
            self.classes = np.array(data['classes'])