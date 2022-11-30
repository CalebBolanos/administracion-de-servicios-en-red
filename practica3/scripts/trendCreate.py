import rrdtool
ret = rrdtool.create("/home/caleb/Documentos/GitHub/administracion-de-servicios-en-red/practica3/RRD/trend.rrd",
                     "--start",'N',
                     "--step",'60',
                     "DS:CPUload:GAUGE:60:0:100",
                     "DS:RAMload:GAUGE:60:0:4000000",
                     "DS:OctetsInload:GAUGE:60:0:9000000",
                     "DS:OctetsOutload:GAUGE:60:0:9000000",
                     "RRA:AVERAGE:0.5:1:24")
if ret:
    print (rrdtool.error())
