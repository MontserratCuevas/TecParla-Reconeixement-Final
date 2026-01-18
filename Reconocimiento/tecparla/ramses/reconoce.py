#! /usr/bin/env python3

import numpy as np
from tqdm import tqdm

from ramses.util import * 
from ramses.prm import * 
from ramses.mod import *
from ramses.euclidio import Euclidio
from ramses.gaussiano import Gauss
from ramses.maxent import MaxEnt
from ramses.gmm import GMM
from ramses.mlp import MLP


def reconoce(dirRec, dirPrm, ficMod, *guiSen, ClsMod=MLP, **kwargs): # ClsMod es Gauss, MaxEnt, GMM o MLP
    """
    Reconoce la unidad cuyo modelo se ajusta mejor
    """
    modelo = MLP(pathMod=ficMod, **kwargs)

    for señal in tqdm(leeLis(*guiSen), ascii="·|/-\\#"):
        pathPrm = pathName(dirPrm, señal, 'prm')
        prm = leePrm(pathPrm)

        reconocida = modelo (prm)

        pathRec = pathName(dirRec, señal, '.rec')
        chkPathName(pathRec)
        with open(pathRec, 'wt') as fpRec: 
            fpRec.write(f'LBO:,,,{reconocida}\n')  

if __name__ == "__main__":
    from docopt import docopt
    import sys

    usage=f"""
Reconoce vocales usando el modelo acústico cargado

usage:
    {sys.argv[0]} [options] <guia> ...
    {sys.argv[0]} -h | --help
    {sys.argv[0]} --version

options:
    -p, --dirPrm PATH      Directorio con las señales parametrizadas [default: .]
    -M, --ficMod PATH      Fichero con el modelo a cargar [default: Mod/vocales.mod]
    -r, --dirRec PATH      Directorio donde se guardarán los resultados [default: .]
    -e, --execPrev SCRIPT  Script de ejecución previa 
    -C, --classMod CLASS   Clase de modelado acústico (GMM, MLP, etc.)
    --n_gauss INT          Número de gaussianas (GMM) [default: 4]
    --n_layers INT         Número de capas (MLP) [default: 2]
    --n_neurons INT        Número de neuronas (MLP) [default: 64]
    --activation STR       Función de activación (MLP) [default: relu]
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

    dirRec = args["--dirRec"]
    dirPrm = args["--dirPrm"]
    ficMod = args["--ficMod"]
    guiSen = args["<guia>"]

    if args["--execPrev"]: exec(open(args["--execPrev"]).read())

    clsMod = eval(args["--classMod"]) if args ["--classMod"] in args else Modelo

    reconoce(dirRec, dirPrm, ficMod, *guiSen, ClsMod=clsMod,**kwargs)



    
