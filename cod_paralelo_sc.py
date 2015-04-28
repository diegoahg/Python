from mpi4py import MPI
from time import time
import csv
import random


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


def contarVoto(comunas, inicio, fin, rank, name, t_com, t_i):
    suma = 0
    sumb = 0
    sumc = 0
    for x in xrange(inicio, fin + 1):
        archivo = 'Data_40/data_servel_' + str(x) + '.csv'
        print "Archivo: " + str(x) + "  Procesador: " + str(rank)
        reader = csv.reader(open(archivo, 'rb'))
        for i, row in enumerate(reader):
            particion = str(row[0]).split(";")
            comuna = particion[1]
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
    t_final = (time() - t_i)
    lista = dict(izquerda=suma, derecha=sumb, independiente=sumc,
                 total=sumtotal, t_com_nodo=t_com, tiempo=t_final)
    print " izquierda: " + str(suma)
    print " derecha: " + str(sumb)
    print " independiente: " + str(sumc)
    print " Total " + str(sumtotal)
    comm.send(lista, dest=0)
    print ("Termine ctm")


def main():
    if rank == 0:
        print "*****Paralelo*****"
        tiempo_inicial = time()
        comunas = LeerComunas()
        z = 0
        x = 0
        r_2 = 0
        print str(size) + "  soy size"
        while z < size:
            r_1 = 1 + x
            x = (40 / size)
            z = z + 1
            r_2 = x * z
            x = r_2
            print str(r_1) + "  soy r1"
            print str(r_2) + "  soy r2"
            t_com_ini = time()
            listb = dict(
                numero=z, t_com_inicial=t_com_ini, comunas=comunas, rango_1=r_1, rango_2=r_2)
            comm.send(listb, dest=z)
    if rank != 0:
        t_recibido = time()
        lista = comm.recv(source=0)
        t_comunicacion = lista["t_com_inicial"] - t_recibido
        contarVoto(lista["comunas"], lista["rango_1"], lista[
                   "rango_2"], rank, name, t_comunicacion, t_recibido)
    if rank == 0:
        izquerda = 0
        derecha = 0
        independiente = 0
        totales = 0
        t_mayor = -1
        t_com_total = 0
        for i in range(1, size - 1):
            voto = comm.recv(source=i)
            izquerda = izquerda + voto["izquerda"]
            derecha = derecha + voto["derecha"]
            independiente = independiente + voto["independiente"]
            totales = totales + voto["total"]
            t_com_total = t_com_total + voto["t_com_nodo"]
            if voto["tiempo"] > t_mayor:
                t_mayor = voto["tiempo"]
        print " izquierda: " + str(izquerda)
        print " derecha: " + str(derecha)
        print " independiente: " + str(independiente)
        print " votos totales: " + str(totales)
        print " Timpo comunicacion: " + str(t_com_total)
        print " Tiempo Mayor de proceso: " + str(t_mayor)
        tiempo_final = time() - tiempo_inicial
        print "tiempo total de ejecucion: " + str(tiempo_final)
        print "Listo"
        return 0

# Inicio del programa
main()
