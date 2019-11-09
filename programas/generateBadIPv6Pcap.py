#!/usr/bin/python3

##############################################################################
# Programa con funciones para generar una captura de tráfico "malo", a partir de
# una de tráfico "bueno", en base a las siguientes técnicas (por cada paquete
# y respetando sus direcciones IPv6 originales):
#	- Falsear la caché de la máquina destino con mensajes NS.
#	- Falsear la caché de la máquina destino con mensajes NA.
#	- Asignar una dirección IPv6 global errónea en la máquina destino con
#	  mensajes RA.
#
# Se utiliza para crear las partes de tráfico anómalo en los datasets de redes
# IPv6.

# ENTRADAS:
# goodPcap => captura de tráfico original (con el tráfico "bueno").
# badPcap => captura de tráfico que queremos que albergue el tráfico "malo" generado.

# SALIDAS:
# 1. La captura de tráfico con el tráfico "malo" generado (badPcap con el
# tráfico sospechoso).

# EJEMPLO DE EJECUCIÓN:
# python3 generateBadIPv6Pcap.py captura-buena.pcap captura-mala-NS.pcap
##############################################################################

from scapy.all import *

# Comprueba si se ha ejecutado bien el programa. Si está bien ejecutado, devuelve [goodPcap] y [badPcap].
def checkExecution():
	if len(sys.argv) != 3:
		print("usage: python3 generateBadIPv6Pcap.py [goodPcap] [badPcap]")
		sys.exit()
	goodPcap = sys.argv[1]
	badPcap = sys.argv[2]
	return goodPcap, badPcap

# Muestra al usuario un menú para que elija cómo quiere generar la nueva captura.
def showMenu():
	print("###########################################")
	print("Elija cómo quiere generar la nueva captura:")
	print("###########################################")
	print("1. Falseando la caché de la máquina destino con mensajes NS")
	print("2. Falseando la caché de la máquina destino con mensajes NA")
	print("3. Configurando una dirección global IPv6 errónea en la máquina destino con mensajes RA")
	print("")

# Lee la opción introducida por el usuario.
def getOption():
	# Para leer de teclado:
	# https://docs.python.org/3/library/functions.html#input
	num = input("Su opción es: ")
	return num

# Genera direcciones Ethernet aleatorias:
# https://stackoverflow.com/questions/50187634/random-mac-address-generator-in-python
def generateEthernetAddress():
	hexBytesList = []
	for i in range(6):
		decimalByte = random.randint(0, 255)	# De 0 a (2^8bits - 1)
		hexByte = '%02x' % decimalByte
		hexBytesList.append(hexByte)
	EthAddress = ":".join(hexBytesList)
	return EthAddress

# Para cada paquete de una captura (buena), crea uno nuevo en otra captura
# (mala) falseando la caché de la máquina destino, asociando la máquina origen
# a una dirección MAC inválida (ataque DoS).
# -- Con mensajes NS --
def neighbourCacheAttackWithNS(goodPcap, badPcap):
	packets = rdpcap(goodPcap)
	packetsList = []
	for packet in packets:
		if IPv6 in packet:
			IPv6Src = packet[IPv6].src
			IPv6Dst = packet[IPv6].dst
			newPacket1 = IPv6(src=IPv6Src, dst=IPv6Dst)
			newPacket2 = ICMPv6ND_NS(tgt=IPv6Dst)
			randomEthAddress = generateEthernetAddress()
			newPacket3 = ICMPv6NDOptSrcLLAddr(lladdr=randomEthAddress)
			newPacket = newPacket1 / newPacket2 / newPacket3
			packetsList.append(newPacket)
	wrpcap(badPcap, packetsList)

# Para cada paquete de una captura (buena), crea uno nuevo en otra captura
# (mala) falseando la caché de la máquina destino, asociando la máquina origen
# a una dirección MAC inválida (ataque DoS).
# -- Con mensajes NA --
def neighbourCacheAttackWithNA(goodPcap, badPcap):
	packets = rdpcap(goodPcap)
	packetsList = []
	for packet in packets:
		if IPv6 in packet:
			IPv6Src = packet[IPv6].src
			IPv6Dst = packet[IPv6].dst
			newPacket1 = IPv6(src=IPv6Src, dst=IPv6Dst)
			newPacket2 = ICMPv6ND_NA(R=0, tgt=IPv6Src)
			randomEthAddress = generateEthernetAddress()
			newPacket3 = ICMPv6NDOptDstLLAddr(lladdr=randomEthAddress)
			newPacket = newPacket1 / newPacket2 / newPacket3
			packetsList.append(newPacket)
	wrpcap(badPcap, packetsList)

# Genera prefijos de red IPv6 aleatorios:
# https://stackoverflow.com/questions/7660485/how-to-generate-random-ipv6-address-using-pythonor-in-scapy
def generateIPv6Prefix():
	hexBytesList = []
	for i in range(2):
		decimalTwoBytes = random.randint(0, 65535)	# De 0 a (2^16bits - 1)
		hexTwoBytes = '%02x' % decimalTwoBytes
		hexBytesList.append(hexTwoBytes)
	IPv6Prefix = "2001:db8:" + ":" .join(hexBytesList) + "::"
	return IPv6Prefix

# Para cada paquete de una captura (buena), crea uno nuevo en otra captura
# (mala) configurando erróneamente la dirección global IPv6 de la máquina
# destino (con una dirección aleatoria, ataque DoS).
# -- Con mensajes RA --
def wrongGlobalIPv6AddressWithRA(goodPcap, badPcap):
	packets = rdpcap(goodPcap)
	packetsList = []
	for packet in packets:
		if IPv6 in packet:
			IPv6Src = packet[IPv6].src
			newPacket1 = IPv6(src=IPv6Src, dst="ff02::1")
			newPacket2 = ICMPv6ND_RA(M=0, O=0)
			ramdomIPv6Prefix = generateIPv6Prefix()
			newPacket3 = ICMPv6NDOptPrefixInfo(prefixlen=64, prefix=ramdomIPv6Prefix, L=1, A=1)
			newPacket = newPacket1 / newPacket2 / newPacket3
			packetsList.append(newPacket)
	wrpcap(badPcap, packetsList)

# Procesa la opción elegida por el usuario.
def processOption(num, goodPcap, badPcap):
	if num == "1":
		neighbourCacheAttackWithNS(goodPcap, badPcap)
	elif num == "2":
		neighbourCacheAttackWithNA(goodPcap, badPcap)
	elif num == "3":
		wrongGlobalIPv6AddressWithRA(goodPcap, badPcap)
	else:
		print("Esa opción no existe")
		sys.exit()

goodPcap, badPcap = checkExecution()
showMenu()
num = getOption()
processOption(num, goodPcap, badPcap)
