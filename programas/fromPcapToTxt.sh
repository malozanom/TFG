#! /bin/sh

###############################################################################
# Script de shell que se encarga de extraer en la captura [inputFile.pcap] los
# bytes de los paquetes indicados en [filterByRangePackets]. La extracción se
# lleva al fichero de texto [outputFile.txt].

# ENTRADAS:
# [inputFile.pcap] => captura donde se encuentran los paquetes.
# [filterByRangePackets] => rango de paquetes en el cual queremos extraer los
#							bytes.

# SALIDAS:
# [outputFile.txt] => fichero de texto a donde se lleva la extracción.

# EJEMPLO DE EJECUCIÓN:
# ./fromPcapToTxt.sh captura.pcap "frame.number <= 1000" captura-train.txt

# Pasos:
# 1. Quitamos los 4 primeros dígitos + los 2 espacios (la primera columna).
# 2. Quitamos los 16 últimos carácteres (la última columna).
# 3. Quitamos los espacios que quedan al final de cada línea.
# 4. Sustituimos los "\n" por " " (conseguimos que los paquetes estén en la misma línea separados por ";").
# 5. Sustituimos " ; " por "\n" (conseguimos que haya un paquete por línea).
# 6. Quitamos la última línea ya que terminaba en "\n".
###############################################################################

if [ ! $# -eq 3 ] ; then
	echo "usage: $0 [inputFile.pcap] [filterByRangePackets] [outputFile.txt]"
	exit 1
fi

tshark -x -r $1 -S ";" -Y "$2" | sed 's/^[0-9a-f]*  //' | sed 's/.\{16\}$//' \
	| sed 's/ *$//' | tr "\n" " " | sed 's/ ; /\n/g' | head -c -1 > $3
