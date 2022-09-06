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
import json

SNMP_V1 = 0
SNMP_V2 = 1


def imprimir_get(comunidad, version_snmp, ip, puerto):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(comunidad, mpModel=version_snmp),
        UdpTransportTarget((ip, puerto)),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.2.0')),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.4.0')),
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


print('Prueba :0')
imprimir_get('comunidadASRWin', SNMP_V1, '192.168.72.199', 161)
print('Linux')
imprimir_get('comunidadASR', SNMP_V2, 'localhost', 161)

prueba_json = {
    "comunidad": "comunidadASRWin",
    "versionSNMP": 0,
    "ip": "192.168.72.199",
    "puerto": 161
}

prueba_json["versionSNMP"] = SNMP_V2

print(prueba_json)
print(prueba_json['puerto'])