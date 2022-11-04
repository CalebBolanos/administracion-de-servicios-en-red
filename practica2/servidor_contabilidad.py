"""
Practica 2: Adquisición de información 
Caleb Salomón Bolaños Ramos - 4CM13 - 2020630043
++++++


"""  #

import rrdtool
from pysnmp.hlapi import *
from datetime import date
from datetime import datetime
from operacionesSNMP import snmpget

#atributos de contabilidad
oids = {
    'Paquetes multicast que ha enviado la interfaz de la interfaz de red de un agente': 'a',
    'Paquetes IP que los protocolos locales (incluyendo ICMP) suministraron a IP en las solicitudes de transmisión.': 'b',
    'Mensajes ICMP que ha recibido el agente': 'c',
    'Número de segmentos TCP transmitidos que contienen uno o más octetos transmitidos previamente': 'd',
    'Datagramas enviados por el dispositivo': 'e'
}


def calcular_bloque_ejercicio(fecha_nacimiento):
    fecha_actual = date(2022, 10, 27)

    delta = fecha_actual - fecha_nacimiento
    dias_vividos = delta.days
    # print(dias_vividos)

    bloque_ejercicios = (dias_vividos % 3) + 1

    return bloque_ejercicios


def imprimir_diccionario(diccionario):
    for i, (key, value) in enumerate(diccionario.items()):
        print("{}- {} ({})".format(i, key, value))


def crear_datetime(str_fecha, str_hora):
    anio, mes, dia = map(int, str_fecha.split('-'))
    horas, minutos = map(int, str_hora.split(':'))
    return datetime(anio, mes, dia, horas, minutos)


print()
# imprimir_diccionario(oids)

print("Practica 2 - Servidor de contabilidad")
print("Caleb Salomón Bolaños Ramos - 4CM13 - 2020630043")


print("Generar reporte de bloque " + str(calcular_bloque_ejercicio(date(2001, 2, 11))) + "\n")


comunidad_agente = input("Escribe el nombre de la comunidad del Agente (Elemento de servicio): ")
ip_agente = input("Escribe la direccion ip del Agente (Elemento de servicio): ")

print(snmpget(comunidad_agente, ip_agente, "1.3.6.1.2.1.1.1.0"))


# seleccion = input('Digita el bloque del cual se generara el reporte: ')
fecha_inicio = input('Escribe la fecha de inicio en formato AAAA-MM-DD: ')
hora_inicio = input('Escribe la hora de inicio en formato HH:MM: ')

fecha_final = input('Escribe la fecha de fin en formato AAAA-MM-DD: ')
hora_final = input('Escribe la hora de fin en formato HH:MM: ')

datetime_inicio = crear_datetime(fecha_inicio, hora_inicio)
datetime_final = crear_datetime(fecha_final, hora_final)

print(datetime_inicio, datetime_final)