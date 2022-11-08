
import rrdtool

# por cada atributo de contabilidad crear su Data Source correspondiente
atributos_contabilidad = [
    'paquetes_multicast',
    'paquetes_ip',
    'mensajes_icmp',
    'segmentos_tcp',
    'datagramas'
]

#guarda un dia en resolucion de un minuto
def crear_rrd(nombre_agente):
    datasources = []
    for atributo in atributos_contabilidad:
        datasources.append("DS:{}:COUNTER:300:U:U".format(atributo))
    rrdx = rrdtool.create("contabilidad_{}.rrd".format(nombre_agente),
                             "--start", 'N',
                             "--step", '60',#acepta info cada 60 segundos
                             datasources,
                             "RRA:AVERAGE:0.5:1:1440",)

    if rrdx:
        print(rrdtool.error())
    rrdtool.dump("contabilidad_{}.rrd".format(nombre_agente), "contabilidad_{}.xml".format(nombre_agente))
