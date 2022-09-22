from random import randint, choice


def genMZ(m: int, n: int, ffact=0):
    # Listas de ofertas (si), demandas (dj) y preferencias (cij)
    si = [0]
    dj = [0]
    cij = [0]

    # Cantidad de horas ofrecidas desde el nodo i como tupla (indice, horas)
    if ffact == 0:
        for _ in range(m):
            si.append(randint(1, 15))
    else:
        for _ in range(m):
            si.append(15)

    # Cantidad de horas demandadas por el nodo i como tupla (indice, horas)
    for _ in range(n):
        dj.append(choice([7, 8, 15]))

    # Numero M "grande" que "castiga" a la funcion objetivo denotando una no preferencia
    M = 100000

    # Crear los arcos entre la oferta i y la demanda j, con su respectiva preferencia
    for _ in range(m):
        fila = [0]
        for _ in range(n):
            fila.append(choice([-M, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
        cij.append(fila)

    # Comprobar factibilidad tanto de demandas con ofertas, y las preferencias

    fact_d = True

    if sum(si) < sum(dj):
        fact_d = False
        print("Problema infactible: demanda menor a oferta")
    else:
        print("Problema factible: demanda mayor o igual a oferta")

    fact_p = True

    for j in range(1, 1 + n):
        pref = 0
        for i in range(1, 1 + m):
            if cij[i][j] > 0:
                pref += 1
        if pref == 0:
            fact_p = False
            print("Problema infactible: nadie quiere hacer la ayudantia " + str(j))

    if fact_p:
        print("Problema factible: todas las ayudantias tienen al menos un postulante")

    # ---------------------------------------------------------------------------------------------------------------
    # Creamos el modelo en forma de string, separados adecuadamente

    t1_mn = "int: m;\nint: n;\nm = {a};\nn = {b};\n\n".format(a=m, b=n)
    t2_var_decision = "array[1..m, 1..n] of var int: x;\narray[1..m] of var 0..1: y;\n\narray[1..m, 1..n] of int: c;\n"

    t3_preferencias = "c =\n[|"
    for i in range(1, 1 + m):
        if i != 1:
            t3_preferencias += "\n |"
        for j in range(1, 1 + n):
            t3_preferencias += " " + str(cij[i][j]) + ","
    t3_preferencias += "\n|];\n\n"

    t4_ofertas = "array[1..m] of int: s;\ns = ["
    for i in range(1, 1 + m):
        if i != m:
            t4_ofertas += str(si[i]) + ", "
        else:
            t4_ofertas += str(si[i]) + "];\n\n"

    t5_demandas = "array[1..n] of int: d;\nd = ["
    for j in range(1, 1 + n):
        if j != n:
            t5_demandas += str(dj[j]) + ", "
        else:
            t5_demandas += str(dj[j]) + "];\n\n"

    t6_fo = "var int: fo;\nconstraint fo = sum(i in 1..m, j in 1..n) "
    t6_fo += "(c[i, j]*x[i, j]) - sum(i in 1..m) (y[i]);\n\n"

    t7_restriccion_oferta = "constraint forall (i in 1..m)\n    "
    t7_restriccion_oferta += "(sum(j in 1..n) (x[i, j]) <= y[i]*s[i]);\n\n"

    t8_restriccion_demanda = "constraint forall (j in 1..n)\n    "
    t8_restriccion_demanda += "(sum(i in 1..m) (x[i, j]) = d[j]);\n\n"

    t9_restriccion_nnegatividad = "constraint forall (i in 1..m, j in 1..n)"
    t9_restriccion_nnegatividad += "\n     (x[i, j] >= 0);\n\n"

    t10_solve = "solve maximize fo;"

    # Concatenamos el modelo completo
    modelo = t1_mn + t2_var_decision + t3_preferencias + t4_ofertas + \
        t5_demandas + t6_fo + t7_restriccion_oferta + \
        t8_restriccion_demanda + t9_restriccion_nnegatividad + \
        t10_solve

    return (modelo, fact_d and fact_p)


def txtMZ(filepath, text):
    with open(filepath, 'w') as f:
        f.write(text)


# Definimos nuestros limites superiores y el directorio donde se guardaran los casos
M_SUP = 10
N_SUP = 10
directorio = r'C:\Users\claud\Desktop\2022-1\INF292 (opti)\proyecto2\modelos\\'

# Iteramos por cada archivo .mzn mxn a crear
for m in range(1, M_SUP + 1):
    for n in range(1, N_SUP + 1):
        print(str(m) + "x" + str(n))
        texto, fact = genMZ(m, n)
        strfact = "infact"
        if fact:
            strfact = "fact"
        nombre_archivo = strfact + str(m) + "x" + str(n) + ".mzn"
        txtMZ(directorio + nombre_archivo, texto)
