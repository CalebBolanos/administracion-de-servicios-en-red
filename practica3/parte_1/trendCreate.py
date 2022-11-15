import rrdtool
ret = rrdtool.create("/home/caleb/Documentos/GitHub/administracion-de-servicios-en-red/practica3/RRD/trend.rrd",
                     "--start",'N',
                     "--step",'60',
                     "DS:CPUload:GAUGE:60:0:100",
                     "RRA:AVERAGE:0.5:1:24")
if ret:
    print (rrdtool.error())
