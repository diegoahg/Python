import random

#################################
#Funcione de Simulacion del Voto#
#Retorna 1 si es IZQUERDA       #
#Retorna 2 si es DERECHA        #
#Retorna 3 si es INDEPENDIENTE  #
#################################
def Voto(izquierda , derecha , independiente):
	rango1 = izquierda
	rango2 = izquierda + derecha
	probabilidad = random.randint(0, 100)
	voto = 0
	if probabilidad <= rango1:
		voto = 1
	elif probabilidad > rango1 and probabilidad <= rango2:
		voto = 2
	elif probabilidad > rango2 and probabilidad <= 100:
		voto = 3
	return voto

voto = Voto(20,30,50)
#print "El voto fue :" + str(voto)

comunas = [ ["Santiago", 20, 30, 40], ["Macul", 25,40,35]]

#for i in range(len(comunas)):
#    print comunas[i][0]

f = open("datos.csv")
dato = f.readline()
while dato != "":
	datos = dato.split(';')
	#print datos[1]
	for i in range(len(comunas)):
    		if datos[1] == comunas[i][0]:
			 voto = Voto(comunas[i][1],comunas[i][2],comunas[i][3])
			 print (datos[0] + ";" + datos[1] + ";" + datos[2] + ";" + str(voto) + ";")
	dato = f.readline()
f.close()
