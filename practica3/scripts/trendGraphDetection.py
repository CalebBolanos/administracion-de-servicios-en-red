import sys
import rrdtool
import time
import datetime
from Notify import send_alert_attached
from getSNMP import consultaSNMP
import time

rrdpath = '/home/caleb/Documentos/GitHub/administracion-de-servicios-en-red/practica3/RRD/'
imgpath = '/home/caleb/Documentos/GitHub/administracion-de-servicios-en-red/practica3/IMG/'


def generarGraficaCPU(ultima_lectura):
    nombre_agente = consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.1.5.0')
    tiempo_final = int(ultima_lectura)
    tiempo_inicial = tiempo_final - 1800
    ret = rrdtool.graphv(imgpath + "deteccionCPU.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_final),
                         "--vertical-label=Carga de CPU (%)",
                         '--lower-limit', '0',
                         '--upper-limit', '100',
                         "--title=Carga del CPU del agente Usando SNMP y RRDtools \n Detección de umbrales\n {}".format(
                             nombre_agente),
                         "DEF:cargaCPU=" + rrdpath + "trend.rrd:CPUload:AVERAGE",
                         "VDEF:cargaMAX=cargaCPU,MAXIMUM",
                         "VDEF:cargaMIN=cargaCPU,MINIMUM",
                         "VDEF:cargaSTDEV=cargaCPU,STDEV",
                         "VDEF:cargaLAST=cargaCPU,LAST",
                         "CDEF:umbralOperativo=cargaCPU,20,LT,0,cargaCPU,IF",
                         "CDEF:umbralSobrecarga=cargaCPU,60,LT,0,cargaCPU,IF",
                         "CDEF:umbralCargaExcesiva=cargaCPU,85,LT,0,cargaCPU,IF",
                         "AREA:cargaCPU#00FF00:Carga del CPU",
                         "AREA:umbralOperativo#FF9F00:Carga CPU entre 20% a 60%",
                         "AREA:umbralSobrecarga#fa8231:Carga CPU entre 60% a 85%",
                         "AREA:umbralCargaExcesiva#ff3838:Carga CPU > 85%",
                         "HRULE:20#FF8F00:Umbral 20%",
                         "HRULE:60#EF6C00:Umbral 60%",
                         "HRULE:85#D84315:Umbral 85%",
                         "PRINT:cargaLAST:%6.2lf",
                         "GPRINT:cargaMIN:%6.2lf %SMIN",
                         "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                         "GPRINT:cargaLAST:%6.2lf %SLAST")


def generarGraficaRAM(ultima_lectura):
    nombre_agente = consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.1.5.0')
    tiempo_final = int(ultima_lectura)
    tiempo_inicial = tiempo_final - 1800
    ret = rrdtool.graphv(imgpath + "deteccionRAM.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_final),
                         "--vertical-label=RAM (Kb)",
                         '--lower-limit', '0',
                         '--upper-limit', '100',
                         "--title=Carga de la RAM del agente Usando SNMP y RRDtools \n Detección de umbrales\n {}".format(
                             nombre_agente),
                         "DEF:cargaRAM=" + rrdpath + "trend.rrd:RAMload:AVERAGE",
                         "VDEF:cargaMAX=cargaRAM,MAXIMUM",
                         "VDEF:cargaMIN=cargaRAM,MINIMUM",
                         "VDEF:cargaSTDEV=cargaRAM,STDEV",
                         "VDEF:cargaLAST=cargaRAM,LAST",
                         "CDEF:umbralOperativo=cargaRAM,1582764,LT,0,cargaRAM,IF",
                         "CDEF:umbralSobrecarga=cargaRAM,2374147,LT,0,cargaRAM,IF",
                         "CDEF:umbralCargaExcesiva=cargaRAM,3363375,LT,0,cargaRAM,IF",
                         "AREA:cargaRAM#00FF00:Carga de RAM",
                         "AREA:umbralOperativo#FF9F00:RAM entre 40% a 60%",
                         "AREA:umbralSobrecarga#fa8231:RAM entre 60% a 85%",
                         "AREA:umbralCargaExcesiva#ff3838:RAM > 85%",
                         "HRULE:1582764#FF8F00:Umbral 40%",
                         "HRULE:2374147#EF6C00:Umbral 60%",
                         "HRULE:3363375#D84315:Umbral 85%",
                         "PRINT:cargaLAST:%6.2lf",
                         "GPRINT:cargaMIN:%6.2lf %SMIN",
                         "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                         "GPRINT:cargaLAST:%6.2lf %SLAST")


def generarGraficaRED(ultima_lectura):
    nombre_agente = consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.1.5.0')
    tiempo_final = int(ultima_lectura)
    tiempo_inicial = tiempo_final - 1800
    ret = rrdtool.graphv(imgpath + "deteccionRED.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_final),
                         "--vertical-label=Octetos",
                         '--lower-limit', '0',
                         '--upper-limit', '100',
                         "--title=Carga de la red del agente Usando SNMP y RRDtools \n Detección de umbrales\n {}".format(
                             nombre_agente),
                         "DEF:cargaRED=" + rrdpath + "trend.rrd:OctetsInload:AVERAGE",
                         "DEF:cargaRED_2=" + rrdpath + "trend.rrd:OctetsOutload:AVERAGE",
                         "VDEF:cargaMAX=cargaRED,MAXIMUM",
                         "VDEF:cargaMIN=cargaRED,MINIMUM",
                         "VDEF:cargaSTDEV=cargaRED,STDEV",
                         "VDEF:cargaLAST=cargaRED,LAST",
                         "VDEF:cargaMAX_2=cargaRED_2,MAXIMUM",
                         "VDEF:cargaMIN_2=cargaRED_2,MINIMUM",
                         "VDEF:cargaSTDEV_2=cargaRED_2,STDEV",
                         "VDEF:cargaLAST_2=cargaRED_2,LAST",
                         "CDEF:umbralOperativoIn=cargaRED,20,LT,0,cargaRED,IF",
                         "CDEF:umbralSobrecargaIn=cargaRED,50,LT,0,cargaRED,IF",
                         "CDEF:umbralCargaExcesivaIn=cargaRED,90,LT,0,cargaRED,IF",
                         "CDEF:umbralOperativoOut=cargaRED_2,20,LT,0,cargaRED_2,IF",
                         "CDEF:umbralSobrecargaOut=cargaRED_2,50,LT,0,cargaRED_2,IF",
                         "CDEF:umbralCargaExcesivaOut=cargaRED_2,90,LT,0,cargaRED_2,IF",
                         "LINE:cargaRED#66BB6A:Octetos de entrada",
                         "LINE:umbralOperativoIn#43A047:InOctets entre 20 a 50",
                         "LINE:umbralSobrecargaIn#388E3C:InOctets entre 50 a 90",
                         "LINE:umbralCargaExcesivaIn#1B5E20:InOctets > 90",
                         "LINE:cargaRED_2#29B6F6:Octetos de salida",
                         "LINE:umbralOperativoOut#039BE5:InOctets entre 20 a 50",
                         "LINE:umbralSobrecargaOut#0288D1:InOctets entre 50 a 90",
                         "LINE:umbralCargaExcesivaOut#01579B:InOctets > 90",
                         "HRULE:20#FF8F00:Umbral 20%",
                         "HRULE:50#EF6C00:Umbral 50%",
                         "HRULE:90#D84315:Umbral 90%",
                         "PRINT:cargaLAST:%6.2lf",
                         "GPRINT:cargaMIN:%6.2lf %SMIN",
                         "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                         "GPRINT:cargaLAST:%6.2lf %SLAST")


def detectarUmbrales():
    while (1):
        ultima_actualizacion = rrdtool.lastupdate(rrdpath + "trend.rrd")
        timestamp = ultima_actualizacion['date'].timestamp()
        datoCPU = ultima_actualizacion['ds']["CPUload"]
        datoRAM = ultima_actualizacion['ds']["RAMload"]
        datoOctetosEntrada = ultima_actualizacion['ds']["OctetsInload"]
        datoOctetosSalida = ultima_actualizacion['ds']["OctetsOutload"]

        print('N:' + str(datoCPU) + ':' + str(datoRAM) + ':' + str(datoOctetosEntrada) + ':' + str(datoOctetosSalida))

        elementos_sobrecargados = ['CPU', 'RAM', 'RED']
        if 20 < datoCPU < 60 or 1582764 < datoRAM < 2374147 or 20 < datoOctetosSalida < 50 or 20 < datoOctetosEntrada < 50:
            cadena = "Sobrepasa primer umbral (Umbral operativo)"
            generarGraficaCPU(int(timestamp))
            generarGraficaRAM(int(timestamp))
            generarGraficaRED(int(timestamp))
            send_alert_attached(cadena, elementos_sobrecargados)
            print(cadena)

        if 60 < datoCPU < 85 or 2374147 < datoRAM < 3363375 or 50 < datoOctetosSalida < 90 or 50 < datoOctetosEntrada < 90:
            cadena = "Sobrepasa segundo umbral (Umbral Sobrecarga)"
            generarGraficaCPU(int(timestamp))
            generarGraficaRAM(int(timestamp))
            generarGraficaRED(int(timestamp))
            send_alert_attached(cadena, elementos_sobrecargados)
            print(cadena)

        if datoCPU > 65 or datoRAM > 3363375 or datoOctetosSalida > 90 or datoOctetosEntrada > 90:
            cadena = "Sobrepasa tercer umbral (Umbral Carga excesiva)"
            generarGraficaCPU(int(timestamp))
            generarGraficaRAM(int(timestamp))
            generarGraficaRED(int(timestamp))
            send_alert_attached(cadena, elementos_sobrecargados)
            print(cadena)


        time.sleep(20)
