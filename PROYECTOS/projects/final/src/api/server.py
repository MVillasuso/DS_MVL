import os, sys
sys.path.append('/Users/purbina/Desktop/THE_BRIDGE/DS_MVL/PROYECTOS/projects/final/src/utils') 
import io
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, make_response, request
from flask import render_template, redirect, request, jsonify , send_file
# Manejo de imágenes
import imageio
import cv2
from PIL import Image
# Módulos del proyecto
import models_tb as mtb
import folders_tb as ftb
import apis_tb as atb

# ----------------------
# $$$$$$$ FLASK $$$$$$$$
# ----------------------
app = Flask(__name__)  # init

@app.route("/")  # Default path
def default():
    return """
    <html>
        <body style="background-color: #accba1;" >
            <h1> Revisión de lesiones cutáneas  (GET) </h1>     
            <img src= 'f1.png' alt="IMAGEN" width="200" height="200">          
            <p> Modelo para evaluación de lunares o lesiones cutáneas sospechosas <h3> Use     /get/access?tok=</p></h3>
             <h6> Token: LETRA y dígitos del DNI (sin espacios) (Ej.: M12345678) </h6>
        </body>
    </html> """


# ----------------------
# $$$$$$$ FLASK GET $$$$$$$$
# ----------------------

@app.route('/get/access', methods=['GET'])
def acceso():

    token_id = None
    if 'tok' in request.args:
        token_id = str(request.args['tok'])
    if token_id == 'E55114370':           #Si el token es válido
        resp = """
                <html>
                    <body style="background-color: #accba1;" >
                        <h2> Nota: Necesitará la foto de su lesión en formato PNG </h2>
                        <h3> Para ver la predicción     use  -->    get/pred?mod=lunares <h3>  
                        <h3> Para obtener archivo json  use -->    get/pred?mod=json <h3>    
                    </body> 
                </html>"""
        return resp
    else:
        return "Error: Token inválido" + "<br>" + "<br>" + str(request.args)

@app.route('/get/pred', methods=['GET'])
def pred():
    valid = None
    if 'mod' in request.args:
        valid = str(request.args['mod'])
    if valid == 'lunares':           #Si el token es válido
        return """
                <html>
                    <body style="background-color: #accba1;" >
                        <h2>Evaluación de lesiones cutáneas</h2>
                        <p> Sube una foto de la lesión en formato <b>PNG</b> o <b>JPG</b> y te diremos si debes revisarla con un especialista. </p>
                        <p> <i> El resultado es orientativo. No pretende reemplazar el diagnóstico o la opinión de un profesional </i> </p>
                        <p> <h5> <b> NOTA: </b> No se modificará ni almacenará ninguna información en tu ordenador. </h5> </p>
                        </p>
                        <form action="/predict" method="post" enctype="multipart/form-data">
                            <input type="file" name="data_file" />
                            <input type="submit" />
                        </form>
                    </body>
                </html>
            """
    elif valid == "json":
        return """
                <html>
                    <body style="background-color: #accba1;" >
                        <h2>[JSON] Evaluación de lesiones cutáneas</h2>
                        <p> Sube una foto de la lesión en formato <b>PNG</b> o <b>JPG</b>. </p>
                        <p> <i> Devuelve un string en formato JSON con la probabilidad del modelo para cada clase </i> </p>
                        <p> <h5> <b> NOTA: </b> No se modificará ni almacenará ninguna información en tu ordenador. </h5> </p>
                        </p>
                        <form action="/pred_json" method="post" enctype="multipart/form-data">
                            <input type="file" name="data_file" />
                            <input type="submit" />
                        </form>
                    </body>
                </html>
            """
    else:
        return "Error: Token inválido" + "<br>" + "<br>" + str(request.args)


@app.route('/predict', methods=["POST"])
def get_pred():
    request_file = request.files['data_file']
    if not request_file:
        return "No hay archivo seleccionado"
    if ".png"  in str(request_file) :
        foto=ftb.preparar_imagen(request_file,48)
        foto_r= ftb.formatear_imagen(foto,48)
        class_names = ['Sospechoso','Benigno']
        ubicacion = "/Users/purbina/Desktop/THE_BRIDGE/DS_MVL/PROYECTOS/projects/final/modelos"
        model_name = "Model_0.82609_16-18-16"
        modelo = mtb.cargar_modelo (ubicacion, model_name)
        prediccion = atb.prediccion_imagen(modelo, foto_r, class_names, imagen_orig=None)
        respuesta= """
                <html>
                    <body style="background-color: #9cab97;" > 
                        <h4> Imagen de caracter </h4>
                         <p> <h3>"""+ prediccion  + """ </h3> <p> 
                    </body>
                </html> """
        return respuesta
    else :
        return "Seleccione un formato de archivo válido (.png o .jpg)"

@app.route('/pred_json', methods=["POST"])
def get_pred_json():
    request_file = request.files['data_file']
    if not request_file:
        return "No hay archivo seleccionado"
    if ".png"  in str(request_file) :
        foto=ftb.preparar_imagen(request_file,48)
        foto_r= ftb.formatear_imagen(foto,48)
        class_names = ['Sospechoso','Benigno']
        ubicacion = "/Users/purbina/Desktop/THE_BRIDGE/DS_MVL/PROYECTOS/projects/final/modelos"
        model_name = "Model_0.82609_16-18-16"
        modelo = mtb.cargar_modelo (ubicacion, model_name)
        prediccion = atb.pred_json(modelo,foto_r,class_names)
        #<img src="""+ im_path + """ alt="IMAGEN" width="500" height="600">
        respuesta= """
                <html>
                    <body style="background-color: #9cab97;" > 
                        <p> <h3>"""+ prediccion + """ </h3> <p> 
                    </body>
                </html> """
        return respuesta
    else :
        return "Seleccione un formato de archivo válido (.png o .jpg)"

# ----------------------
# $$$$$$$ MAIN $$$$$$$$
# ----------------------

def main():

    print("STARTING PROCESS")
    print(os.path.dirname(__file__))
    
    # Get the settings fullpath
    settings_file = os.path.dirname(__file__) + "/settings.json"
    # Load json from file 
    with open(settings_file, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)
    
    # Load variables from jsons
    SERVER_RUNNING = json_readed["server_running"]
    
    if SERVER_RUNNING:
        DEBUG = json_readed["debug"]
        HOST = json_readed["host"]
        PORT_NUM = json_readed["port"]
        app.run(debug=DEBUG, host=HOST, port=PORT_NUM)
    else:
        print("Server settings.json doesn't allow to start server. " + "Please, allow it to run it.")
            

if __name__ == "__main__":
    main()

