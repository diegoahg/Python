import os

for i in range(46):
    archivo = 'data_' + str(i) + '.csv'
    print archivo
    os.remove(archivo)
