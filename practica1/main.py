"""
SNMPv1
++++++

Send SNMP GET request using the following options:

  * with SNMPv1, community 'comunidadASR'
  * over IPv4/UDP
  * to an Agent at localhost
  * for two instances of SNMPv2-MIB::sysDescr.0 MIB object,

Functionally similar to:

| $ snmpget -v1 -c comunidadASR localhost 1.3.6.1.2.1.1.1.0

linux: comunidadASR, localhost

windows: comunidadASRWin
ip casa: 192.168.1.87
ip asignada por celular: '192.168.72.199'

"""  #
from pysnmp.hlapi import *
from fpdf import FPDF
import json

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

diccionario_dispositivos = {}


# imprimir_get('comunidadASRWin', SNMP_V1, '192.168.72.199', 161)
# imprimir_get('comunidadASR', SNMP_V2, 'localhost', 161)


def snmpget(dispositivo):
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
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))
        return varBinds


def obtener_informacion_interfaces(dispositivo, numero_interfaces):
    lista_interfaces = []
    oids = []
    for i in range(1, numero_interfaces+1):
        oids.append(ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.2.' + str(i)))) #nombre de interfaz
        oids.append(ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.8.' + str(i)))) #estado

    iterator = getCmd(
        SnmpEngine(),#numero_interfaces
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
            if val.prettyPrint().startswith('0x'):
                lista_interfaces.append(bytes.fromhex(val.prettyPrint()[2:]).decode('utf-8'))
            else:
                lista_interfaces.append(val.prettyPrint())

    it = iter(lista_interfaces)
    tabla_interfaces = dict(zip(it, it))
    return tabla_interfaces


def inicializar():
    global diccionario_dispositivos

    try:
        with open("dispositivos.json", "r") as archivo:
            diccionario_dispositivos = json.load(archivo)

    except IOError:
        print('Archivo dispositivos.json no encontrado, se creara uno nuevo.')
        diccionario_dispositivos = json.loads(JSON_INICIAL)


def guardar_cambios():
    with open('dispositivos.json', 'w') as archivo:
        json.dump(diccionario_dispositivos, archivo, indent=4)
    print("Información actualizada")


def imprimir_menu():
    print("\nMenu principal:")
    print("1. Agregar dispositivo")
    print("2. Editar información de dispositivo")
    print("3. Eliminar dispositivo")
    print("4. Listar dispositivos existentes")
    print("5. Generar reporte")
    print("6. Salir")


def agregar_dispositivo():
    print("Agregar dispositivo")
    comunidad = input("Escribe el nombre de la comunidad del dispositivo: ")
    version = int(input("Digita la version SNMP del dispositivo v1(0), v2c(1): "))
    puerto = int(input("Escribe el puerto del dispositivo: "))
    ip = input("Escribe la direccion ip del dispositivo: ")
    diccionario_dispositivos["dispositivos"].append(
        {'comunidad': comunidad, 'versionSNMP': version, 'ip': ip, 'puerto': puerto})
    guardar_cambios()


def editar_dispositivo():
    listar_dispositivos()
    dispositivo_elegido = int(input("Selecciona el dispositivo a editar: "))

    diccionario_dispositivos["dispositivos"][dispositivo_elegido]["comunidad"] = input(
        "Escribe el nuevo nombre de la comunidad del dispositivo: ")
    diccionario_dispositivos["dispositivos"][dispositivo_elegido]["versionSNMP"] = int(
        input("Digita la version SNMP del dispositivo v1(0), v2c(1): "))
    diccionario_dispositivos["dispositivos"][dispositivo_elegido]["ip"] = int(
        input("Escribe el puerto del dispositivo: "))
    diccionario_dispositivos["dispositivos"][dispositivo_elegido]["puerto"] = input(
        "Escribe la nueva direccion ip del dispositivo: ")

    guardar_cambios()


def eliminar_dispositivo():
    listar_dispositivos()
    dispositivo_elegido = int(input("Selecciona el dispositivo a eliminar: "))

    print(diccionario_dispositivos["dispositivos"][dispositivo_elegido])
    str_borrar = input("Estas seguro que quieres eliminar el sigiente dispositivo? s/n")

    if str_borrar == "s":
        del diccionario_dispositivos["dispositivos"][dispositivo_elegido]
        print("dispositivo eliminado")
        guardar_cambios()
    else:
        print("No se ha eliminado el dispositivo")


def listar_dispositivos():
    for dispositivo, i in enumerate(diccionario_dispositivos["dispositivos"]):
        print(dispositivo, i)


def generar_pdf():
    # obtenemos la informacion del dispositivo del cual se generará el reporte
    listar_dispositivos()
    dispositivo_elegido = int(input("Selecciona el dispositivo del cual se genere el reporte: "))

    print(diccionario_dispositivos["dispositivos"][dispositivo_elegido])
    dispositivo = diccionario_dispositivos["dispositivos"][dispositivo_elegido]

    datos_dispositivo = snmpget(dispositivo)

    numero_interfaces = int(datos_dispositivo[4][1]) if int(datos_dispositivo[4][1]) <= 5 else 5
    tabla_interfaces = obtener_informacion_interfaces(dispositivo, numero_interfaces)

    pdf = FPDF()

    # añadir una pagina
    pdf.add_page()

    # encabezado (Datos personales)
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
    for contenido in datos_dispositivo:
        pdf.set_font("Arial", 'B', size=12)
        pdf.multi_cell(200, 10, txt=informacion_reporte[i], align='L')

        pdf.set_font("Arial", size=12)
        contenido_texto = ' = '.join([x.prettyPrint() for x in contenido])

        if i == 0:
            pdf.multi_cell(150, 7, txt=contenido_texto, align='L')
            pdf.image(obtener_imagen_os(contenido_texto), x=170, y=40, w=25, h=25, type='PNG')
        else:
            pdf.multi_cell(200, 7, txt=contenido_texto, align='L')

        pdf.multi_cell(200, 5, txt='', align='L')
        i = i+1

    # estado administrativo de interfaces (tabla)
    pdf.set_font("Arial", 'B', size=12)
    pdf.multi_cell(200, 10, txt=informacion_reporte[5], align='L')
    print(tabla_interfaces)

    pdf.set_font("Arial", size=12)
    for interfaz, estado in tabla_interfaces.items():
        print(interfaz, estado)
        pdf.multi_cell(190, 7, txt="-" + interfaz + ": " + estado_interfaz.get(estado, "Desconocido") + " (" + estado + ")", align='L')

    pdf.output("reporte_"+dispositivo["ip"]+"_"+dispositivo["comunidad"]+".pdf")


def obtener_imagen_os(string):
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


inicializar()
print("Practica 1 - Adquisición de información")
print("Caleb Salomón Bolaños Ramos - 4CM13 - 2020630043\n")

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
        print("Todos los dispositivos disponibles:")
        listar_dispositivos()
    elif opcion == 5:
        generar_pdf()
    elif opcion == 6:
        print('Adios! :)')
        exit()
    else:
        print('Opcion invalida. Introduce un número del 1 al 6.')
