import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

def prediccion_imagen (modelo, imagen, cnames, imagen_orig=None):
    """
        Recibe el modelo, la imagen a predecir, los nombres de las clases y la imagen a mostrar
        Muestra la imagen
        Calcula la predicción según el modelo y retorna un string con el resultado para mostrarlo por pantalla
        (incluyendo la probabilidad)
    """
    y_pred = modelo.predict(imagen)
    pred_df = pd.DataFrame(y_pred)
    pred_df.columns = cnames
    json_df = pred_df.to_json()
    if imagen_orig:
        plt.figure(figsize=(3,3))
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(imagen_orig) #,  cmap=plt.cm.binary)
        plt.show()
    res_pred = cnames[np.where(max(y_pred[0])==y_pred[0])[0][0]] 
    result =  res_pred.upper() + " (" + str(round(max(y_pred[0])*100,2))+ "%)"
    if y_pred[0][0] > y_pred[0][1]:  # Lesión Sospechosa
        result += " Recomendamos acudir a un especialista para su revisión."
    return result

def pred_json (modelo, imagen, cnames):
    """
        Recibe el modelo, la imagen a predecir, los nombres de las clases 
        Calcula la predicción según el modelo y la retorna en formato json 
    """
    y_pred = modelo.predict(imagen)
    pred_df = pd.DataFrame(y_pred)
    pred_df.columns = cnames
    json_df = pred_df.to_json()
    return json_df