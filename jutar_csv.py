import csv

# Con este codigo junte toda la data del Servel en un solo csv


def juntardata():
    writer = csv.writer(open("Data/data_total.csv", "wb"))
    for x in xrange(1, 14):
        archivo = 'Data/data_servel_' + str(x) + '.csv'
        print str(x)
        reader = csv.reader(open(archivo, 'rb'))
        for i, row in enumerate(reader):
            particion = str(row[0]).split(";")
            writer.writerow([particion[0] + ";" + particion[1]])

# Con este codigo cuento cuantos datos hay en el csv


def contardata():
    archivo = 'Data/data_total.csv'
    contador = 0
    reader = csv.reader(open(archivo, 'rb'))
    for i, row in enumerate(reader):
        contador = contador + 1
    print str(contador)

# Funcion lee por rangos de datos


def leerdata(inicio, fin):
    f = open('Data/data_total.csv', 'r')
    p = f.readlines()
    contador = 0
    primera = p[inicio:fin]
    for l in primera:
        particion = str(l).split(";")
        print particion[1]
        contador = contador + 1
    print contador

# Funcion te entrega rangos por el size que le pongas


def rangos(size):
    total = 12905887
    rango = int(total / size)
    resto = total - (rango * size)
    for i in range(size-1):
        inicio = rango * i
        fin = rango * (i + 1)
        print "incio = " + str(inicio)
        print "fin = " + str(fin)
    inicio = fin
    fin = inicio + rango + resto
    print "incio = " + str(inicio)
    print "fin = " + str(fin)

rangos(3)
