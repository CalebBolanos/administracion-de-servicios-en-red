import sys
import rrdtool
import time
rrdtool.dump("contabilidad.rrd", "contabilidad.xml")
tiempo_actual = int(time.time())
#Grafica desde el tiempo actual menos diez minutos
tiempo_inicial = tiempo_actual - (60*20)

#separar cada datasorce para hacer su propia grafica
ret = rrdtool.graphv( "contabilidad.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_actual),
                     "--vertical-label=Bytes/s",
                     "--title=Tráfico de Red de un agente \n Usando SNMP y RRDtools",
                     "DEF:traficoPaquetesMulticast=contabilidad.rrd:paquetes_multicast:AVERAGE",
                     "LINE1:traficoPaquetesMulticast#f9ca24:paq_multicast",#paquetes_multicast
                     "DEF:traficoPaquetesIP=contabilidad.rrd:paquetes_ip:AVERAGE",
                     "LINE1:traficoPaquetesIP#f0932b:paq_ip",#paquetes_ip
                     "DEF:traficoMensajesICMP=contabilidad.rrd:mensajes_icmp:AVERAGE",
                     "LINE1:traficoMensajesICMP#eb4d4b:men_icmp",#mensajes_icmp
                     "DEF:traficoSegmentosTCP=contabilidad.rrd:segmentos_tcp:AVERAGE",
                     "LINE1:traficoSegmentosTCP#6ab04c:seg_tcp",#segmentos_tcp
                     "DEF:traficoDatagramas=contabilidad.rrd:datagramas:AVERAGE",
                     "LINE1:traficoDatagramas#0000FF:datagramas",#datagramas
                     )
