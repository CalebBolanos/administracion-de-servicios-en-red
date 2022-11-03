
import rrdtool

#por cada atributo de contabilidad crear su Data Source correspondiente
oids = {
    'Paquetes multicast que ha enviado la interfaz de la interfaz de red de un agente': 'a',
    'Paquetes IP que los protocolos locales (incluyendo ICMP) suministraron a IP en las solicitudes de transmisión.': 'b',
    'Mensajes ICMP que ha recibido el agente': 'c',
    'Número de segmentos TCP transmitidos que contienen uno o más octetos transmitidos previamente': 'd',
    'Datagramas enviados por el dispositivo': 'e'
}
print(oids)
#
"""
ret = rrdtool.create("traficoRED.rrd",
                     "--start",'N',
                     "--step",'60',
                     "DS:inoctets:COUNTER:120:U:U",
                     "DS:outoctets:COUNTER:120:U:U",
                     "RRA:AVERAGE:0.5:5:5",
                     "RRA:AVERAGE:0.5:1:20")

if ret:
    print (rrdtool.error())
"""