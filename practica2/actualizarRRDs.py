import time
import rrdtool
from operacionesSNMP import snmpget

#por cada atributo de contabilidad crear su Data Source correspondiente
atributos_contabilidad = {
    'paquetes_multicast': '1.3.6.1.2.1.2.2.1.12.1',
    'paquetes_ip': '1.3.6.1.2.1.4.10.0',
    'mensajes_icmp': '1.3.6.1.2.1.5.1.0',
    'segmentos_tcp': '1.3.6.1.2.1.6.12.0',
    'datagramas': '1.3.6.1.2.1.7.4.0'
}

valor_datasource = 0
nombres_ds = ''
for datasource, oid in atributos_contabilidad.items():
    nombres_ds += str(datasource) + ":"

nombres_ds = nombres_ds[:-1]

print(nombres_ds)

while 1:
    valor = "N"
    for datasource, oid in atributos_contabilidad.items():
        valor_datasource = int(snmpget('comunidadASR','localhost', oid))

        valor += ":" + str(valor_datasource)
        # print(datasource, valor)
        #rrdtool.dump('traficoRED.rrd','traficoRED.xml')

    print(valor)
    rrdtool.update('contabilidad.rrd', valor)
    time.sleep(1*60)
