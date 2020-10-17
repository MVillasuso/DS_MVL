import os, sys
from flask import Flask, make_response, request
from flask import render_template, redirect, request, jsonify 
import json
import pandas as pd
import matplotlib.pyplot as plt

# Manejo de imágenes
import imageio
import cv2

# ----------------------
# $$$$$$$ FLASK $$$$$$$$
# ----------------------

app = Flask(__name__)  # init

@app.route("/")  # Default path
def default():
    return """
    <html>
        <body style="background-color: #81bdff;" >
            <h1> Revisión de lesiones cutáneas  (GET) </h1> <p> Modelo para evaluación de lunares o lesiones cutáneas sospechosas <h3> Use     /get/access?tok=</p></h3>
             <h6> Token: LETRA y dígitos del DNI (sin espacios) (Ej.: M12345678) </h6>
        </body>
    </html> """
    #return mensaje

# ----------------------
# $$$$$$$ FLASK GET $$$$$$$$
# ----------------------

@app.route('/get/access', methods=['GET'])
def acceso():

    token_id = None
    if 'tok' in request.args:
        token_id = str(request.args['tok'])
    if token_id == 'E55114370':           #Si el token es válido
        resp = "Nota: Necesitará la foto de su lesión en formato PNG <h3> Use -->    get/pred?mod=lunares <h3>"
        #resp =  atb.preparar_df(jobfile,cfile)      
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
                    <body style="background-color: #81bdff;" >
                        <h2>Evaluación de lesiones cutáneas</h2>
                        <p> Carga la foto de la lesión en formato <b>PNG</b> o <b>JPG</b> y te diremos si debes revisarla con un especialista. </p>
                        <p> <i> La información obtenida es únicamente orientativa y no pretende reemplazar el diagnóstico o la opinión de un profesional </i> </p>
                        <p> <b> NOTA: </b> Este programa no salvará ni almacenará ninguna información en tu computadora.</p>
                        </p>
                        <form action="/predict" method="post" enctype="multipart/form-data">
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

    if ".png" in str(request_file):
        foto = imageio.imread(request_file)
        foto_byn = foto[:, :, 0]       # Foto en Blanco y Negro
        foto_red= cv2.resize(foto_byn,(48,48))   # Foto reducida a 48x48
        plt.imshow(foto_red)
        #plt.show()
        return "Foto cargada"
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

