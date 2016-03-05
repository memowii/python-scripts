# -*- coding: utf-8 -*-

from sys import exit
from os import system

system('clear')

print "Este script de python creará un usuario para usted."
print "Por favor considere que debe estar en modo súper usuario (sudo)."
print "\n¿Se encuentra en modo súper usuario? (s/n)"
respuesta = raw_input()
if respuesta == 's':
	print "\n¿Quiere crear un nuevo grupo para el nuevo usuario? (s/n)"
	respuesta = raw_input()
	if respuesta == 's':
		print "\nIntroduzca el nombre del nuevo grupo:",
		nombre_grupo = raw_input()
		sentencia_cli = 'groupadd'+' '+nombre_grupo
		system(sentencia_cli)
		print "\nEl nuevo grupo para su usuario ha sido creado."
	print "\nIngrese todos los datos correspodientes al nuevo usuario."
	print "\nDirectorio del usuario:",
	dir_hogar = raw_input()
	print "\nDirectorio del esqueleto:",
	dir_esqueleto = raw_input()
	print "\n¿Quiere que su usuario tenga permiso del shell? (s/n)",
	perm_shell = raw_input()
	if perm_shell == "s":
		dir_shell = "/bin/bash"
	else:
		dir_shell = "/bin/false"
	print "\nComentario del usuario:",
	comentario = raw_input()
	print "\nNombre de grupo del usuario:",
	nombre_grupo = raw_input()
	print "\nNombre del usuario (nickname):",
	usuario = raw_input()

	sentencia_cli = "useradd -d "+dir_hogar+" -m -k "+dir_esqueleto+" -s "+dir_shell+" -c "+"'"+comentario+"'"+" -g "+nombre_grupo+" "+usuario
	system(sentencia_cli)
	print "\nEl usuario ha sido creado, ahora debe ponerle una contraseña, vamos a 'testear' su contraseña."
	print "La contraseña debe tener 5 carácteres al menos, una letra mayúscula y un número."
	password = raw_input('\nIngrese contraseña: ')
	while True:
		if len(password) < 5:
			print "\nLa contraseña es muy corta, esta debe contener al menos 5 carácteres."
		elif not any(char.isupper() for char in password):
			print "\nLa contraseña debe tener al menos una letra mayúscula."
		elif not any(char.isdigit() for char in password):
			print "\nLa contraseña debe tener al menos un número."
		else:
			break
		password = raw_input('\nIngrese contraseña: ')
	print "\nLa contraseña introducida cumple con nuestros estándares."
	print "Ahora la asignaremos al nuevo usuario. Llamaremos a un comando externo"
	print "de linux para que usted vuelva a ingresar la contraseña que acaba"
	print "de crear.\n"
	sentencia_cli = 'passwd'+' '+usuario
	system(sentencia_cli)
	print "\nEl usuario ha sido creado."
	print "\n¿Desea crear una cuota para el usuario creado? (s/n)"
	respuesta = raw_input()
	if respuesta == 's':
		print "\nIngrese la cantidad del soft (en bytes):",
		soft = raw_input()
		print "\nIngrese la cantidad del hard (en bytes):",
		hard = raw_input()
		sentencia_cli = "setquota -u "+usuario+" "+soft+" "+hard+" 10000 10000  -a /dev/loop0"
		system(sentencia_cli)
		print "\nLa cuota del usuario "+usuario+" fue creada."
else:
	print "\nPor favor ejecute este script en modo súper usuario (sudo)."
	exit()