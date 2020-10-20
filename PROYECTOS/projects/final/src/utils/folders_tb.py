# Módulo con funciones para el procesamiento de imágenes
import os
import pandas as pd 
import matplotlib.pyplot as plt
# Manejo de imágenes
import cv2
import imageio

from tensorflow.keras.preprocessing.image import ImageDataGenerator ,img_to_array

def leer_imagen (ubicacion,nombre):
    if ubicacion:
        ruta = ubicacion + "/" + nombre
    else:
        ruta=nombre
    im = imageio.imread(ruta)
    return im

def guardar_imagen (imagen, ubicacion,nombre):
    ruta = ubicacion + "/" + nombre
    imageio.imwrite(ruta,imagen)
    return 

def preparar_imagen (imagen, dimension):
    """
        Recibe un archivo en formato .png 
        Convierte el archivo de entrada en formato Blanco y Negro y Reduce su tamaño a las dimensiones 
        (pixels) especificadas (cuadrada)
        Retorna la foto modificada
    """
    imagen_orig=imageio.imread(imagen)
    img_byn = imagen_orig[:, :, 0]       # Foto en Blanco y Negro
    img_red= cv2.resize(img_byn,(dimension,dimension))   # Foto reducida a 48x48
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

def generar_imagenes (imagen, cantidad, ubicacion, prefijo, formato):
    """
    Crea la cantidad de imágenes indicada (cantidad) usando Keras ImageDataGenerator.
    Las imágenes son guardadas en el directorio "ubicacion" con el prefijo y la extensión (formato)
    indicados coo argumento.
    Ejemplo: 
    generar_imagenes (imag,3,ubic,"im_", "png") Crea en el directorio ubic, 3 variaciones de imagen con
    prefijo im_*.png
    """
    augmenter = ImageDataGenerator(horizontal_flip=True,
        rotation_range=30, 
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.2,
        shear_range=0.1,
        fill_mode='nearest')

    x = img_to_array(imagen)  # la imagen original convertida a Numpy array
    x = x.reshape((1,) + x.shape)  # Numpy array con shape (1, 293,360,4)
    i = 0
    for batch in augmenter.flow(x, batch_size=1, save_to_dir=ubicacion, save_prefix=prefijo, save_format=formato):
        i += 1
        if i > cantidad:
            break  # Detiene el generador luego de 10 imágenes para que no  itere indefinidamente
    return

def cargar_csv(fname):
    df = pd.read_csv(fname)
    df.set_index("Unnamed: 0", inplace=True)
    df.index.name = None
    return df

def salvar_plot (dir_name, f_name):
    """
    Guarda el archivo como .PNG en el directorio indicado
    """
    results_dir = os.path.join(dir_name) 
    if not os.path.isdir(results_dir): 
        os.makedirs(results_dir) 
    plt.savefig(results_dir + f_name,bbox_inches='tight') 
