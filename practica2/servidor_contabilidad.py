"""
Practica 2: Adquisición de información 
Caleb Salomón Bolaños Ramos - 4CM13 - 2020630043
++++++


"""  #

import rrdtool
import time
from pysnmp.hlapi import *
from threading import Thread
from datetime import date
from datetime import datetime
from operacionesSNMP import snmpget
from crearRRDs import crear_rrd
from graficarRRDs import generar_graficas_rrd
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format="\n[%(levelname)s] (%(threadName)-s) %(message)s")
opcion = ''

JSON_INICIAL = """
{
    "agentes": [

    ]
}
"""

#atributos de contabilidad
strings_contabilidad = {
    'Paquetes multicast que ha enviado la interfaz de la interfaz de red de un agente': '1.3.6.1.2.1.2.2.1.12.1',
    'Paquetes IP que los protocolos locales (incluyendo ICMP) suministraron a IP en las solicitudes de transmisión.': '1.3.6.1.2.1.4.10.0',
    'Mensajes ICMP que ha recibido el agente': '1.3.6.1.2.1.5.1.0',
    'Número de segmentos TCP transmitidos que contienen uno o más octetos transmitidos previamente': '1.3.6.1.2.1.6.12.0',
    'Datagramas enviados por el dispositivo': '1.3.6.1.2.1.7.4.0'
}

atributos_contabilidad = {
    'paquetes_multicast': '1.3.6.1.2.1.2.2.1.12.1',
    'paquetes_ip': '1.3.6.1.2.1.4.10.0',
    'mensajes_icmp': '1.3.6.1.2.1.5.1.0',
    'segmentos_tcp': '1.3.6.1.2.1.6.12.0',
    'datagramas': '1.3.6.1.2.1.7.4.0'
}


def inicializar_json():
    """
    funcion encargada de inicializar el archivo dispositivos.json, el cual contiene la informacion de los dispositivos.
    Dicha información es cargada en diccionario_agentes, la cual se utiliza a lo largo del programa.
    Si no existe el archivo se crea uno nuevo y asi, se garantiza la persistencia de datos
    :return:
    """
    global diccionario_agentes
    global hilo_actualizar_rrds
    try:
        with open("agentes.json", "r") as archivo:
            diccionario_agentes = json.load(archivo)

    except IOError:
        print('Archivo agentes.json no encontrado, se creara uno nuevo.')
        diccionario_agentes = json.loads(JSON_INICIAL)

    hilo_actualizar_rrds = Thread(target=actualizar_rrds)
    hilo_actualizar_rrds.start()


def guardar_cambios():
    """
    funcion que se encarga de guardar la informacion de diccionario_agentes en agentes.json, es usada
    cada que se agrega, edita o elimina un dispositivo
    :return:
    """
    with open('agentes.json', 'w') as archivo:
        json.dump(diccionario_agentes, archivo, indent=4)
    print("agentes.json actualizado")


def listar_agentes():
    """
    imprime todos los agentes guardados por el usuario
    :return:
    """
    print("\nAgentes disponibles: ")
    for agente, i in enumerate(diccionario_agentes["agentes"]):
        print(agente, i)


def agregar_agente():
    """
    Funcion encargada de agregar un agente, en donde se especifica la comunidad, e ip que lo conforman.
    :return:
    """
    print("\nAgregar dispositivo")
    comunidad = input("Escribe el nombre de la comunidad del dispositivo: ")
    ip = input("Escribe la direccion ip del dispositivo: ")
    diccionario_agentes["agentes"].append(
        {'comunidad': comunidad, 'ip': ip})

    crear_rrd(comunidad)
    # falta hacer update de agente, si es el primero crear hilo
    guardar_cambios()


def eliminar_agente():
    """
    funcion que permite al usuario eliminar la información y rrd de un agente dado.
    Se borran los datos del agente del archivo agente.json y si existe un rrd generado de dicho
    agente tambien se elimina del disco.
    :return:
    """
    listar_agentes()
    agente_elegido = int(input("\nSelecciona el agente a eliminar: "))

    print("Agente seleccionado:")
    agente_a_borrar = diccionario_agentes["agentes"][agente_elegido]
    print(agente_a_borrar)
    str_borrar = input("\nEstas seguro que quieres eliminar el sigiente agente? s/n: ")

    if str_borrar == "s":
        if os.path.exists("contabilidad_{}.rrd".format(agente_a_borrar["comunidad"])):
            os.remove("contabilidad_{}.rrd".format(agente_a_borrar["comunidad"]))
            os.remove("contabilidad_{}.xml".format(agente_a_borrar["comunidad"]))
            print("contabilidad_{}.rrd".format(agente_a_borrar["comunidad"]) + "eliminado")

        del diccionario_agentes["agentes"][agente_elegido]

        print("Agente eliminado correctamente")
        guardar_cambios()
        # falta quitar del update a agente eliminado
    else:
        print("No se ha eliminado el dispositivo seleccionado")


def imprimir_menu():
    print("\nMenu principal:")
    print("1. Agregar agente")
    print("2. Eliminar agente")
    print("3. Listar agentes monitorizados")
    print("4. Generar reporte")
    print("5. Salir")


def actualizar_rrds():
    valor_datasource = 0
    while opcion != 5:

        for agente in diccionario_agentes["agentes"]:
            valor = "N"
            for datasource, oid in atributos_contabilidad.items():
                valor_datasource = int(snmpget(agente["comunidad"], agente["ip"], oid))

                valor += ":" + str(valor_datasource)

            logging.info(agente["comunidad"] + " " + valor)
            rrdtool.update("contabilidad_{}.rrd".format(agente["comunidad"]), valor)
        time.sleep(1 * 60)

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


def generar_reporte():
    listar_agentes()
    agente_elegido = int(input("\nSelecciona el agente a generar el reporte: "))

    print("Agente seleccionado:")
    agente_seleccionado = diccionario_agentes["agentes"][agente_elegido]

    fecha_inicio = input('Escribe la fecha de inicio del reporte en formato AAAA-MM-DD: ')
    hora_inicio = input('Escribe la hora de inicio del reporte en formato HH:MM: ')

    fecha_final = input('Escribe la fecha de fin del reporte en formato AAAA-MM-DD: ')
    hora_final = input('Escribe la hora de fin del reporte en formato HH:MM: ')

    datetime_inicio = crear_datetime(fecha_inicio, hora_inicio)
    datetime_final = crear_datetime(fecha_final, hora_final)

    posix_inicio = str(time.mktime(datetime_inicio.timetuple()))[:-2]
    posix_final = str(time.mktime(datetime_final.timetuple()))[:-2]

    print(posix_inicio, posix_final)
    # print(str(posix_inicio)[:-2], str(posix_final)[:-2])

    generar_graficas_rrd(posix_inicio, posix_final, agente_seleccionado["comunidad"])
    print(time.mktime(datetime_final.timetuple()))


# imprimir_diccionario(oids)
inicializar_json()
print("Practica 2 - Servidor de contabilidad")
print("Caleb Salomón Bolaños Ramos - 4CM13 - 2020630043")
print("Usando contabilidad del bloque " + str(calcular_bloque_ejercicio(date(2001, 2, 11))) + "\n")

while True:
    imprimir_menu()
    try:
        opcion = int(input('\nIngresa una opción: '))
    except:
        print('Ingresa un número')

    if opcion == 1:
        agregar_agente()
    elif opcion == 2:
        eliminar_agente()
    elif opcion == 3:
        listar_agentes()
    elif opcion == 4:
        generar_reporte()
    elif opcion == 5:
        print('Adios! :)')
        hilo_actualizar_rrds.join()
        exit()
    else:
        print('Opcion invalida. Introduce un número del 1 al 5.')




"""
comunidad_agente = input("Escribe el nombre de la comunidad del Agente (Elemento de servicio): ")
ip_agente = input("Escribe la direccion ip del Agente (Elemento de servicio): ")



crear_rrd(comunidad_agente)

fecha_inicio = input('Escribe la fecha de inicio en formato AAAA-MM-DD: ')
hora_inicio = input('Escribe la hora de inicio en formato HH:MM: ')

fecha_final = input('Escribe la fecha de fin en formato AAAA-MM-DD: ')
hora_final = input('Escribe la hora de fin en formato HH:MM: ')

datetime_inicio = crear_datetime(fecha_inicio, hora_inicio)
datetime_final = crear_datetime(fecha_final, hora_final)

print(datetime_inicio, datetime_final)
""" #