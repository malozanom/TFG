#!/usr/bin/python3

##############################################################################
# Programa con funciones para generar una captura de tráfico "malo", a partir de
# una de tráfico "bueno", intercambiando algunos campos por cada paquete:
# direcciones Ethernet, IP, puertos TCP/UDP o combinaciones de ellos.
#
# Se utiliza para crear las partes de tráfico anómalo en los datasets de redes
# IPv4.

# ENTRADAS:
# goodPcap => captura de tráfico original (con el tráfico "bueno").
# badPcap => captura de tráfico que queremos que albergue el tráfico modificado
#			 (el tráfico "malo").

# SALIDAS:
# 1. La captura de tráfico con las modificaciones hechas en base a la original
# (badPcap con el tráfico sospechoso).

# EJEMPLO DE EJECUCIÓN:
# python3 generateBadIPv4Pcap.py captura-buena.pcap captura-mala-IP.pcap
##############################################################################

from scapy.all import *

# Comprueba si se ha ejecutado bien el programa. Si está bien ejecutado, devuelve [goodPcap] y [badPcap].
def checkExecution():
	if len(sys.argv) != 3:
		print("usage: python3 generateBadIPv4Pcap.py [goodPcap] [badPcap]")
		sys.exit()
	goodPcap = sys.argv[1]
	badPcap = sys.argv[2]
	return goodPcap, badPcap

# Muestra al usuario un menú para que elija cómo quiere generar la nueva captura.
def showMenu():
	print("###########################################")
	print("Elija cómo quiere generar la nueva captura:")
	print("###########################################")
	print("1. Intercambiando las direcciones Ethernet")
	print("2. Intercambiando las direcciones IP")
	print("3. Intercambiando las direcciones Ethernet e IP")
	print("4. Intercambiando los puertos TCP/UDP")
	print("5. Intercambiando las direcciones IP y los puertos TCP/UDP")
	print("6. Intercambiando las direcciones Ethernet, IP y los puertos TCP/UDP")
	print("")

# Lee la opción introducida por el usuario.
def getOption():
	# Para leer de teclado:
	# https://docs.python.org/3/library/functions.html#input
	num = input("Su opción es: ")
	return num

# Genera una nueva captura intercambiando las direcciones Ethernet.
def exchangeEthernetDirs(goodPcap, badPcap):
	packets = rdpcap(goodPcap)
	for packet in packets:
		EtherSrc = packet[Ether].src
		packet[Ether].src = packet[Ether].dst
		packet[Ether].dst = EtherSrc
	wrpcap(badPcap, packets)

# Genera una nueva captura intercambiando las direcciones IP.
def exchangeIPDirs(goodPcap, badPcap):
	packets = rdpcap(goodPcap)
	for packet in packets:
		if IP in packet:					# No todos los paquetes pasan por el nivel IP (ARP por ejemplo)
			IPSrc = packet[IP].src
			packet[IP].src = packet[IP].dst
			packet[IP].dst = IPSrc
	wrpcap(badPcap, packets)

# Genera una nueva captura intercambiando las direcciones Ethernet e IP.
def exchangeEthernetIPDirs(goodPcap, badPcap):
	packets = rdpcap(goodPcap)
	for packet in packets:
		EtherSrc = packet[Ether].src
		packet[Ether].src = packet[Ether].dst
		packet[Ether].dst = EtherSrc
		if IP in packet:
			IPSrc = packet[IP].src
			packet[IP].src = packet[IP].dst
			packet[IP].dst = IPSrc
	wrpcap(badPcap, packets)

# Genera una nueva captura intercambiando los puertos TCP/UDP.
def exchangeTCPUDPPorts(goodPcap, badPcap):
	packets = rdpcap(goodPcap)
	for packet in packets:
		if TCP in packet:
			TCPSPort = packet[TCP].sport
			packet[TCP].sport = packet[TCP].dport
			packet[TCP].dport = TCPSPort
		if UDP in packet:
			UDPSPort = packet[UDP].sport
			packet[UDP].sport = packet[UDP].dport
			packet[UDP].dport = UDPSPort
	wrpcap(badPcap, packets)

# Genera una nueva captura intercambiando las direcciones IP y los puertos TCP/UDP.
def exchangeIPDirsTCPUDPPorts(goodPcap, badPcap):
	packets = rdpcap(goodPcap)
	for packet in packets:
		if IP in packet:
			IPSrc = packet[IP].src
			packet[IP].src = packet[IP].dst
			packet[IP].dst = IPSrc
		if TCP in packet:
			TCPSPort = packet[TCP].sport
			packet[TCP].sport = packet[TCP].dport
			packet[TCP].dport = TCPSPort
		if UDP in packet:
			UDPSPort = packet[UDP].sport
			packet[UDP].sport = packet[UDP].dport
			packet[UDP].dport = UDPSPort
	wrpcap(badPcap, packets)

# Genera una nueva captura intercambiando las direcciones Ethernet, IP y los puertos TCP/UDP
def exchangeEthernetIPDirsTCPUDPPOrts(goodPcap, badPcap):
	packets = rdpcap(goodPcap)
	for packet in packets:
		EtherSrc = packet[Ether].src
		packet[Ether].src = packet[Ether].dst
		packet[Ether].dst = EtherSrc
		if IP in packet:
			IPSrc = packet[IP].src
			packet[IP].src = packet[IP].dst
			packet[IP].dst = IPSrc
		if TCP in packet:
			TCPSPort = packet[TCP].sport
			packet[TCP].sport = packet[TCP].dport
			packet[TCP].dport = TCPSPort
		if UDP in packet:
			UDPSPort = packet[UDP].sport
			packet[UDP].sport = packet[UDP].dport
			packet[UDP].dport = UDPSPort
	wrpcap(badPcap, packets)

# Procesa la opción elegida por el usuario.
def processOption(num, goodPcap, badPcap):
	if num == "1":
		exchangeEthernetDirs(goodPcap, badPcap)
	elif num == "2":
		exchangeIPDirs(goodPcap, badPcap)
	elif num == "3":
		exchangeEthernetIPDirs(goodPcap, badPcap)
	elif num == "4":
		exchangeTCPUDPPorts(goodPcap, badPcap)
	elif num == "5":
		exchangeIPDirsTCPUDPPorts(goodPcap, badPcap)
	elif num == "6":
		exchangeEthernetIPDirsTCPUDPPOrts(goodPcap, badPcap)
	else:
		print("Esa opción no existe")
		sys.exit()

goodPcap, badPcap = checkExecution()
showMenu()
num = getOption()
processOption(num, goodPcap, badPcap)
