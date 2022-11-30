import time
import rrdtool
from getSNMP import consultaSNMP
rrdpath = '/home/caleb/Documentos/GitHub/administracion-de-servicios-en-red/practica3/RRD/'

oids_cpu = {
    'cpu1': '1.3.6.1.2.1.25.3.3.1.2.196608',
    'cpu2': '1.3.6.1.2.1.25.3.3.1.2.196609',
    'cpu3': '1.3.6.1.2.1.25.3.3.1.2.196610',
    'cpu4': '1.3.6.1.2.1.25.3.3.1.2.196611',
}

oid_ram_total = '1.3.6.1.4.1.2021.4.5.0'
oid_ram_libre = '1.3.6.1.4.1.2021.4.6.0'

oids_octetos_entrada = {
    'octeto1': '1.3.6.1.2.1.2.2.1.10.1',
    'octeto2': '1.3.6.1.2.1.2.2.1.10.2',
}
oids_octetos_salida= {
    'octeto1': '1.3.6.1.2.1.2.2.1.16.1',
    'octeto2': '1.3.6.1.2.1.2.2.1.16.2',
}


def actualizarDatos():
    while 1:
        #carga de cpu
        suma = 0
        for cpu in oids_cpu:
            suma += int(consultaSNMP('comunidadASR','localhost',oids_cpu[cpu]))

        carga_cpu = (suma)/len(oids_cpu)

        #carga de ram en kb
        carga_ram = int(consultaSNMP('comunidadASR','localhost', oid_ram_total)) - int(consultaSNMP('comunidadASR','localhost', oid_ram_libre))

        #carga de red (total de octetos)
        suma_entrada= 0
        suma_salida = 0
        for octetos_in in oids_octetos_entrada:
            suma_entrada += int(consultaSNMP('comunidadASR', 'localhost', oids_octetos_entrada[octetos_in]))
        for octetos_out in oids_octetos_salida:
            suma_salida += int(consultaSNMP('comunidadASR', 'localhost', oids_octetos_salida[octetos_out]))

        valor = "N:" + str(carga_cpu) + ":" + str(carga_ram) + ":" + str(suma_entrada/1000000)+ ":" + str(suma_salida/1000000)
        #print(valor)
        rrdtool.update(rrdpath+'trend.rrd', valor)
        time.sleep(5)

    if ret:
        print (rrdtool.error())
        time.sleep(300)
