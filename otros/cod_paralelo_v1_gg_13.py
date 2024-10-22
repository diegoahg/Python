from mpi4py import MPI
import csv
import random
from time import time

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size


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


def contarVoto(comunas, inicio, fin):
    suma = 0
    sumb = 0
    sumc = 0
    for x in xrange(inicio, fin):
        archivo = 'Data/data_servel_' + str(x) + '.csv'
        print (str(x))
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
                print (comuna + "hola")
    sumtotal = suma + sumb + sumc
    print (" izquierda: " + str(suma))
    print (" derecha: " + str(sumb))
    print (" independiente: " + str(sumc))
    print (" votos totales: " + str(sumtotal))


def main():
    if rank == 0:
        # comm.send(arrImg, dest=i)
        print ("*****Paralelo*****")
        tiempo_inicial = time()
        comunas = LeerComunas()
        for x in xrange(1, 14):
            comm.send(x, dest=x)
    if rank != 0:
        # cada procesador recibe un arreglo RGB que contiene un trozo
        # horizontal de la imagen
        comunas = LeerComunas()
        archivo = comm.recv(source=0)
        # imagen
        contarVoto(comunas, archivo, archivo + 1)
        comm.send("OK" + str(archivo), dest=0)
        # recibe los arreglos y los junta uno abajo del otro
    if rank == 0:
        ok1 = comm.recv(source=1)
        ok2 = comm.recv(source=2)
        ok3 = comm.recv(source=3)
        ok4 = comm.recv(source=4)
        ok5 = comm.recv(source=5)
        ok6 = comm.recv(source=6)
        ok7 = comm.recv(source=7)
        ok8 = comm.recv(source=8)
        ok9 = comm.recv(source=9)
        ok10 = comm.recv(source=10)
        ok11 = comm.recv(source=11)
        ok12 = comm.recv(source=12)
        ok13 = comm.recv(source=13)
        tiempo_final = time() - tiempo_inicial
        print ("tiempo total de ejecucion: " + str(tiempo_final))
        print (ok1 + "-" + ok2 + "-" + ok3 + "-" + ok4 + "-" + ok5 + "-" + ok6 + "-" +
               ok7 + "-" + ok8 + "-" + ok9 + "-" + ok10 + "-" + ok11 + "-" + ok12 + "-" + ok13)
        return 0
        # for i in range(1, size):
        #    if i > 1:
        #        construcImg = np.concatenate(
        #            (construcImg, comm.recv(source=i)))
        #    if i == 1:
        #        construcImg = comm.recv(source=i)


main()
print ("Listo")
