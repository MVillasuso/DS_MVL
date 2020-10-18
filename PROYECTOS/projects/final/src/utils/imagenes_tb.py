# Módulo con funciones para el procesamiento de imágenes

# Manejo de imágenes
import imageio
import cv2

import numpy as np 
import matplotlib.pyplot as plt

def leer_imagen (ubicacion,nombre):
    if ubicacion:
        ruta = ubicacion + "/" + nombre
    else:
        ruta=nombre
    im = imageio.imread(ruta)
    return im

def guardar_imagen (imagen, ubicacion,nombre):
    ruta = ubicacion + "/" + nombre
    im = imageio.imwrite(ruta,imagen)
    return


def preparar_imagen (imagen, dimension):
    """
        Recibe un archivo en formato .png 
        Convierte el archivo de entrada en formato Blanco y Negro y Reduce su tamaño a las dimensiones            (pixels) especificadas (cuadrada)
        Retorna la foto modificada
    """
    imagen_orig=imageio.imread(imagen)
    img_byn = imagen_orig[:, :, 0]       # Foto en Blanco y Negro
    img_red=cv2.resize(img_byn,(dimension,dimension))   # Foto reducida a 48x48
    return img_red

def formatear_imagen (imagen, dimension):
    """
        Recibe un archivo en formato .png 
        Normaliza las dimensiones del array que representa la imagen (div / 255)
        Redimensiona la imagen  con  el formato requerido para la predicción
        Retorna la imagen modificada
    """
    img_normaliz=imagen.astype('float32')    
    img_normaliz /=255             #Foto normalizada
    imagen_nr =img_normaliz.reshape(1,dimension, dimension, 1)     #Reshape para la predicción 
    return imagen_nr

def prediccion_imagen (modelo, imagen, cnames, imagen_orig=None):
    """
        Recibe el modelo, la imagen a predecir, los nombres de las clases y la imagen a mostrar
        Muestra la imagen
        Calcula la predicción según el modelo y la muestra (incluyendo la probabilidad)
    """
    y_pred = modelo.predict(imagen)
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