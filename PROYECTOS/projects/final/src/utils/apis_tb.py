import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import folders_tb as f_tb
import imageio

def predic_imagen (modelo, pimagen, cnames, modif= False, mostrar=False, rjson=False):
    """
        Recibe el modelo, la imagen a predecir, los nombres de las clases 
        Un booleano si la imagen debe modificarse
        Un booleano si la imagen se quiere  mostrar
        Un booleano si se desea la predicción en formato json, si no la revuelve como string
        Calcula la predicción según el modelo 
    """
    if modif:
        foto_red = f_tb.preparar_imagen(pimagen,48)
        imagen = f_tb.formatear_imagen(foto_red,48)
    else:
        imagen = pimagen
    y_pred = modelo.predict(imagen)
    if rjson:
        pred_df = pd.DataFrame(y_pred)
        pred_df.columns = cnames
        json_df = pred_df.to_json()
        result = json_df
    else:
        res_pred = cnames[np.where(max(y_pred[0])==y_pred[0])[0][0]] 
        result =  res_pred.upper() + " (" + str(round(max(y_pred[0])*100,2))+ "%)"
        if y_pred[0][0] > y_pred[0][1]:  # Lesión Sospechosa
            result += " - Acuda a un especialista para su revisión."
        if mostrar:     
            img =imageio.imread(pimagen)
            plt.figure(figsize=(3,3))
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.title (result)
            plt.imshow(img) #,  cmap=plt.cm.binary)
    return result