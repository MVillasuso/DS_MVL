import os, sys
from flask import Flask, render_template, redirect, request, jsonify 
import json
# import mean_group_d as mg


# ----------------------
# $$$$$$$ FLASK $$$$$$$$
# ----------------------

app = Flask(__name__)  # init

@app.route("/")  # Default path
def default():
    mensaje = " <h1> DataScience Jobs API  (GET) </h1> <p> Datos resumidos sobre la oferta laboral en Datascience según www.glassdoor.com <h3>     /get/df?tok=</p></h3>"
    mensaje +=  "<br>" + " <h6> Token: LETRA y dígitos del DNI (sin espacios) (Ej.: M12345678) </h6>"
    return mensaje

# ----------------------
# $$$$$$$ FLASK GET $$$$$$$$
# ----------------------

@app.route('/get/df', methods=['GET'])
def api_df():
    """"
    Recibe como argumento un token. Si es válido (según las especificaciones), retorna un archivo resumido y depurado con los datos de oferta laboral en 
    DataScience según  GlassDoor.com
    """
    token_id = None
    if 'tok' in request.args:
        token_id = str(request.args['tok'])
    if token_id == 'E55114370':           #Si el token es válido
        #resp =  mg.t_d_mean (url, country_l)            # Obtener la media diaria de total_deaths para esos países
        #return resp
        return  "Resumen glassdoor - Oferta de trabajo en DataScience" 
    else:
        return "Error: Token inválido" + "<br>" + "<br>" + str(request.args)

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