# Proyecto-redes
### Comandos:

HABILITAR MODO CON PRIVILEGIOS HUAWEI PARA CONFIGURAR:
system-view

CAMBIAR CONTRASEÑA ADMIN HUAWEI:
local-user admin password irreversible-cipher CONTRASEÑA (esto va despues del aaa, osea q seria system-view y despues aaa)

CONFIG PARA HABILITAR SSH:

local-user admin service-type ssh (habilita usuario admin para ingreso por ssh)
stelnet server enable (habilita server ssh)
ssh user admin (crea usuario admin para ssh)
ssh user admin authentication-type password (método de autenticación por contraseña)
ssh user admin service-type all

user-interface vty 0 4
authentication-mode aaa
user privilege level 15
protocol inbound all

ANULAR SERVER TELNET

undo telnet server enable

CAMBIAR CLAVE DE ACCESO AL SWITCH LOCAL POR CABLE CONSOLA:

user-interface con 0
authentication-mode password
set authentication password cipher CLAVE

Comandos para probar

display current-configuration #Es una especio de ifconfig

### Credenciales:

usuario: admin
contraseña: hospitales.axzs*7 (si no funciona esa probar con, q suele ser la q funciona en los swtiches de bolivar mrsi94zqtd@)