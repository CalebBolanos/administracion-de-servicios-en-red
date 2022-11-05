
import rrdtool

# por cada atributo de contabilidad crear su Data Source correspondiente
atributos_contabilidad = [
    'paquetes_multicast',
    'paquetes_ip',
    'mensajes_icmp',
    'segmentos_tcp',
    'datagramas'
]

for atributo in atributos_contabilidad:
    rrdx = rrdtool.create("{}.rrd".format(atributo),
                         "--start", 'N',
                         "--step", '60',#acepta info cada 60 segundos
                         "DS:{}:COUNTER:120:U:U".format(atributo),#nombreds:dstype:heartbeat(segundos):min:max
                         "RRA:AVERAGE:0.5:5:5",)

    if rrdx:
        print(rrdtool.error())

    # rrdtool.dump("{}.rrd".format(atributo), "{}.xml".format(atributo))
