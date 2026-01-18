#! /bin/bash
# Esto hace que el script siempre se ejecute relativo a su propia carpeta
cd "$(dirname "$0")/.."

NOM=uno
DIR_WRK=.

# Captura de argumentos para las gráficas
EPS=${1:-0.0001}
NUM_COF=${2:-15}
NUM_FILT=${3:-20}
N_GAUSS=${4:-4}
N_LAYERS=${5:-2}      # Valor por defecto: 2 capas
N_NEURONS=${6:-128}    # Valor por defecto: 128 neuronas
ACTIVATION=${7:-relu} # Valor por defecto: relu

DIR_LOG=$DIR_WRK/Log
FIC_LOG=$DIR_LOG/$(basename $0 .sh).$NOM.log
[ -d $DIR_LOG ] || mkdir -p $DIR_LOG

exec > >(tee $FIC_LOG) 2>&1

hostname
pwd
date 

# Ficheros guia
DIR_GUI=$DIR_WRK/Gui
GUI_ENT=$DIR_GUI/train.gui
GUI_DEV=$DIR_GUI/devel.gui

DIR_SEN=$DIR_WRK/Sen
DIR_MAR=$DIR_WRK/Sen
DIR_PRM=$DIR_WRK/Prm/$NOM
DIR_MOD=$DIR_WRK/Mod/$NOM
FIC_MOD=$DIR_MOD/vocales.mod
DIR_REC=$DIR_WRK/Rec/$NOM

LIS_MOD=$DIR_WRK/Lis/vocales.lis

FIC_RES=$DIR_WRK/Res/$NOM.res
# LIMPIEZA DE RUTAS: Borramos para asegurar que el experimento es nuevo
rm -rf $DIR_PRM $DIR_REC
mkdir -p $DIR_PRM $DIR_REC $DIR_MOD
[ -d $(dirname $FIC_RES) ] || mkdir -p $(dirname $FIC_RES)

# Parametrización
dirSen="-s $DIR_SEN"
dirPrm="-p $DIR_PRM"

# Definición de la función de parametrización
FUNK_PRM=mel # Lo dejamos fijado en cepstrum para las de Gauss, en Lpc o en Mel

if [ $FUNK_PRM == periodograma ]; then
    EXEC_PREV=$DIR_PRM/$FUNK_PRM
    echo "import numpy as np" > $EXEC_PREV
    echo "def $FUNK_PRM(x):" >> $EXEC_PREV
    echo "    return 10*np.log10($EPS+abs(np.fft.fft(x))**2)" >> $EXEC_PREV

elif [ $FUNK_PRM == cepstrum ]; then
    EXEC_PREV=$DIR_PRM/$FUNK_PRM
    echo "import numpy as np" > $EXEC_PREV
    echo "def $FUNK_PRM(x):" >> $EXEC_PREV
    echo "    Sx=10*np.log10($EPS+abs(np.fft.fft(x))**2)" >> $EXEC_PREV
    echo "    cepstrum = np.real(np.fft.ifft(Sx))" >> $EXEC_PREV
    echo "    return cepstrum[:$NUM_COF]" >> $EXEC_PREV

elif [ $FUNK_PRM == lpc ]; then
    EXEC_PREV=$DIR_PRM/$FUNK_PRM
    echo "import numpy as np" > $EXEC_PREV
    echo "from scipy.linalg import solve_toeplitz" >> $EXEC_PREV
    echo "def $FUNK_PRM(x):" >> $EXEC_PREV
    echo "    # Ventana de Hamming y Autocorrelación" >> $EXEC_PREV
    echo "    x = x * np.hamming(len(x))" >> $EXEC_PREV
    echo "    r = np.correlate(x, x, mode='full')[len(x)-1:]" >> $EXEC_PREV
    echo "    # Resolución de Yule-Walker para Estimación de Máxima Entropía" >> $EXEC_PREV
    echo "    # El orden del filtro es NUM_COF" >> $EXEC_PREV
    echo "    a = solve_toeplitz(r[:$NUM_COF], r[1:$NUM_COF+1])" >> $EXEC_PREV
    echo "    return a" >> $EXEC_PREV

elif [ $FUNK_PRM == mel ]; then
    NUM_FILT=${3:-26}
    EXEC_PREV=$DIR_PRM/$FUNK_PRM
    echo "import numpy as np" > $EXEC_PREV
    echo "from python_speech_features import mfcc" >> $EXEC_PREV
    echo "def $FUNK_PRM(x):" >> $EXEC_PREV
    echo "    # Calculamos la matriz de MFCC para el segmento x" >> $EXEC_PREV
    echo "    # Usamos nfft=512 para fs=8000Hz" >> $EXEC_PREV
    echo "    f = mfcc(x, samplerate=8000, winlen=0.025, winstep=0.01, \\" >> $EXEC_PREV
    echo "             numcep=$NUM_COF, nfilt=$NUM_FILT, nfft=512, appendEnergy=True)" >> $EXEC_PREV
    echo "    # Si f devuelve varias filas (matriz), calculamos la media" >> $EXEC_PREV
    echo "    # Esto garantiza que devolvemos un único vector de tamaño $NUM_COF" >> $EXEC_PREV
    echo "    if f.ndim > 1:" >> $EXEC_PREV
    echo "        return np.mean(f, axis=0)" >> $EXEC_PREV
    echo "    return f" >> $EXEC_PREV

else 
    echo "Parametrización desconocida ($FUNK_PRM)"
    exit 1
fi

funkPrm="-f $FUNK_PRM"
execPrev="-e $EXEC_PREV"

# Llamadas corregidas usando el módulo de python
EXEC="python3 -m ramses.parametriza $dirSen $dirPrm $funkPrm $execPrev $GUI_ENT $GUI_DEV"
echo $EXEC && $EXEC || exit 1

# Entrenamiento
dirPrm="-p $DIR_PRM"
dirMar="-m $DIR_MAR"
lisUni="-l $LIS_MOD"
ficMod="-M $FIC_MOD"

#EXEC="python3 -m ramses.entrena $dirPrm $dirMar $lisUni $ficMod -C MLP $GUI_ENT" #poner la clase correspondiente(Gauss, MaxEnt, GMM o MLP)
# FORMA CORRECTA: Sin comillas alrededor de las variables de comando
#python3 -m ramses.entrena $dirPrm $dirMar $lisUni $ficMod -C MLP $GUI_ENT -n_layers $N_LAYERS -n_neurons $N_NEURONS -activation $ACTIVATION || exit 1
#echo $EXEC && $EXEC || exit 1
EXEC="python3 -m ramses.entrena $dirPrm $dirMar $lisUni $ficMod -C MLP $GUI_ENT -G $N_GAUSS -N $N_LAYERS -n $N_NEURONS -A $ACTIVATION"
echo $EXEC && $EXEC || exit 1

# Reconocimiento 
dirRec="-r $DIR_REC"
dirPrm="-p $DIR_PRM"
ficMod="-M $FIC_MOD"

EXEC="python3 -m ramses.reconoce $dirRec $dirPrm $ficMod -C MLP $GUI_DEV"
echo $EXEC && $EXEC || exit 1

# Evaluación del resultado 
dirRec="-r $DIR_REC" 
dirMar="-m $DIR_MAR" 

# 1. Creamos la carpeta usando la variable que ya definiste arriba
# Esto asegura que la carpeta exista sea cual sea el valor de $FIC_RES
mkdir -p $(dirname "$FIC_RES")

# 2. Ejecutamos la evaluación. 
echo "--- EVALUACIÓN ---"
# Importante: Usamos comillas por si hay espacios en las rutas
python3 -m ramses.evalua $dirRec $dirMar $GUI_DEV > "$FIC_RES"

# 3. Esperamos un segundo para que el sistema de archivos termine de escribir
sleep 1

# 4. Comprobamos si el archivo existe antes de hacer el cat
echo "--- RESULTADO FINAL ---"
if [ -f "$FIC_RES" ]; then
    cat "$FIC_RES"
else
    echo "ERROR: El archivo $FIC_RES no se ha creado."
fi

date
echo "sacabao, chula"