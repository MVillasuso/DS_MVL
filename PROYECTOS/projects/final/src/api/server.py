import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../utils") )
import io
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, make_response
from flask import render_template, redirect, request, jsonify , send_file, url_for
# Manejo de imágenes
import imageio
import cv2
from PIL import Image
from datetime import datetime
# Módulos del proyecto
import models_tb as mtb
import folders_tb as ftb
import apis_tb as atb
import random
import string

# ----------------------
# $$$$$$$ FLASK $$$$$$$$
# ----------------------
app = Flask(__name__)  # init
uploads_dir = os.path.join(os.path.dirname(__file__), 'static/uploads')
MODEL_NAME=""

@app.route("/")  # Default path
def default():
    message = "Token: LETRA y dígitos del DNI (sin espacios) (Ej.: M12345678)" 
    return render_template('index.html', message=message)

# ----------------------
# $$$$$$$ FLASK GET $$$$$$$$
# ----------------------

@app.route('/get/access', methods=['GET'])
def acceso():
    token_id = None
    if 'tok' in request.args:
        token_id = str(request.args['tok'])
    if token_id == 'E55114370':           #Si el token es válido
        return render_template('access.html')
    else:
        return "Error: Token inválido" + "<br>" + "<br>" + str(request.args)

@app.route('/get/pred', methods=['GET'])
def pred():
    valid = None
    if 'mod' in request.args:
        valid = str(request.args['mod'])
    if valid == 'vista':           #Si el token es válido
        return render_template('vista.html')
    elif valid == "json":
        return render_template('json.html')
    else:
        return "Error: Token inválido" + "<br>" + "<br>" + str(request.args)

@app.route('/predict', methods=["POST"])
def get_pred():
    request_file = request.files['data_file']
    rand_name = "img_".join(random.choice(string.ascii_letters) for i in range(2)) + ".png"
    img_path = os.path.join("/uploads", rand_name)
    img_name = os.path.join(uploads_dir, rand_name)
    request_file.save(img_name)
    if not request_file:
        return "No hay archivo seleccionado"
    if ".png"  in str(request_file) :
        class_names = ['Sospechoso','Benigno']
        ubicacion=  os.path.join(os.path.dirname(__file__), "../../modelos")
        model_name= MODEL_NAME
        modelo = mtb.cargar_modelo (ubicacion, model_name)
        prediccion = atb.predic_imagen(modelo, img_name, class_names, modif=True, mostrar=False, rjson=False)
        return render_template("pred_vista.html", prediccion=prediccion, rfoto=img_path)
    else :
        return "La imagen debe estar en formato .png"

@app.route('/pred_json', methods=["POST"])
def get_pred_json():
    request_file = request.files['data_file']
    if not request_file:
        return "No hay archivo seleccionado"
    if ".png"  in str(request_file) :
        class_names = ['Sospechoso','Benigno']
        ubicacion=  os.path.join(os.path.dirname(__file__), "../../modelos")
        model_name= MODEL_NAME
        modelo = mtb.cargar_modelo (ubicacion, model_name)
        prediccion = atb.predic_imagen(modelo, request_file, class_names, modif=True, mostrar=False, rjson=True)
        return render_template( "pred_json.html", prediccion=prediccion)
    else :
        return "Seleccione un formato de archivo válido (.png)"

# ----------------------
# $$$$$$$ MAIN $$$$$$$$
# ----------------------

def main():

    print("STARTING PROCESS")
    print(os.path.dirname(__file__))

    global MODEL_NAME

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
        MODEL_NAME = json_readed["model_name"]
        app.run(debug=DEBUG, host=HOST, port=PORT_NUM)
    else:
        print("Server settings.json doesn't allow to start server. " + "Please, allow it to run it.")
            

if __name__ == "__main__":
    main()

