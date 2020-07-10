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


The following table summarizes some other built-in Pandas aggregations:

Aggregation	Description
count()	Total number of items
first(), last()	First and last item
mean(), median()	Mean and median
min(), max()	Minimum and maximum
std(), var()	Standard deviation and variance
mad()	Mean absolute deviation
prod()	Product of all items
sum()	Sum of all items
These are all methods of DataFrame and Series objects.


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