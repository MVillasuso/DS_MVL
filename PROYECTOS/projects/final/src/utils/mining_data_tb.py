import os
# Manejo de imágenes
import imageio
import cv2

def preparar_datos (path_ini,ruta_img,dir_a ="gray",dir_b = "resize", dimen=48):
    """
    Toma las imágenes y las graba en disco segun lo siguiente:
    dir_a: Directorio con las imágenes guardadas en  Blanco y Negro 
    dir_b: Directorio dentro de dir_a con las imágenes en Blanco y Negro Redimensionadas segun dimen
    """
    os.chdir(path_ini)
    os.chdir (ruta_img)
    # Archivos de imágenes. Excluye .DS_Store
    lfiles =  [f for f in os.listdir('.') if (os.path.isfile(f)) and (not f.startswith('.'))] 
    os.mkdir(dir_a)
    direc = dir_a+"/"+dir_b
    os.mkdir(direc)
    for elem in lfiles:
        im = imageio.imread(elem)
        im_name = dir_a +'/'+ elem.split(".")[0] + 'g.jpg'
        imageio.imwrite(im_name, im[:, :, 0])  
        # Lee la imagen que acaba de convertir a ByN
        im2=imageio.imread(im_name) 
        #redimensiona a 48x48
        imageio.imwrite(direc+ '/'+ elem.split(".")[0] + 'g_r.jpg', cv2.resize(im2, (dimen, dimen) ) ) 
    os.chdir(path_ini)


def lista_img (Xlist, y_list, y_val, path_ini,ruta_img):
    os.chdir(path_ini)
    os.chdir(ruta_img)
    lfiles = [f for f in os.listdir('.') if (os.path.isfile(f)) and (not f.startswith('.'))] 
    for file in lfiles:
        imagen = imageio.imread(file)
        Xlist.append(imagen)
        y_list.append(y_val)     #  1 = "Benigno" , 0 = "Sospechoso o Maligno"
    os.chdir(path_ini)
    return Xlist, y_list