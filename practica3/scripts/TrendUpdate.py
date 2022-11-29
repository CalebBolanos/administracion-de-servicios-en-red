import time
import rrdtool
from getSNMP import consultaSNMP
rrdpath = '/home/caleb/Documentos/GitHub/administracion-de-servicios-en-red/practica3/RRD/'
carga_CPU = 0

while 1:
    cpu_uno = int(consultaSNMP('comunidadASR','localhost','1.3.6.1.2.1.25.3.3.1.2.196608'))
    cpu_dos = int(consultaSNMP('comunidadASR','localhost','1.3.6.1.2.1.25.3.3.1.2.196609'))
    promedio = (cpu_uno + cpu_dos)/2
    print ("N:" + str(cpu_uno) + ":" + str(cpu_dos) + ":" + str(promedio))
    valor = "N:" + str(promedio)
    print(valor)
    rrdtool.update(rrdpath+'trend.rrd', valor)
    time.sleep(5)

if ret:
    print (rrdtool.error())
    time.sleep(300)
