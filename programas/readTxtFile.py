#!/usr/bin/python3

###############################################################################
# Programa auxiliar con la función createDataset() que realmente se encarga de
# juntar el tráfico de las capturas guardadas como ficheros .txt. para
# generar el training, validation y test set del dataset final que se va a
# inyectar en la red neuronal.
#
# Por tanto, se importa desde el fichero NNForNetworkTraffic.py para utilizar
# la función createDataset().

# ENTRADAS:
# origTxt => fichero .txt con la parte de tráfico "bueno".
# modTxt => fichero .txt con la parte de tráfico modificado (tráfico "malo").
# numFeatures => número de bytes que caracterizan a cada uno de los paquetes.

# SALIDAS:
# Devuelve el training/validation/test set resultante en 2 variables:
# 1. Matriz de muestras de tráfico del subconjunto en cuestión.
# 2. Vector con las etiquetas correspondientes a cada paquete.

# EJEMPLO DE EJECUCIÓN:
# import readTxtFile as rtxt
# rtxt.createDataset("cap-ipv6-train.txt", "cap-ipv6-train-NS.txt", 88)
###############################################################################

import numpy as np

# Devuelve el número de líneas de un fichero.
def countLines(filepath):
	f = open(filepath, "r")
	counter = 0
	for line in f:
		counter += 1
	f.close()
	return counter

# Devuelve la matriz de ceros rellenada con los bytes en decimal.
def fillData(filepath, numFeatures, data):
	f = open(filepath, "r")
	i, j = 0, 0
	for line in f:
		hexData = line.split(" ")[:numFeatures]		# ['ff', 'b7', 'aa', '00', 'a2', ...] (hasta 50).
		for pairHex in hexData:						# len(hexData) = nº de bytes en el paquete.
			try:
				decData = int(pairHex, 16)			# hexData => decData.
			except ValueError as e:
				# j += 1							# Seguimos con el mismo indice de j (omitimos que nos hemos encontrado caracteres especiales).
				continue							# Si Wireshark ha introducido caracteres no hexadecimales, nos los saltamos.
			decDataNorm = decData / 255				# decData normalizado.
			data[i, j] = decDataNorm
			j += 1
		j = 0
		i += 1
	f.close()
	return data

# Crea un dataset de muestras (bytes de paquetes) y sus correspondientes salidas (0 o 1).
def createDataset(origTxt, modTxt, numFeatures):
	# Calculamos el número de paquetes que hay en la captura (una línea con los bytes por paquete).
	numPackets = countLines(origTxt)

	# Cargamos las muestras de tráfico normal (el de la captura original, y = 0).
	goodData = np.zeros((numPackets, numFeatures))						# (10 x 50) 			{por ejemplo}.
	goodDataFilled = fillData(origTxt, numFeatures, goodData)			# (10 x 50 rellenado) 	{por ejemplo}.

	# Cargamos las muestras de tráfico anormal (el de la captura modificada, y = 1).
	badData = np.zeros((numPackets, numFeatures))						# (10 x 50)				{por ejemplo}.
	badDataFilled = fillData(modTxt, numFeatures, badData)				# (10 x 50 rellenado)	{por ejemplo}.

	# Juntamos las muestras de tráfico normal y anormal (tanto y = 0 como y = 1).
	xAll = np.concatenate((goodDataFilled, badDataFilled), axis=0)		# (20 x 50)				{por ejemplo}.

	# Creamos las etiquetas para el tráfico normal (y = 0) y anormal (y = 1).
	# https://stackoverflow.com/questions/22053050/difference-between-numpy-array-shape-r-1-and-r
	yZero = np.zeros((numPackets))				# Vector (1 x 10) == (10,)						{por ejemplo}.
	yOne = np.ones((numPackets))				# Vector (1 x 10) == (10,)						{por ejemplo}.

	# Juntamos las etiquetas para el tráfico normal y anormal (tanto y = 0 como y = 1).
	yAll = np.concatenate((yZero, yOne), axis=0)		# Vector (1 x 20) == (20,)				{por ejemplo}.

	# Alteramos el orden de las muestras y sus salidas para que estén mezcladas.
	# https://stackoverflow.com/questions/43229034/randomly-shuffle-data-and-labels-from-different-files-in-the-same-order
	idxShuffled = np.random.permutation(len(xAll))
	xAllShuffled = xAll[idxShuffled]
	yAllShuffled = yAll[idxShuffled]

	# https://stackoverflow.com/questions/39345995/how-does-python-return-multiple-values-from-a-function
	return xAllShuffled, yAllShuffled
