# Módulo con funciones para cargar y guardar los modelos predictivos en la ruta especificada
import os
import json
import time
from tensorflow.keras.models import model_from_json  # Cargar los modelos guardados


def guardar_modelo (modelo, ruta, test_acc):
    """
    Guarda el modelo y los pesos por separado. EL primer valor del nombre del archivo del modelo 
    (test_acc)es el % de accuracy que alcanzó con el conjunto de test
    """
    #os.chdir(ruta)
    moment=time.localtime()
    name=ruta + "/"+'Model_{}_{}-{}-{}'.format(round(test_acc,5),moment[2],moment[3],moment[4])
    modelo.save(name)
    model_json = modelo.to_json()
    with open(name+'.json', "w") as json_file:
        json.dump(model_json, json_file)
    modelo.save_weights(name+'.h5')
    return

def cargar_modelo (ruta, nombre):
    """
    Carga un modelo guardado previamente en la ruta indicada y lo retorna
    El modelo debe estar almacenado con extensión .json y los pesos con extensión .h5
    """
    #os.chdir(ruta)
    model_name=ruta + "/"+ nombre + ".json"
    model_weigths = ruta + "/"+ nombre + ".h5"
    
    with open(model_name,'r') as f:
        model_json = json.load(f)

    modelo = model_from_json(model_json)
    modelo.load_weights(model_weigths)
    return modelo
