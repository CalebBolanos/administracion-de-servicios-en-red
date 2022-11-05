import sys
import rrdtool
import time

tiempo_actual = int(time.time())
#Grafica desde el tiempo actual menos diez minutos
tiempo_inicial = tiempo_actual - 1200
ret = rrdtool.graph( "traficoRED.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_actual),
                     "--vertical-label=Bytes/s",
                     "--title=Tráfico de Red de un agente \n Usando SNMP y RRDtools",
                     "DEF:traficoEntrada=datagramas.rrd:datagramas:AVERAGE",
                     "CDEF:escalaIn=traficoEntrada,8,*",
                     "LINE1:escalaIn#0000FF:datagramas",)
