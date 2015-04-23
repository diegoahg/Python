import csv
rango = 50
fin = 345
inicio = fin - rango
contador = fin
comunas = 0
reader = csv.reader(open('Data/comunas.csv', 'rb'))
for i, row in enumerate(reader):
    particion = str(row[0]).split(";")
    if contador > inicio:
        comunas = comunas + 1
        contador = contador - 1
    else:
        print comunas
        comunas = 0
        fin = inicio
        inicio = fin - rango
    ultimo = i
print comunas
print ultimo
