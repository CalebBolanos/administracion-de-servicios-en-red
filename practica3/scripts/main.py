from TrendUpdate import actualizarDatos
from trendGraphDetection import detectarUmbrales
from threading import Thread

print("Practica 3 - Monitorizar el rendimiento de un agente usando SNMP")
print("Caleb Salomón Bolaños Ramos - 4CM13 - 2020630043")


def imprimir_menu():
    print("\nMenu principal:")
    print("1. Iniciar")
    print("2. Salir")


while True:
    imprimir_menu()
    try:
        opcion = int(input('\nIngresa una opción: '))
    except:
        print('Ingresa un número')

    if opcion == 1:
        hilo_actualizar_rrd = Thread(target=actualizarDatos)
        hilo_actualizar_rrd.start()
        detectarUmbrales()
    elif opcion == 5:
        print('Adios! :)')
        exit()
    else:
        print('Opcion invalida. Introduce un número del 1 al 2.')

