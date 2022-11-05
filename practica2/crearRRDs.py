
import rrdtool

# por cada atributo de contabilidad crear su Data Source correspondiente
atributos_contabilidad = [
    'paquetes_multicast',
    'paquetes_ip',
    'mensajes_icmp',
    'segmentos_tcp',
    'datagramas'
]

datasources = []
for atributo in atributos_contabilidad:
    datasources.append("DS:{}:COUNTER:120:U:U".format(atributo))


rrdx = rrdtool.create("contabilidad.rrd",
                         "--start", 'N',
                         "--step", '60',#acepta info cada 60 segundos
                         datasources,
                         "RRA:AVERAGE:0.5:5:5",)

if rrdx:
    print(rrdtool.error())

# rrdtool.dump("contabilidad.rrd", "contabilidad.xml")
print(datasources)