import pandas as pd
import numpy as np

 
def elim_cols(df):

    """ 
    Retorna un DF con un subconjunto de las columnas del DF de entrada (seleccionado únicamente las columnas con información relevante
    o con  datos )) y las renombra para más facilidad en su uso 
    """

    newdf=df.loc[:,['gaTrackerData.empSize', 'header.easyApply','header.employerName', 'header.jobTitle',
       'header.posted', 'header.salaryHigh', 'header.salaryLow','job.description', 'job.jobSource', 'map.country',
        'map.lat', 'map.lng', 'map.location','overview.foundedYear', 'overview.industry',
       'overview.revenue', 'overview.sector', 'overview.size','overview.type']]

    newdf = newdf.rename(columns={'gaTrackerData.empSize':'empSize','header.easyApply':'easyApply', 
    'header.employerName':'empName', 'header.jobTitle': 'jobTitle', 'header.posted': 'jobDate', 
    'header.salaryHigh':'salHigh','header.salaryLow':'salLow', 'job.description': 'jobDesc', 
    'job.jobSource':'jobSource', 'map.country':'country','map.lat': 'lat', 'map.lng': 'long', 'map.location': 'location', 
    'overview.foundedYear': 'foundedYear','overview.industry':'industry', 'overview.revenue': "revenue",
    'overview.sector':'sector', 'overview.size': 'size', 'overview.type':'type'})

    return newdf

def transf_cols(df):
    """
    Cambia el tipo de dato a fecha y actualiza ciertas columnas a formato title para su facil manipulacion y visualización
    """
    df["jobDate"] = pd.to_datetime(df["jobDate"])
    lista_cols= ['empName','jobTitle','location', 'industry', 'sector', 'type']
    for elem in lista_cols:
        df[elem]=df[elem].str.title()
    return df

def norm_country(df, names_df):
    """"
    Estandarización de los datos relacionados al país
    """
    # Estandarizar como país United Kingdom cuando en la location se indique que la ciudad pertenece a England 
    # (había diferentes valores en la columna country  (United Kingdom, UK, GBR, England, GB, gb) 
    list_Eng = df[(df["location"].str.contains(", England", na=False))].index.to_list()
    df["country"][df.index.isin (list_Eng)] = "GB"

    # Estandarizar valores pertenecientes a United States
    df["country"][df.country.isin (["US", "United States", "USA"])] = "US"
    df["country"][((df["location"].str.contains(",", na=False))) & (df["country"].isnull())] = "US"

    # Asignar el valor de location a la columna country cuando esta sea nula
    df["country"][df.country.isnull()] = df["location"]

    # Actualizaciom para estandarizar registros de India
    df["country"][df.country.isin (["India", "IN"])] = "IN"

    # Estandarizacion de códigos de países y nombres con info del df de códigos
    df=pd.merge(df, names_df, left_on='country', right_on='Name', how = "left")
    df=pd.merge(df, names_df, left_on='country', right_on='Code', how = "left")
    df['Code_x'] = np.where(df['Code_x'].isnull(), df['Code_y'], df['Code_x'])
    df['Name_x'] = np.where(df['Name_x'].isnull(), df['Name_y'], df['Name_x'])
    df.drop(columns=["Name_y", "Code_y"], inplace = True)
    df.rename(columns={"Name_x":"cname", "Code_x":"ccode"}, inplace=True)

    return df

def ubicar_loc (df):
    """
    Función para asignar pais a localizaciones (45000 aprox)sin este valor que existan en otros registros con valor único 
    en el dataframe
    """
    #Eliminar las filas que contienen location null
    df.drop(df[df.location.isnull()].index, inplace=True)

    #Buscar las location que cumplan esta condicion (5788 en total)
    regs_df= df.loc[:,[ "location", "cname","ccode"]]
    regs_df.drop_duplicates(inplace=True)
    regs_df.dropna(inplace=True)
    a = (regs_df.location.value_counts()>1).to_frame()
    a.drop(a[(a.location == False)].index, inplace=True)
    regs_df.drop(regs_df[regs_df.location.isin (a.index)].index, inplace=True)

    # Merge para asignar valor al pais cuando la localizacion ya exista con valor unico
    df=pd.merge(df, regs_df, on='location', how="left")

    df['ccode_x'] = np.where(df['ccode_x'].isnull(), df['ccode_y'], df['ccode_x'])
    df['cname_x'] = np.where(df['cname_x'].isnull(), df['cname_y'], df['cname_x'])
    df.drop(columns=["cname_y", "ccode_y"], inplace = True)
    df.rename(columns={"cname_x":"cname", "ccode_x":"ccode"}, inplace=True)
    #Elimina los registros de los cuales no pudo determinar la localizacion (6.000 aprox)
    df.drop(df[df.ccode.isnull()].index, inplace=True)

    return df

def experience (df):
    """
    Calcula la experiencia segun algunos valores indicados en JobTitle
    """
    df["exp"]= np.where(df.jobTitle.str.contains('Senior|Sr.|Director'), "Senior","")
    df["exp"]= np.where((df.jobTitle.str.contains('Junior|Jr.')), "Junior", df.exp)
    df["exp"]= np.where((df.jobTitle.str.contains('Internship|Apprentice|Summer|Intern,')), "Internship", df.exp)
    return df

def level(df):
    """
    Calcula el nivel de responsabilidad segun algunos valores indicados en JobTitle
    """
    df["level"]= np.where((df.jobTitle.str.contains('Assistant')), "Assistant", "")
    df["level"]= np.where((df.jobTitle.str.contains('Analyst')), "Analyst", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Management|Mgmt|Controller|Lead|Coord|Project')), "PMO", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Technical|Engineer|Ingénieur')), "Technical", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Dba|Admin|Database')), "Dba", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Scientist|Stat|Math')), "Scientist", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Research')), "Research", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Developer|Programmer')), "Developer", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Product')), "Product", df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Consult')), "Consultant", df.level)
    df["level"]= np.where(df.jobTitle.str.contains('Manager'), "Manager",df.level)
    df["level"]= np.where((df.jobTitle.str.contains('Director')), "Director",df.level)
    return df

def jobType (df):
    """
    Calcula el tipo de perfil demandado relacionado con Data Science  segun lo especificado en JobTitle
    """
    df["jobType"]= np.where(df.jobTitle.str.contains('Learning|Ai |Deep|Ml |Artific'), "ML ","")
    df["jobType"]= np.where((df.jobTitle.str.contains('Data') & df.jobTitle.str.contains('Analyst|Analist') ), "DA", df.jobType)
    df["jobType"]= np.where((df.jobTitle.str.contains('Business|Intelligence|Bi ') & df.jobTitle.str.contains('Analyst') ), "BA", df.jobType)
    df["jobType"]= np.where((df.jobTitle.str.contains('Data Scien')), "DS", df.jobType)
    df["jobType"]= np.where((df.jobTitle.str.contains('Data Engineer|Big Data')), "DE", df.jobType)
    return df
