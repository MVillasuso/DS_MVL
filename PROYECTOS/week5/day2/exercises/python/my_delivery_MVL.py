import pandas as pd
import matplotlib
from functools import wraps

key_url = "http://winterolympicsmedals.com/medals.csv"

#Para probar si grafica un df con más de una columna numérica usar la siguiente url
#key_url = "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/02_Filtering_&_Sorting/Euro12/Euro_2012_stats_TEAM.csv"

def histo_cols (datf):
    tip_num = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    newdf = datf.select_dtypes(include=tip_num)
    for elem in list(newdf.columns):  #Para todas las columnas numéricas ...
        datf.hist(elem)                 #.... presentar un histograma

def prepost(url):
    def inner(function):
        @wraps(function)
        def wrapper(*a, **k):               #Args y Kwargs 
            if url:
                df = pd.read_csv (url)
                retval = function(*a, **k)      #Args y Kwargs (los mismos que pasa wrapper)
                histo_cols(df)
            else:
                retval = None
            return retval
        return wrapper
    return inner

@prepost(url=key_url)   
def _f_protected():
    l1 = [ l for l in range(16)]    # Creación de lista con list comprehension
    mayor_5_lambda = list(filter(lambda x: x >5 , l1))  # Lambda function y filter de la lista
    return mayor_5_lambda           # Retorna la lista filtrada con los mayores a 5

