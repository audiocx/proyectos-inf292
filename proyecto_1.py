from random import *
from math import *

#Cantidad de estudiantes
#m = int(input('Cantidad de estudiantes: '))
m = 5
#Cantidad de ayudantias
#n = int(input('Cantidad de ayudantias: '))
n = 5

#Posibles horas demandadas por cada ayudantia
dc = [7, 8, 15]

#Listas de ofertas (si), demandas (dj) y preferencias (cij)
si = []
dj = []
cij = []

M = 100000
#Posibles preferencias
p = [-M, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

#Cantidad de horas ofrecidas desde el nodo i como tupla (indice, horas)
for i in range(0, m):
    si.append((i + 1, round(random() * 15, 1)))

#Cantidad de horas demandadas por el nodo i como tupla (indice, horas)
for i in range(0, n):
    dj.append((i + 1, choice(dc)))

#Factibilidad, es decir que la suma de ofertas >= suma de demandas
SumaS = 0
SumaD = 0
for t in si:
    SumaS += t[1]

for t in dj:
    SumaD += t[1]

#¿crear fuente fantasma?
if(SumaS < SumaD):
    print("Problema infactible :(")

#Crear los arcos entre la oferta i y la demanda j, con su respectiva preferencia
for i in range(0, m):
    for j in range(0, n):
        cij.append((i + 1, j + 1, choice(p)))

#Genera funcion objetivo con la suma de las variables de decision Xij multiplicado por su respectiva preferencia Cij
fo = "max "
for i, j, c in cij:
    if c < 0:
        p = "(" + str(c) + ")"
    else:
        p = str(c)
    fo += p + " X" + str(i) + str(j)
    if(i != m or j != n):
        fo += " + "

const_si = ""
for i, h in si:
    suma_xij = ""
    for j in range(1, m + 1):
        suma_xij += "X" + str(i) + str(j)
        if(j != m):
            suma_xij += " + "
    const_si += suma_xij + " <= " + str(h) + "\n"


const_dj = ""
for i, h in dj:
    suma_xji = ""
    for j in range(1, n + 1):
        suma_xji += "X" + str(j) + str(i)
        if(j != n):
            suma_xji = " + "
    const_dj += suma_xij + " = " + str(h) + "\n"

