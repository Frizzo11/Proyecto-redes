#ver configuraciones de ssh por telnet
import paramiko
import telnetlib #no esta en el nativo de python, hay que instalarlo usando el comando en el notion
import time
import random
import string

# Configuración de conexión
ssh_host = "10.80.255.15"
ssh_port = 22
ssh_username = "admin"
ssh_password = "BmU&qff$6&Zl" # Contraseña actual

telnet_host = "10.80.255.15"
telnet_port = 23
telnet_username = "admin"
telnet_password = "BmU&qff$6&Zl"

# Generar contraseña aleatoria
def generar_contraseña(longitud=12):
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(caracteres) for _ in range(longitud))

# Log de operaciones
log = []


def esperar_y_enviar(channel, prompts, response, delay=1, timeout=30):
    """
    Espera dinámicamente ciertos prompts y responde.
    """
    output = ""
    start_time = time.time()
    while True:
        if channel.recv_ready():
            time.sleep(delay)
            chunk = channel.recv(1024).decode(errors='ignore')
            output += chunk
            log.append(chunk)
            for prompt in prompts:
                if prompt in chunk:
                    channel.send(response + "\n")
                    time.sleep(delay)
                    log.append(f"Enviado: {response}")
                    return output
        else:
            if time.time() - start_time > timeout:
                log.append("Timeout esperando respuesta.")
                break
            time.sleep(1)
    return output

def conectar_ssh(ip):
    try:
        log.append(f"Intentando conectar por SSH a {ip}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, ssh_port, ssh_username, ssh_password, look_for_keys=False, allow_agent=False)
        channel = ssh.invoke_shell()
        time.sleep(2)
        output = channel.recv(65535).decode()
        log.append("Conexión SSH establecida.")

        # cartel de contraseña débil
        if "Change now? [Y/N]:" in output:
            channel.send("N\n")
            time.sleep(1)
            log.append("Cambio de contraseña rechazado.")

        # modo privilegiado
        channel.send("screen-length 0 temporary\n")
        time.sleep(1)
        channel.send("system-view\n")
        time.sleep(1)

        # genero y cambio contraseña
        nueva_contraseña = generar_contraseña()
        with open("contraseñanueva.txt", "w") as file:
            file.write(f"Contraseña: {nueva_contraseña}\n")
            file.write(f"IP: {ip}\n")
        log.append(f"Nueva contraseña generada: {nueva_contraseña}")

        prompts = ["Re-enter password:", "Are you sure? [Y/N]:", "Please enter old password:"]
        channel.send("aaa\n")
        channel.send(f"local-user admin password irreversible-cipher {nueva_contraseña}\n")
        esperar_y_enviar(channel, prompts, ssh_password) #parece q solo pide old password

        # Finalizar configuración
        channel.send("quit\n")
        time.sleep(1)
        channel.close()
        ssh.close()
        return True, nueva_contraseña

    except Exception as e:
        log.append(f"Error en conexión SSH a {ip}: {e}")
        return False, None

def conectar_telnet(ip):
    try:
        log.append(f"Intentando conectar por Telnet a {ip}...")
        tn = telnetlib.Telnet(ip, telnet_port, timeout=10)
        tn.read_until(b"Username:")
        tn.write(telnet_username.encode("ascii") + b"\n")
        tn.read_until(b"Password:")
        tn.write(telnet_password.encode("ascii") + b"\n")
        time.sleep(2)
        log.append("Conexión Telnet establecida.")

        # Configurar SSH
        tn.write(b"system-view\n")
        time.sleep(1)
        tn.write(b"stelnet server enable\n") #verificar si es stelnet o ssh server enable
        time.sleep(1)
        tn.write(b"quit\n")
        time.sleep(1)
        log.append("SSH habilitado desde Telnet.")
        tn.close()
        return True

    except Exception as e:
        log.append(f"Error en conexión Telnet a {ip}: {e}")
        return False

# lee ips desde el archivo ips.txt
def leer_ips(archivo):
    with open("ips.txt", "r") as file:
        return [line.strip() for line in file.readlines()]

# loop principal
ips = leer_ips("ips.txt")
for ip in ips:
    log.append(f"Procesando IP: {ip}")
    exito_ssh, contraseña_generada = conectar_ssh(ip)
    if not exito_ssh:
        if conectar_telnet(ip):
            exito_ssh, contraseña_generada = conectar_ssh(ip)
    log.append(f"Contraseña generada para {ip}: {contraseña_generada}" if contraseña_generada else f"No se pudo generar una contraseña para {ip}.")

with open("log_conexiones.txt", "w") as f:
    f.write("\n".join(log))

print("Script finalizado. Detalles guardados en 'log_conexiones.txt'.")
