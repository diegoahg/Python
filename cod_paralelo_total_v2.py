from mpi4py import MPI
import csv
import random
import sys
import os
from time import time

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()


# Funcion que genera un voto en base a la probabilidad que tiene la comuna
# es por esto que se entregan como rango1 el porcentaje que tiene el
# partido de izquierda y rango2 como las suma de la probabilidad de
# partido de izquierda junto con la probabilidad del partido de derecha.

def Voto(rango1, rango2):
    probabilidad = random.randint(1, 100)
    voto = 0
    # rango perteneciente a partido de izquierda.
    if probabilidad <= rango1:
        voto = 1
    # rango perteneciente a partido de derecha.
    elif probabilidad > rango1 and probabilidad <= rango2:
        voto = 2
    # rango perteneciente a partido independiente.
    else:
        voto = 3
    return voto

# Funcion que lee el archivo csv que contiene las comunas y
# sus probabilidades de cada partido politico. Estos datos se
# trasladan a una lista para reducir el tiempo de lectura de
# los datos al generar los datos con la funcion Voto


def LeerComunas():
    # Apertura de archivo.
    reader = csv.reader(open('Data/comunas.csv', 'rb'))
    lista = []
    for i, row in enumerate(reader):
        # Particionar la informacion con el delimitador ";"
        particion = str(row[0]).split(";")
        comuna = particion[0]
        region = particion[1]
        derecha = particion[2]
        izquierda = particion[3]
        independiente = particion[4]
        dato = [comuna, region, derecha,
                izquierda, independiente]
        lista.append(dato)
    return lista

# Funcion que lee la informacion entregada por SERVEL
# comparando una comuna con sus probabilidades y utilizando
# la funcion Voto. Teniendo el voto generado, se asigna al
# partido politico.


def contarVoto(comunas, archivo, rank, name):
    wt = MPI.Wtime()
    suma = 0
    sumb = 0
    sumc = 0
    reader = csv.reader(open('TMP/' + str(archivo) + '.csv', 'rb'))
    # sw = 0
    for i, row in enumerate(reader):
        particion = str(row[0]).split(";")
        comuna = particion[1].rstrip()
        for j in range(len(comunas)):
            # Se busca que la comuna leida en el archivo "data_server_'xx'"
            # coincida con la lista de comunas, para asi, obtener sus
            # probabilidades.
            if comuna == comunas[j][0]:
                # Generar rango partido Izquierda
                rango1 = int(comunas[j][2])
                # Generar rango partido Derecha
                rango2 = (int(comunas[j][2]) + int(comunas[j][3]))
                # Guardar el voto generado con la funcion Voto
                voto = Voto(rango1, rango2)
                # Acumular los votos de cada partido politico donde:
                # suma guarda los votos de izquierda
                # sumb guarda los votos de derecha
                # sumc guarda los votos independiente.
                if voto == 1:
                    suma = suma + 1
                elif voto == 2:
                    sumb = sumb + 1
                else:
                    sumc = sumc + 1
                # sw = 1
            # if sw == 0:
            #    print comuna + "hola"
    sumtotal = suma + sumb + sumc
    # print "Suma total: " + str(sumtotal)
    wt = MPI.Wtime() - wt
    lista = dict(
        izquerda=suma, derecha=sumb, independiente=sumc, total=sumtotal)
    comm.send(lista, dest=0)


def HacerCsv(nombre, data):
    writer = csv.writer(open("TMP/" + str(nombre) + ".csv", "wb"))
    for l in data:
        particion = str(l).split(";")
        particion[1] = particion[1].rstrip()
        particion[0] = particion[0].rstrip()
        writer.writerow([particion[0] + ";" + particion[1]])


def main():
    if rank == 0:
        print "*****Paralelo Granularidad Fina de Codigo Version 2*****"
        tiempo_inicial = time()
        total = 12905887
        rango = int(total / (size - 1))
        resto = total - (rango * (size - 1))
        process = 0
        f = open('Data/data_total.csv', 'r')
        p = f.readlines()
        for i in range(size - 2):
            inicio = rango * i
            fin = rango * (i + 1)
            process = process + 1
            primera = p[inicio:fin]
            HacerCsv(process, primera)
            print "hice algo " + str(i)
        inicio = fin
        fin = inicio + rango + resto
        process = process + 1
        primera = p[inicio:fin]
        HacerCsv(process, primera)
        print "hice algo " + str(i+1)
        for i in range(1, size):
            comm.send(i, dest=i)
    if rank != 0:
        archivo = comm.recv(source=0)
        comunas = LeerComunas()
        contarVoto(comunas, archivo, rank, name)
    if rank == 0:
        izquerda = 0
        derecha = 0
        independiente = 0
        totales = 0
        for i in range(1, size):
            voto = comm.recv(source=i)
            # print voto
            izquerda = izquerda + voto["izquerda"]
            derecha = derecha + voto["derecha"]
            independiente = independiente + voto["independiente"]
            totales = totales + voto["total"]
        tiempo_final = time() - tiempo_inicial
        print " Izquierda: " + str(izquerda)
        print " Derecha: " + str(derecha)
        print " Independiente: " + str(independiente)
        print " Votos totales: " + str(totales)
        print "Tiempo total de ejecucion: " + str(tiempo_final)
        for i in range(1, size):
            archivo = 'TMP/' + str(i) + '.csv'
            os.remove(archivo)
        return 0
main()
