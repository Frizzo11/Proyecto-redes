# Proyecto-redes
## Funcionamiento
### Antes de ejecutar
- Editar ips.txt con las ips a recorrer
- Si es necesario cambiar las credenciales para acceder inicialmente editar los siguientes campos (dejar los dos "username" iguales, lo mismo con los dos "password"): ssh_username, ssh_password, telnet_username, telnet_password
- Tener en la terminal donde se ejecuta el script la última version de python y las siguientes librerias instaladas:
  - import paramiko
  - import telnetlib (pip install telnetlib-313-and-up pq no esta disponible de forma nativa en python)
  - import time
  - import random
  - import string
### Mientras se ejecuta
No cambiar los txt y esperar que se termine de ejecutar para revisarlos, suele tardar un rato en terminar y es normal que tarde bastante si hay muchas ips en la lista
## Archivos
### config_con_recorrido.py
Es el archivo que hace el recorrido principal y el que se tiene que ejecutar
### contraseñanueva.txt
Al terminar de correr el script guarda las contraseñas nuevas y en que IP fueron cambiadas
### ips.txt
Listado de las IP a recorrer, debe ser editado antes de correr el script
### log_conexiones.txt
Al terminar de correr el script guarda en este txt todos lo que esta en pantalla
### config_2.py
Ignorar, archivo con version vieja del script
