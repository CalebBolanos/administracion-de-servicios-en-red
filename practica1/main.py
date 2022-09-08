"""
Practica 1: Adquisición de información 
Caleb Salomón Bolaños Ramos - 4CM13 - 2020630043
++++++
Este programa es un gestor SNMP el cual monitoriza dispositivos (agentes), de los cuales, se 
obtiene su información a través de consultas SNMP (GET), utilizando la biblioteca pysnmp.

Dentro de este programa se puede:

  * Agregar un dispositivo
  * Editar información de dispositivo
  * Eliminar dispositivo
  * Listar dispositivos existentes
  * Generar reporte de un dispositivo

La información de cada uno de los dispositivos es persistente, ya que es guardado en un json.
También es posible generar reportes en PDF de cada uno de los dispositivos, usando la libreria fpdf.

"""  #
from pysnmp.hlapi import *
from fpdf import FPDF
import json
import os

SNMP_V1 = 0
SNMP_V2 = 1
estado_interfaz = {
    "1": "up",
    "2": "down",
    "3": "testing"
}
JSON_INICIAL = """
{
    "dispositivos": [

    ]
}
"""
informacion_reporte = ["1. Sistema Operativo\n", "2. Nombre del dispositivo\n", "3. Informacion de contacto\n",
                       "4. Ubicacion\n", "5. Numero de interfaces", "6. Estado administrativo de interfaces (Interfaz - Estado)"]
# contiene todos los dispositivos guardados por el usuario
diccionario_dispositivos = {}


def snmpget(dispositivo):
    """
    funcion encargada de hacer consultas snmp de tipo get, dado un dispositivo.
    :param dispositivo: contiene la informacion del dispositivo (comunidad, versionSNMP, ip, puerto) para
    hacer la consulta
    :return varBinds: contiene las respuestas de las consultas (sistema operativo, nombre del dispositivo, informacion
    de contacto, ubicacion y numero de interfaces)
    """
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(dispositivo["comunidad"], mpModel=dispositivo["versionSNMP"]),
        UdpTransportTarget((dispositivo["ip"], dispositivo["puerto"])),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),  # sistema operativo
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')),  # nombre del dispositivo
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.4.0')),  # informacion de contacto
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0')),  # ubicacion
        ObjectType(ObjectIdentity('1.3.6.1.2.1.2.1.0')),  # numero de interfaces
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        return varBinds


def obtener_informacion_interfaces(dispositivo, numero_interfaces):
    """
    funcion encargada de hacer las consultas snmp de tipo get para obtener informacion de la tabla de interfaces (nombre
    de interfaz y estado)
    :param dispositivo: contiene la informacion del dispositivo al cual se le hara la consulta
    :param numero_interfaces: el numero de interfaces que posee el dispositivo
    :return tabla_interfaces: diccionario que contiene las interfaces con sus respectivos estados
    """
    lista_interfaces = []
    oids = []

    # se generan los oids necesarios en funcion del numero de interfaces que tiene el dispositivo
    for i in range(1, numero_interfaces+1):
        oids.append(ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.2.' + str(i)))) # nombre de interfaz
        oids.append(ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.8.' + str(i)))) # estado

    iterator = getCmd(
        SnmpEngine(),
        CommunityData(dispositivo["comunidad"], mpModel=dispositivo["versionSNMP"]),
        UdpTransportTarget((dispositivo["ip"], dispositivo["puerto"])),
        ContextData(),
        *oids,
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for oid, val in varBinds:
            if val.prettyPrint().startswith('0x'): # si la respuesta es un hexadecimal, esta se decodifica en utf-8
                lista_interfaces.append(bytes.fromhex(val.prettyPrint()[2:]).decode('utf-8'))
            else:
                lista_interfaces.append(val.prettyPrint())

    it = iter(lista_interfaces)
    tabla_interfaces = dict(zip(it, it))
    return tabla_interfaces


def inicializar_json():
    """
    funcion encargada de inicializar el archivo dispositivos.json, el cual contiene la informacion de los dispositivos.
    Dicha información es cargada en diccionario_dispositivos, la cual se utiliza a lo largo del programa.
    Si no existe el archivo se crea uno nuevo y asi, se garantiza la persistencia de datos
    :return:
    """
    global diccionario_dispositivos

    try:
        with open("dispositivos.json", "r") as archivo:
            diccionario_dispositivos = json.load(archivo)

    except IOError:
        print('Archivo dispositivos.json no encontrado, se creara uno nuevo.')
        diccionario_dispositivos = json.loads(JSON_INICIAL)


def guardar_cambios():
    """
    funcion que se encarga de guardar la informacion de diccionario_dispositivos en dispositivos.json, es usada
    cada que se agrega, edita o elimina un dispositivo
    :return:
    """
    with open('dispositivos.json', 'w') as archivo:
        json.dump(diccionario_dispositivos, archivo, indent=4)
    print("dispositivos.json actualizado")


def imprimir_menu():
    print("\nMenu principal:")
    print("1. Agregar dispositivo")
    print("2. Editar información de dispositivo")
    print("3. Eliminar dispositivo")
    print("4. Listar dispositivos existentes")
    print("5. Generar reporte")
    print("6. Salir")


def agregar_dispositivo():
    """
    Funcion encargada de agregar un dispositivo, en donde se especifica la comunidad, version, puerto e ip que conforman
    a un dispositivo.
    :return:
    """
    print("\nAgregar dispositivo")
    comunidad = input("Escribe el nombre de la comunidad del dispositivo: ")
    version = int(input("Digita la version SNMP del dispositivo v1(0), v2c(1): "))
    puerto = int(input("Escribe el puerto del dispositivo: "))
    ip = input("Escribe la direccion ip del dispositivo: ")
    diccionario_dispositivos["dispositivos"].append(
        {'comunidad': comunidad, 'versionSNMP': version, 'ip': ip, 'puerto': puerto})
    guardar_cambios()


def editar_dispositivo():
    """
    funcion que permite al usuario editar la informacion de un dispositivo ya existente
    :return:
    """
    listar_dispositivos()
    dispositivo_elegido = int(input("\nSelecciona el dispositivo a editar: "))

    diccionario_dispositivos["dispositivos"][dispositivo_elegido]["comunidad"] = input(
        "Escribe el nuevo nombre de la comunidad del dispositivo: ")
    diccionario_dispositivos["dispositivos"][dispositivo_elegido]["versionSNMP"] = int(
        input("Digita la version SNMP del dispositivo v1(0), v2c(1): "))
    diccionario_dispositivos["dispositivos"][dispositivo_elegido]["puerto"] = int(
        input("Escribe el puerto del dispositivo: "))
    diccionario_dispositivos["dispositivos"][dispositivo_elegido]["ip"] = input(
        "Escribe la nueva direccion ip del dispositivo: ")

    guardar_cambios()


def eliminar_dispositivo():
    """
    funcion que permite al usuario eliminar la información y reporte de un dispositivo dado.
    Se borran los datos del dispositivo del archivo dispositivos.json y si existe un reporte generado de dicho
    dispositivo tambien se elimina del disco.
    :return:
    """
    listar_dispositivos()
    dispositivo_elegido = int(input("\nSelecciona el dispositivo a eliminar: "))

    print("Dispositivo seleccionado:")
    dispositivo_a_borrar = diccionario_dispositivos["dispositivos"][dispositivo_elegido]
    print(dispositivo_a_borrar)
    str_borrar = input("\nEstas seguro que quieres eliminar el sigiente dispositivo? s/n: ")

    if str_borrar == "s":
        if os.path.exists("reporte_"+dispositivo_a_borrar["ip"]+"_"+dispositivo_a_borrar["comunidad"]+".pdf"):
            os.remove("reporte_"+dispositivo_a_borrar["ip"]+"_"+dispositivo_a_borrar["comunidad"]+".pdf")
            print("reporte_"+dispositivo_a_borrar["ip"]+"_"+dispositivo_a_borrar["comunidad"]+".pdf eliminado")

        del diccionario_dispositivos["dispositivos"][dispositivo_elegido]

        print("Dispositivo eliminado correctamente")
        guardar_cambios()
    else:
        print("No se ha eliminado el dispositivo seleccionado")


def listar_dispositivos():
    """
    imprime todos los dispositivos guardados por el usuario
    :return:
    """
    print("\nDispositivos disponibles: ")
    for dispositivo, i in enumerate(diccionario_dispositivos["dispositivos"]):
        print(dispositivo, i)


def generar_pdf():
    """
    Genera un archivo pdf el cual contiene el reporte detallado de un dispositivo elegido por el usuario.
    El reporte del dispositivo contiene: sistema operativo (version y logo), nombre del dispositivo, información de
    contacto, ubicacion, numero de interfaces y el estado administrativo de cada interfaz. Toda esta informacion se
    obtiene a través de las consultas snmp get hechas en las funciones snmpget() y obtener_informacion_interfaces()
    :return:
    """

    # parte donde el usuario elige el dispositivo
    listar_dispositivos()
    dispositivo_elegido = int(input("Selecciona el dispositivo del cual se genere el reporte: "))

    print(diccionario_dispositivos["dispositivos"][dispositivo_elegido])
    dispositivo = diccionario_dispositivos["dispositivos"][dispositivo_elegido]

    # obtenemos la informacion del dispositivo del cual se generará el reporte
    datos_dispositivo = snmpget(dispositivo)

    numero_interfaces = int(datos_dispositivo[4][1]) if int(datos_dispositivo[4][1]) <= 5 else 5
    tabla_interfaces = obtener_informacion_interfaces(dispositivo, numero_interfaces)

    print("Creando reporte del dispositivo (reporte_"+dispositivo["ip"]+"_"+dispositivo["comunidad"]+".pdf)")

    pdf = FPDF()
    pdf.add_page()

    # parte de encabezado (Datos personales)
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 10, txt="Administración de Servicios en Red",
             ln=1, align='C')
    pdf.set_font("Arial", 'I', size=20)
    pdf.cell(200, 10, txt="Practica 1 - Adquisición de información",
             ln=2, align='C')
    pdf.set_font("Arial", 'B', size=20)
    pdf.cell(200, 10, txt="Caleb Salomón Bolaños Ramos - 4CM13 - 2020630043",
             ln=2, align='C')

    i = 0
    # se imprimen las respuestas de las consultas las cuales contienen la informacion del dispositivo
    for contenido in datos_dispositivo:
        pdf.set_font("Arial", 'B', size=12)
        pdf.multi_cell(200, 10, txt=informacion_reporte[i], align='L')

        pdf.set_font("Arial", size=12)
        contenido_texto = ' = '.join([x.prettyPrint() for x in contenido])

        if i == 0:  # para la parte del sistema operativo se imprime su respectivo logo
            pdf.multi_cell(150, 7, txt=contenido_texto, align='L')
            pdf.image(obtener_imagen_os(contenido_texto), x=170, y=40, w=25, h=25, type='PNG')
        else:
            pdf.multi_cell(200, 7, txt=contenido_texto, align='L')

        pdf.multi_cell(200, 5, txt='', align='L')
        i = i+1

    # parte de estado administrativo de interfaces
    pdf.set_font("Arial", 'B', size=12)
    pdf.multi_cell(200, 10, txt=informacion_reporte[5], align='L')

    pdf.set_font("Arial", size=12)
    for interfaz, estado in tabla_interfaces.items():
        pdf.multi_cell(190, 7, txt="-" + interfaz + ": " + estado_interfaz.get(estado, "Desconocido") + " (" + estado + ")", align='L')

    #se genera el pdf utilizando como nombre la ip y comunidad del dispositivo
    pdf.output("reporte_"+dispositivo["ip"]+"_"+dispositivo["comunidad"]+".pdf")
    print("reporte_"+dispositivo["ip"]+"_"+dispositivo["comunidad"]+".pdf creado correctamente")


def obtener_imagen_os(string):
    """
    obtiene la imagen del sistema operativo dado un string con la informacion del so
    :param string: contiene la informacion del so
    :return: un string con la url del so
    """
    if string is None:
        return ""

    if "Ubuntu" in string:
        return "https://cdn-icons-png.flaticon.com/512/888/888879.png"
    elif "Linux" in string:
        return "https://www.redhat.com/cms/managed-files/tux-327x360.png"
    elif "Windows" in string:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Windows_logo_-_2012.png/800px-Windows_logo_-_2012.png"
    else:
        return ""


inicializar_json()
print("Practica 1 - Adquisición de información")
print("Caleb Salomón Bolaños Ramos - 4CM13 - 2020630043")

while True:
    imprimir_menu()
    opcion = ''
    try:
        opcion = int(input('\nIngresa una opción: '))
    except:
        print('Ingresa un número')

    if opcion == 1:
        agregar_dispositivo()
    elif opcion == 2:
        editar_dispositivo()
    elif opcion == 3:
        eliminar_dispositivo()
    elif opcion == 4:
        listar_dispositivos()
    elif opcion == 5:
        generar_pdf()
    elif opcion == 6:
        print('Adios! :)')
        exit()
    else:
        print('Opcion invalida. Introduce un número del 1 al 6.')
