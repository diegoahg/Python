import csv
import random
from time import time


def Voto(rango1, rango2):
    probabilidad = random.randint(1, 100)
    voto = 0
    if probabilidad <= rango1:
        voto = 1
    elif probabilidad > rango1 and probabilidad <= rango2:
        voto = 2
    else:
        voto = 3
    return voto


def LeerComunas():
    reader = csv.reader(open('comunas.csv', 'rb'))
    lista = []
    for i, row in enumerate(reader):
        comuna = row[0]
        region = row[1]
        derecha = row[2]
        izquierda = row[3]
        independiente = row[4]
        dato = [comuna, region, derecha,
                izquierda, independiente]
        lista.append(dato)
    return lista


def contarVoto(comunas):
    suma = 0
    sumb = 0
    sumc = 0
    for x in xrange(1, 4):
        archivo = 'data_servel_' + str(x) + '.csv'
        reader = csv.reader(open(archivo, 'rb'))
        for i, row in enumerate(reader):
            comuna = row[1]
            for j in range(len(comunas)):
                if comuna == comunas[j][0]:
                    rango1 = int(comunas[j][2])
                    rango2 = (int(comunas[j][2]) + int(comunas[j][3]))
                    voto = Voto(rango1, rango2)
                    if voto == 1:
                        suma = suma + 1
                    elif voto == 2:
                        sumb = sumb + 1
                    else:
                        sumc = sumc + 1
    sumtotal = suma + sumb + sumc
    print " izquierda: " + str(suma)
    print " derecha: " + str(sumb)
    print " independiente: " + str(sumc)
    print " votos totales: " + str(sumtotal)

tiempo_inicial = time()
comunas = LeerComunas()
contarVoto(comunas)
tiempo_final = time() - tiempo_inicial
print "tiempo total de ejecucion: " + str(tiempo_final)
