#!/usr/bin/python3

##############################################################################
# Programa que crea la red neuronal y, posteriormente, la entrena y prueba en
# base a los datasets que se indican por la línea de comandos (como ficheros de
# texto - formato .txt).

# ENTRADAS:
# [numFeatures] => número de bytes que caracterizan a cada uno de los paquetes.
# [goodXTrainTxt] => fichero .txt con el tráfico "bueno" del futuro training set.
# [badXTrainTxt] => fichero .txt con el tráfico anormal del futuro training set.
# [goodXValTxt] => fichero .txt con el tráfico "bueno" del futuro validation set.
# [badXValTxt] => fichero .txt con el tráfico anormal del futuro validation set.
# [goodXTestTxt] => fichero .txt con el tráfico "bueno" del futuro test set.
# [badXTestTxt] => fichero .txt con el tráfico anormal del futuro test set.

# SALIDAS:
# 1. Porcentaje de paquetes del test set clasificados correctamente por la red neuronal
# tras haber sido testada => número de paquetes correctamente etiquetados /
# número de paquetes totales.
#
# 2. Porcentaje de paquetes del test set clasificados incorrectamente por la red neuronal
# tras haber sido testada => número de paquetes incorrectamente etiquetados /
# número de paquetes totales.
#
# 3. Suma de porcentaje correcto + incorrecto => siempre debe ser 1.0.

# EJEMPLO DE EJECUCIÓN:
# python3 NNForNetworkTraffic.py features=88
#	goodXTrain=cap-ipv6-train.txt	badXTrain=cap-ipv6-train-NS.txt
#	goodXVal=cap-ipv6-val.txt		badXVal=cap-ipv6-val-NS.txt
#	goodXTest=cap-ipv6-test.txt		badXTest=cap-ipv6-test-NS.txt
##############################################################################

import readTxtFile as rtxt
import numpy as np
from keras import models, layers
import matplotlib.pyplot as plt
import sys

# Comprueba si se ha ejecutado el programa con el número de argumentos correctos.
# Si el número es correcto, guarda [numFeatures], [goodXTrainTxt], [badXTrainTxt],
# [goodXValTxt], [badXValTxt], [goodXTestTxt] y [badXTestTxt].
def checkExecution():
	datasetTxt = {}
	if len(sys.argv) != 8:
		print("")
		print("usage: python3 NNForNetworkTraffic.py features=[numFeatures] " +
			"goodXTrain=[goodXTrainTxt] badXTrain=[badXTrainTxt] " +
			"goodXVal=[goodXValTxt] badXVal=[badXValTxt] " +
			"goodXTest=[goodXTestTxt] badXTest=[badXTestTxt]")
		sys.exit()
	numFeatures = int(sys.argv[1].split("=")[-1])				# 50 para IPv4, 88 para IPv6.
	datasetTxt["goodXTrainTxt"] = sys.argv[2].split("=")[-1]	# Separo por "=" y me quedo con el último elemento de la lista.
	datasetTxt["badXTrainTxt"] = sys.argv[3].split("=")[-1]
	datasetTxt["goodXValTxt"] = sys.argv[4].split("=")[-1]
	datasetTxt["badXValTxt"] = sys.argv[5].split("=")[-1]
	datasetTxt["goodXTestTxt"] = sys.argv[6].split("=")[-1]
	datasetTxt["badXTestTxt"] = sys.argv[7].split("=")[-1]
	return numFeatures, datasetTxt

# Genera el dataset final que se va a inyectar en la red neuronal (en base a la
# a las capturas almacenadas en formato .txt con la información del tráfico
# "bueno" y "malo" por separado).
def generateDataset(datasetTxt, numFeatures):
	dataset = {}
	goodXTrainTxt = datasetTxt.get("goodXTrainTxt")
	badXTrainTxt = datasetTxt.get("badXTrainTxt")
	dataset["xTrain"], dataset["yTrain"] = rtxt.createDataset(goodXTrainTxt, badXTrainTxt, numFeatures)

	goodXValTxt = datasetTxt.get("goodXValTxt")
	badXValTxt = datasetTxt.get("badXValTxt")
	dataset["xVal"], dataset["yVal"] = rtxt.createDataset(goodXValTxt, badXValTxt, numFeatures)

	goodXTestTxt = datasetTxt.get("goodXTestTxt")
	badXTestTxt = datasetTxt.get("badXTestTxt")
	dataset["xTest"], dataset["yTest"] = rtxt.createDataset(goodXTestTxt, badXTestTxt, numFeatures)
	return dataset

# Construye la red neuronal.
def buildNN(numFeatures):
	model = models.Sequential()
	model.add(layers.Dense(32, activation='relu', input_shape=(numFeatures,)))
	model.add(layers.Dense(32, activation='relu'))
	model.add(layers.Dense(1, activation='sigmoid'))

	model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
	return model

# Entrena la red neuronal (con el training set)
def trainNN(model, dataset):
	xTrain = dataset.get("xTrain")
	yTrain = dataset.get("yTrain")
	xVal = dataset.get("xVal")
	yVal = dataset.get("yVal")
	history = model.fit(xTrain, yTrain, epochs=20, batch_size=512, validation_data=(xVal, yVal))

# Prueba la red neuronal clasificando tráfico nuevo (el del test set)
def testNN(model, dataset):
	xTest = dataset.get("xTest")
	yTest = dataset.get("yTest")
	yPredictionsMatrix = model.predict(xTest)											# Matriz (X, 1)
	yPredictionsVector = np.reshape(yPredictionsMatrix, np.size(yPredictionsMatrix))	# Vector (X,)

	accPredictions = np.sum(yTest == np.around(yPredictionsVector)) / np.size(yTest)
	inaccPredictions = np.sum(yTest != np.around(yPredictionsVector)) / np.size(yTest)

	print("")
	print("####################################################")
	print("Probando la red neuronal sobre tráfico nuevo (xTest)")
	print("####################################################")
	print("· Precisión (0-1)      =  " + str(accPredictions))
	print("· Imprecisión (0-1)    =  " + str(inaccPredictions))
	print("· Total (debe ser 1.0) =  " + str(accPredictions + inaccPredictions))


numFeatures, datasetTxt = checkExecution()
dataset = generateDataset(datasetTxt, numFeatures)
model = buildNN(numFeatures)
trainNN(model, dataset)
testNN(model, dataset)
