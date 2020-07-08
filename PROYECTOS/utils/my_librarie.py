# Librería de funciones 


# Para definir una función que está pendiente por desarrollar
def Funcion ()
    # TODO (@desarrollador) Escribir lo que va a hacer la función
    pass


def prueba(a):
    print(a)
    return a + " OK "

test1 = prueba ("Hola")
print (test1)

# FUNCIONES PARA MANIPULAR Y LIMPIAR DATA

import re

def clean_strings(strings):
    result = []
    for value in strings:
        value = value.strip()
        value = re.sub('[!#?]', '', value)
        value = value.title()
        result.append(value)
    return result