from mpi4py import MPI
import csv
import random
import sys
from time import time

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()


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
    reader = csv.reader(open('Data/comunas.csv', 'rb'))
    lista = []
    for i, row in enumerate(reader):
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


def contarVoto(comunas, inicio, fin, rank, name):
    suma = 0
    sumb = 0
    sumc = 0
    for x in xrange(inicio, fin):
        archivo = 'Data/data_servel_' + str(x) + '.csv'
        print "Archivo: " + str(x)
        reader = csv.reader(open(archivo, 'rb'))
        for i, row in enumerate(reader):
            particion = str(row[0]).split(";")
            comuna = particion[1]
            sw = 0
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
                    sw = 1
            if sw == 0:
                print comuna + "hola"
    sumtotal = suma + sumb + sumc
    lista = dict(
        izquerda=suma, derecha=sumb, independiente=sumc, total=sumtotal)
    comm.send(lista, dest=0)
    sys.stdout.write("Termino Proceso %d en %s.\n" % (rank, name))


def main():
    if rank == 0:
        print "*****Paralelo*****"
        tiempo_inicial = time()
        for i in range(1, 14):
            comm.send(i, dest=i)
    if rank != 0:
        archivo = comm.recv(source=0)
        comunas = LeerComunas()
        contarVoto(comunas, archivo, archivo + 1, rank, name)
        comm.send("OK" + str(archivo), dest=0) if rank == 0:
        izquerda = 0
        derecha = 0
        independiente = 0
        totales = 0
        for i in range(1, 14):
            voto = comm.recv(source=i)
            izquerda = izquerda + voto["izquerda"]
            derecha = derecha + voto["derecha"]
            independiente = independiente + voto["independiente"]
            totales = totales + voto["total"]
        print " izquierda: " + str(izquerda)
        print " derecha: " + str(derecha)
        print " independiente: " + str(independiente)
        print " votos totales: " + str(totales)
        tiempo_final = time() - tiempo_inicial
        print "tiempo total de ejecucion: " + str(tiempo_final)
        print "Listo"
        return 0
main()
