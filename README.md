# TFG
Trabajo Fin de Grado - Modelos para la detección de tráfico anómalo en redes IPv4 e IPv6

**Material del repositorio:**
  * `programas` -> contiene el software para:
      * Generar las versiones anómalas de las capturas de tráfico (`generateBadIPv4Pcap.py` y `generateBadIPv6Pcap.py`).
      * Preprocesar las capturas de tráfico (`fromPcapToTxt.sh`).
      * Inyectar las capturas de tráfico en la red neuronal (`readTxtFile.py`).
      * Desarrollar la red neuronal (`NNForNetworkTraffic.py`).
  * `resultados` -> contiene el fichero `resultados.ods` con los datos obtenidos tras probar la red neuronal.
  
Además, en el apartado `releases` se incluyen las capturas de tráfico y los ficheros de texto utilizados para llegar a los resultados anteriores.
