from copy import deepcopy
import csv
from math import floor
from random import randint
from time import time

# Entrega el valor de la funcion objetivo y matriz resultante con el metodo MCM


def minimo_costo(matrix_c: list[list], s_i: list, d_j: list):
    matrix_res = [[0 for i in range(len(matrix_c[0]))]
                  for j in range(len(matrix_c))]
    temp_s = deepcopy(s_i)
    temp_d = deepcopy(d_j)

    # Algoritmo de seleccion de minimo costo
    while sum(temp_s) != 0 or sum(temp_d) != 0:
        min_c = 10000000
        pos_i = 0
        pos_j = 0

        # Extraemos la posicion del minimo costo
        for i in range(len(matrix_c)):
            for j in range(len(matrix_c[0])):
                if temp_s[i] != 0 and temp_d[j] != 0:
                    if matrix_c[i][j] < min_c:
                        min_c = matrix_c[i][j]
                        pos_i = i
                        pos_j = j

        # Suplimos todo lo posible a la posicion encontrada
        if temp_s[pos_i] < temp_d[pos_j]:
            matrix_res[pos_i][pos_j] += temp_s[pos_i]
            temp_d[pos_j] -= temp_s[pos_i]
            temp_s[pos_i] = 0
        else:
            matrix_res[pos_i][pos_j] += temp_d[pos_j]
            temp_s[pos_i] -= temp_d[pos_j]
            temp_d[pos_j] = 0

    # Calculamos el valor de la funcion
    fo = 0
    for i in range(len(matrix_c)):
        for j in range(len(matrix_c[0])):
            fo += matrix_c[i][j] * matrix_res[i][j]

    # Retornamos el valor de la funcion junto a la matriz resultante
    return (fo, matrix_res)

# Entrega el valor de la funcion objetivo y matriz resultante con el metodo MAR


def russell(matrix_c: list[list], s_i: list, d_j: list):
    matrix_res = [[0 for i in range(len(matrix_c[0]))]
                  for j in range(len(matrix_c))]
    matrix_IC = [[0 for i in range(len(matrix_c[0]))]
                 for j in range(len(matrix_c))]

    temp_s = deepcopy(s_i)
    temp_d = deepcopy(d_j)

    # Calculamos la matriz de indice de costos
    for i in range(len(matrix_c)):
        for j in range(len(matrix_c[0])):
            max_row = max(matrix_c[i])
            max_col = -1000000

            for row in matrix_c:
                if row[j] > max_col:
                    max_col = row[j]

            matrix_IC[i][j] = max_row + max_col - matrix_c[i][j]

    # Algoritmo de seleccion de maximo IC o menor costo
    while sum(temp_s) != 0 or sum(temp_d) != 0:
        min_c = 10000000
        max_IC = -10000000
        pos_i = 0
        pos_j = 0

        # Extraemos la posicion del maximo IC o menor costo
        for i in range(len(matrix_IC)):
            for j in range(len(matrix_IC[0])):
                if temp_s[i] != 0 and temp_d[j] != 0:
                    if matrix_IC[i][j] == max_IC:
                        if matrix_c[i][j] < min_c:
                            min_c = matrix_c[i][j]
                            pos_i = i
                            pos_j = j
                    elif matrix_IC[i][j] > max_IC:
                        min_c = matrix_c[i][j]
                        max_IC = matrix_IC[i][j]
                        pos_i = i
                        pos_j = j

        # Suplimos todo lo posible a la posicion encontrada
        if temp_s[pos_i] < temp_d[pos_j]:
            matrix_res[pos_i][pos_j] += temp_s[pos_i]
            temp_d[pos_j] -= temp_s[pos_i]
            temp_s[pos_i] = 0
        else:
            matrix_res[pos_i][pos_j] += temp_d[pos_j]
            temp_s[pos_i] -= temp_d[pos_j]
            temp_d[pos_j] = 0

    # Calculamos el valor de la funcion
    fo = 0
    for i in range(len(matrix_c)):
        for j in range(len(matrix_c[0])):
            fo += matrix_c[i][j] * matrix_res[i][j]

    # Retornamos el valor de la funcion junto a la matriz resultante
    return (fo, matrix_res)

# Genera un modelo con matriz de costos, ofertas y demandas de forma aleatoria


def model_generator(m: int, n: int):
    # Generacion aleatoria de matriz de costos
    matrix = [[randint(1, 30) for _ in range(n)] for _ in range(m)]

    # Generacion aleatoria de lista de ofertas
    supply = [50 * randint(10, 100) for _ in range(m)]
    pool = sum(supply)

    # Generacion aleatoria de lista de demandas
    demand = []
    for _ in range(n - 1):
        d_j = randint(1, floor(float(pool) / 10))
        demand.append(d_j)
        pool -= d_j
    demand.append(pool)

    # Retornamos la matriz de costos y la lista de ofertas y demandas
    return (matrix, supply, demand)


M_MAX = 15
N_MAX = 15
hechos = []

dir = r"C:\Users\claud\Desktop\2022-1\INF292 (opti)\proyecto3\tiempos.csv"
file = open(dir, 'w', encoding='UTF8', newline='')
writer = csv.writer(file)
writer.writerow(["N", "TMCM(N)", "TMAR(N)", "MCMvsMAR"])

for i in range(5, M_MAX):
    for j in range(5, N_MAX):
        if 100 * i * j not in hechos:
            print(100 * i * j)
            matriz, ofertas, demandas = model_generator(10 * i, 10 * j)

            start1 = time()
            fo1, _ = minimo_costo(matriz, ofertas, demandas)
            end1 = time()

            start2 = time()
            fo2, _ = russell(matriz, ofertas, demandas)
            end2 = time()

            data = [str(100 * i * j), str(end1 - start1), str(end2 - start2)]

            if fo1 > fo2:
                data.append("MCM")
            elif fo1 < fo2:
                data.append("MAR")
            else:
                data.append("EMP")

            writer.writerow(data)

            hechos.append(100 * i * j)

file.close()
