# DATA CLEANSING  - FUNCIONES PARA MANIPULAR Y LIMPIAR DATA

# Funciones de manipulación y limpieza de strings de datos 
# Creada por:  Mónica Villasuso López
# Última actualización: 12/07/2020

# _____________________________________________________________________________________
# IMPORTAR LIBRERIAS
import re           # Módulo Regular Expressions para poder trabajar con caracteres especiales
import pandas as pd
# _____________________________________________________________________________________
# Clean_Strings
""" Funcion clean_strings
    Retorna una lista con el string de entrada SIN los caracteres especiales a eliminar
    Argumentos: 
        string: El string a depurar 
"""
def clean_strings(strings):     
    result = []
    cadena = ""
    for value in strings:
        value = value.strip()
        value = re.sub('[!#?]', '', value)
        result.append(value)
    cadena = "".join(result)
    return cadena

#Test
#prueba = "Esto es una prueba!! para elimin#ar caract?eres especiales de un te##xto"
#final_str = clean_strings (prueba)
#print(final_str)

# _____________________________________________________________________________________
# Normalize 
""" Función normalize 
    Retorna el string de entrada eliminando los acentos 
    Argumentos: 
        s: El string del cual se eliminarán los acentos 
"""

def normalize(s):           
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


#Test
#print(normalize("¡Hólá, múndó!"))
#print(normalize("¡HÓLÁ, MÚNDÓ!"))

# _____________________________________________________________________________________
# Dollarizer
""" Función dollarizer 
    Elimina el signo monetario al principio de un string y convierte el resto a float 
    Argumentos: 
        s: El string del cual se eliminará el signo monetario y se retornará como  float  
           (Ej.el string $4.32 y retorna el float  4.32 )
    Nota:  Se puede aplicar a toda  una columna de un dataframe para convertirla así df.col = df.col.apply(dollarizer)
"""

dollarizer = lambda x: float(x[1:])

#Test
#result = dollarizer("$4.32") 
#print("Resultado:",  result, "Tipo ", type(result))

# _____________________________________________________________________________________