import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pickle
import os

class MLP(nn.Module):
    def __init__(self, **kwargs):
        super(MLP, self).__init__()
        # Parámetros que vamos a optimizar
        self.n_layers = int(kwargs.get('n_layers', 2))
        self.n_neurons = int(kwargs.get('n_neurons', 64))
        self.activation_str = kwargs.get('activation', 'relu').lower()
        
        self.network = None
        self.classes = None
        self.X_train = []
        self.y_train = []

        # Si existe el modelo, lo cargamos (fase reconocimiento)
        pathMod = kwargs.get('pathMod', None)
        if pathMod and os.path.exists(pathMod):
            self.lecMod(pathMod)

    def inicMod(self):
        self.X_train, self.y_train = [], []

    def __iadd__(self, data):
        prm, unidad = data
        self.X_train.append(prm)
        self.y_train.append(unidad)
        return self

    def calcMod(self):
        # 1. Preparar datos (convertir a tensores de PyTorch)
        X = torch.tensor(np.vstack(self.X_train), dtype=torch.float32)
        self.classes, y_indices = np.unique(self.y_train, return_inverse=True)
        y = torch.tensor(y_indices, dtype=torch.long)

        # 2. Construir la arquitectura dinámicamente
        act_func = nn.ReLU() if self.activation_str == 'relu' else nn.Sigmoid()
        layers = []
        input_dim = X.shape[1]
        
        curr_dim = input_dim
        for _ in range(self.n_layers):
            layers.append(nn.Linear(curr_dim, self.n_neurons))
            layers.append(act_func)
            curr_dim = self.n_neurons
        
        layers.append(nn.Linear(curr_dim, len(self.classes))) # Capa de salida (5 vocales)
        self.network = nn.Sequential(*layers)

        # 3. Entrenamiento (Bucle de optimización)
        optimizer = optim.Adam(self.network.parameters(), lr=0.001)
        criterion = nn.CrossEntropyLoss()
        
        self.network.train()
        for epoch in range(150): # 150 épocas suelen bastar
            optimizer.zero_grad()
            outputs = self.network(X)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
        
        print(f"MLP entrenado: Capas={self.n_layers}, Neuronas={self.n_neurons}, Act={self.activation_str}")

    def __call__(self, X):
        self.network.eval()
        with torch.no_grad():
            if X.ndim == 1: X = X[np.newaxis, :]
            X_tensor = torch.tensor(X, dtype=torch.float32)
            outputs = self.network(X_tensor)
            # Promediamos las salidas si hay varias tramas y elegimos la clase mayoritaria
            avg_output = torch.mean(outputs, dim=0)
            idx = torch.argmax(avg_output).item()
        return self.classes[idx]

    def escMod(self, filename):
        # Guardamos la estructura y los pesos
        with open(filename, 'wb') as f:
            pickle.dump({'network': self.network, 'classes': self.classes, 
                         'config': (self.n_layers, self.n_neurons, self.activation_str)}, f)

    def lecMod(self, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            self.network = data['network']
            self.classes = data['classes']