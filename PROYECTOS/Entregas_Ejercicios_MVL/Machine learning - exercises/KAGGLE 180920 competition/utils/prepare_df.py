#FUNCIONES PARA PREPARAR UN DATAFRAME PARA APLICA UN MODELO DE ML

# Creada por:  Mónica Villasuso López
# Última actualización: 15/09/2020

# _____________________________________________________________________________________
# IMPORTAR LIBRERIAS
import re           # Módulo Regular Expressions para poder trabajar con caracteres especiales
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
# _____________________________________________________________________________________

def normalize_dataframe(df):
    """ 
    Funcion normalize_dataframe
    Retorna el dataframe de entrada con las columnas numéricas normalizadas
    Argumentos: 
        df: El df a normalizar
    """
    scaler = MinMaxScaler()
    df_normalized = pd.DataFrame(
        data=scaler.fit_transform(df.values), 
        columns=df.columns, 
        index=df.index)
    return df_normalized
# _____________________________________________________________________________________
def transformar_df (df, aplic_encod=True, aplic_norm = True):
    """
    Función transformar_df
    Retorna el dataframe codificado y/o normalizado segun se indique en los argumentos
    """
    if aplic_encod:
        X_categorical_no_numbers = df[df.select_dtypes('object').columns].apply(LabelEncoder().fit_transform)
    else:
        X_categorical_no_numbers=df.select_dtypes('object')

    X_others = df.select_dtypes(exclude=['object'])

    if aplic_norm:
        X_others = normalize_dataframe(df=X_others)

    df_mod = pd.concat([X_categorical_no_numbers,X_others], axis=1)
    return df_mod
# _____________________________________________________________________________________
