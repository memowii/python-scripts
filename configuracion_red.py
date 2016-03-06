# -*- coding: utf-8 -*-

from os import system

system('clear')

print "\nSe iniciara la configuración de la red."
print "Antes de realizar los siguientes pasos usted debe estar seguro que los"
print "controladores de su tarjeta de red ya estén bien instalados y"
print "funcionando, también se debe estar ya conectado a la red cableada."
print "Por último debe encontrarse en modo root."

print "\n¿Quiere realizar una configuración dinámica o estática? (d/e)"
respuesta = raw_input()
if respuesta == 'e':
	print "\nHa elegido realizar la configuración estática, por favor ingrese"
	print "todos los datos que se le pidan."
	print "\nIngrese el nombre de la interfaz:",
	interfaz = raw_input()
	print "\nIngrese la ip del dispositivo:",
	ip = raw_input()
	print "\nIngrese la máscara de red:",
	mascara = raw_input()
	print "\nIngrese el broadcast:",
	broadcast = raw_input()
	setencia_cli = "ifconfig "+interfaz+" "+ip+" netmask "+mascara+" broadcast "+broadcast+" up"
	system(setencia_cli)
	print "\nAhora se creara la tabla de enrutamiento.\n"
	system('route')
	print "\nLa configuración estática ha sido terminada."
else:
	print "\nHa elegido realizar la configuración dinámica."
	print "\nIntroduzca el nombre de la intefaz que quiere configurar:",
	interfaz = raw_input()
	print "\nSe llamará a un comando externo de Linux para que realize la"
	print "configuración."
	setencia_cli = "dhclient -v "+interfaz
	print "La configuración dinámica ha sido terminada."