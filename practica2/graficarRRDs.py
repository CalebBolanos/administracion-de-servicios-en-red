import sys
import rrdtool
import time

tiempo_actual = int(time.time())
#Grafica desde el tiempo actual menos diez minutos
tiempo_inicial = tiempo_actual - 2400

#separar cada datasorce para hacer su propia grafica
ret = rrdtool.graph( "contabilidad.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_actual),
                     "--vertical-label=Bytes/s",
                     "--title=Tráfico de Red de un agente \n Usando SNMP y RRDtools",
                     "DEF:traficoPaquetesMulticast=contabilidad.rrd:paquetes_multicast:AVERAGE",
                     "LINE1:traficoPaquetesMulticast#00FFFF:paq_multicast",#paquetes_multicast
                     "DEF:traficoPaquetesIP=contabilidad.rrd:paquetes_ip:AVERAGE",
                     "LINE1:traficoPaquetesIP#AAAAAA:paq_ip",#paquetes_ip
                     "DEF:traficoMensajesICMP=contabilidad.rrd:mensajes_icmp:AVERAGE",
                     "LINE1:traficoMensajesICMP#BBBBBB:men_icmp",#mensajes_icmp
                     "DEF:traficoSegmentosTCP=contabilidad.rrd:segmentos_tcp:AVERAGE",
                     "LINE1:traficoSegmentosTCP#CCCCCC:seg_tcp",#segmentos_tcp
                     "DEF:traficoDatagramas=contabilidad.rrd:datagramas:AVERAGE",
                     "LINE1:traficoDatagramas#0000FF:datagramas",#datagramas
                     )
