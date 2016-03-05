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
	else:
		print "\nIngrese todos los datos correspodientes al nuevo usuario."
		print "\nDirectorio del usuario:",
		dir_hogar = raw_input()
		print "\nDirectorio del esquelto:",
		dir_esqueleto = raw_input()
		print "\n¿Quiere que su usuario tenga permiso del shell? (s/n)",
		perm_shell = raw_input()
		print "Comentario del usuario:",
		comentario = raw_input()
		print "\nNombre de grupo del usuario:",
		nombre = raw_input()
		print "\nNombre del usuario (nickname):",
		usuario = raw_input()

		# no estoy seguro
		# print "\nContraseña del usuario:",
		# password = raw_input()

		

else:
	print "\nPor favor ejecute este script en modo súper usuario (sudo)."
	exit()