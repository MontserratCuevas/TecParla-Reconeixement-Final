#! /usr/bin/env python3

import numpy as np
from tqdm import tqdm

from ramses.util import *
from ramses.prm import * 
from ramses.mar import * 
from ramses.mod import *
from ramses.euclidio import Euclidio
from ramses.gaussiano import Gauss
from ramses.maxent import MaxEnt
from ramses.gmm import GMM
from ramses.mlp import MLP

def entrena(dirPrm, dirMar, lisUni, ficMod, *ficGui, ClsMod=MLP, **kwargs): #dependiendo de la clase de entenamiento, ponemos Gauss,MaxEnt, GMM, MLP añadimos **kwargs para que pueda coger mas parámetros con MLP
    """
    Entrena el modelo acústico
    """
    unidades = leeLis(lisUni)

    # Inicializamos el modelo 
    modelo = MLP(lisMod=lisUni, **kwargs)

    # Inicializamos el entrenamiento 
    modelo.inicMod()

    # Bucle para todas las señales de entrenamiento 
    for señal in tqdm(leeLis(*ficGui)): 
        # leemos la señal y el contenido del fichero de marcas
        pathPrm = pathName(dirPrm, señal, 'prm')
        prm = leePrm(pathPrm)
        pathMar = pathName(dirMar, señal, 'mar')
        unidad =cogeTrn(pathMar)

        #Actualizamos la información del entrenamiento 
        modelo += prm, unidad

    # Recalculamos el modelo 
    modelo.calcMod()

    # Escribimos el modelo resultante
    modelo.escMod(ficMod)   

if __name__ == "__main__":
    from docopt import docopt
    import sys

    usage=f"""
Entrena un modelo acústico para el reconocimento de las vocales

usage:
    {sys.argv[0]} [options] <guia> ...
    {sys.argv[0]} -h | --help
    {sys.argv[0]} --version

options:
    -p, --dirPrm PATH      Directorio con las señales parametrizadas [default: .]
    -m, --dirMar PATH      Directorio con el fonético de las señales [default: .]
    -l, --lisUni PATH      Fichero con la lista de unidades [default: Lis/vocales.lis]
    -M, --ficMod PATH      Fichero con el modelo resultante [default: Mod/vocales.mod]
    -e, --execPrev SCRIPT  Script de ejecución previa 
    -C, --classMod CLASS   Clase de modelado acústico
    -G --n_gauss INT       Número de gaussianas [default: 4]
    -N --n_layers INT       Número de capas de la red [default: 2]
    -n --n_neurons INT     Número de neuronas por capa [default: 64]
    -A --activation STR    Función de activación (relu/sigmoid) [default: relu]
"""
    
    args = docopt(usage, version="tecparla2025")
    
    # Creamos el diccionario de parámetros extra (kwargs)
    kwargs = {}

    # --- MAPEADO PARA GMM ---
    n_gauss = args.get('-G') or args.get('--n_gauss') or 4
    kwargs['n_gauss'] = int(n_gauss)

    # --- MAPEADO PARA MLP ---
    # Capturamos n_layers (N)
    if args.get('--n_layers'): 
        kwargs['n_layers'] = int(args['--n_layers'])
    elif args.get('-N'):
        kwargs['n_layers'] = int(args['-N'])

    # Capturamos n_neurons (n)
    if args.get('--n_neurons'): 
        kwargs['n_neurons'] = int(args['--n_neurons'])
    elif args.get('-n'):
        kwargs['n_neurons'] = int(args['-n'])

    # Capturamos activation (A)
    if args.get('--activation'): 
        kwargs['activation'] = args['--activation']
    elif args.get('-A'):
        kwargs['activation'] = args['-A']



    dirPrm = args["--dirPrm"]
    dirMar = args["--dirMar"]
    lisUni = args["--lisUni"]
    ficMod = args["--ficMod"]
    ficGui = args["<guia>"]
    
    clsMod = eval(args["--classMod"]) if args["--classMod"] else Modelo
    
    # Pasamos kwargs
    entrena(dirPrm, dirMar, lisUni, ficMod, *ficGui, ClsMod=clsMod, **kwargs)


