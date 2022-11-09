import sys
import rrdtool
import time

strings_contabilidad = {
    'paquetes_multicast': 'Paquetes multicast que ha enviado \nla interfaz de la interfaz de red de un agente',
    'paquetes_ip': 'Paquetes IP que los protocolos locales (incluyendo ICMP)\n suministraron a IP en las solicitudes de transmisión.',
    'mensajes_icmp': 'Mensajes ICMP que ha \nrecibido el agente',
    'segmentos_tcp': 'Número de segmentos TCP transmitidos que contienen\n uno o más octetos transmitidos previamente',
    'datagramas': 'Datagramas enviados por\n el dispositivo',
}


def generar_graficas_rrd(inicio, fin, nombre):

    rrdtool.dump("contabilidad_{}.rrd".format(nombre), "contabilidad_{}.xml".format(nombre))

    #separar cada datasorce para hacer su propia grafica
    for datasource, titulo in strings_contabilidad.items():
        ret = rrdtool.graphv( "{}_{}.png".format(nombre, datasource),
                             "--start",inicio,
                             "--end",fin,
                             "--vertical-label=Cantidad",
                             "--title={}".format(titulo),
                             "DEF:traficods=contabilidad_{}.rrd:{}:AVERAGE".format(nombre, datasource),
                             "LINE1:traficods#f9ca24:{}".format(datasource),#paquetes_multicast
                             )

"""
"DEF:traficoPaquetesIP=contabilidad.rrd:paquetes_ip:AVERAGE",
                         "LINE1:traficoPaquetesIP#f0932b:paq_ip",#paquetes_ip
                         "DEF:traficoMensajesICMP=contabilidad.rrd:mensajes_icmp:AVERAGE",
                         "LINE1:traficoMensajesICMP#eb4d4b:men_icmp",#mensajes_icmp mandar pings
                         "DEF:traficoSegmentosTCP=contabilidad.rrd:segmentos_tcp:AVERAGE",
                         "LINE1:traficoSegmentosTCP#6ab04c:seg_tcp",#segmentos_tcp
                         "DEF:traficoDatagramas=contabilidad.rrd:datagramas:AVERAGE",
                         "LINE1:traficoDatagramas#0000FF:datagramas",#datagramas
"""