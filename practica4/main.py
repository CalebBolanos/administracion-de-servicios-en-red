import os
import telnetlib
from ftplib import FTP

def menu_s():
    print('Practica 4 - Modulo de Administracion de configuracion')
    print('Bolaños Ramos Caleb salomón')
    print('2020630043')
    print('Menú principal:')
    print('1. Generar archivo startup-config')
    print('2. Extraer archivo startup-config')
    print('3. Importar archivo startup-config')
    print('4. Salir')
    opcion = input('Elige una opción: ')
    opcion = int(opcion)

    usuario = "rcp"
    psw = "rcp"

    if opcion == 1:
        print('Generar archivo startup-config')
        ipe = input("Escribe la ip del router al cual se va a conectar: ")

        tel = telnetlib.Telnet(ipe)  # Se habilita el servicio telnet
        tel.read_until(b"User: ")
        tel.write(usuario.encode('ascii') + b"\n")
        tel.read_until(b"Password: ")
        tel.write(psw.encode('ascii') + b"\n")

        nombre = input("Escriba el nombre que le pondra al dispositivo: ")

        tel.write(b"enable\n")
        tel.write(b"config\n")
        tel.write(b"hostname " + nombre.encode('ascii') + b"\n")
        tel.write(b"copy running-config startup-config\n")
        tel.write(b"exit\n")
        tel.write(b"exit\n")
        print(tel.read_all().decode('ascii'))

        print('startup-config de {} ({}) creado correctamente'.format(nombre, ipe))
        input('Pulse una tecla para continuar... ')
        menu_s()

    elif opcion == 2:
        print('Extraer archivo startup-config')

        ipftp = input("Escribe la ip del router al cual se va a conectar:  ")
        ftp = FTP(ipftp, usuario, psw)
        print("\n"+ftp.getwelcome())
        print(ftp.retrbinary('RETR startup-config', open('startup-config', 'wb').write))
        print("\n")
        ftp.close()
        print('Archivo startup-config de {}  extraido'.format(ipftp))
        print('Se puede encontrar dentro de la carpeta del proyecto')
        input('Pulse una tecla para continuar... ')
        menu_s()

    elif opcion == 3:
        print('Importar archivo startup-config')

        ipftp = input("Escribe la ip del router al cual se va a conectar:   ")
        ftp = FTP(ipftp, usuario, psw)
        print("\n" + ftp.getwelcome())

        origen = '/home/caleb/Documentos/GitHub/administracion-de-servicios-en-red/practica4/startup-config'
        ftpraiz = '/'

        f = open(origen, 'rb')
        ftp.cwd(ftpraiz)
        ftp.storbinary('STOR startup-config', f)
        f.close()
        ftp.quit()

        print('Archivo startup-config de {} importado'.format(ipftp))
        input('Pulse una tecla para continuar... ')
        menu_s()
    elif opcion == 4:
        exit()
    else:
        print('Escribe una opcion dentro del menu')
        input('Pulse alguna tecla para continuar...')
        os.system("clear")
        menu_s()
    os.system("clear")

menu_s()