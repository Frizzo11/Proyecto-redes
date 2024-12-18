import paramiko
import telnetlib
import time
import random
import string

# Configuración de conexión
ssh_host = "10.80.255.14"
ssh_port = 22
ssh_username = "admin"
ssh_password = "mrsi94zqtd@"

telnet_host = "10.80.255.14"
telnet_port = 23
telnet_username = "admin"
telnet_password = "mrsi94zqtd@"

# Comando global
command = "display current-configuration"

# Generar contraseña aleatoria
def generar_contraseña(longitud=12):
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(caracteres) for _ in range(longitud))

# Log de operaciones
log = []

def esperar_y_enviar(channel, prompts, response, delay=1):
    """
    Espera dinámicamente ciertos prompts y responde.
    """
    output = ""
    while True:
        if channel.recv_ready():
            time.sleep(delay)
            chunk = channel.recv(1024).decode()
            output += chunk
            log.append(chunk)
            for prompt in prompts:
                if prompt in chunk:
                    channel.send(response + "\n")
                    time.sleep(delay)
                    log.append(f"Enviado: {response}")
                    return output
        else:
            break
    return output

def conectar_ssh():
    try:
        log.append("Intentando conectar por SSH...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_host, ssh_port, ssh_username, ssh_password, look_for_keys=False, allow_agent=False)
        channel = ssh.invoke_shell()
        time.sleep(2)
        output = channel.recv(65535).decode()
        log.append("Conexión SSH establecida.")

        # Cartel de contraseña débil
        if "Change now? [Y/N]:" in output:
            channel.send("N\n")
            time.sleep(1)
            log.append("Cambio de contraseña rechazado.")

        # Configuración básica
        channel.send("screen-length 0 temporary\n")
        time.sleep(1)
        channel.send("system-view\n")
        time.sleep(1)

        # Generar y configurar nueva contraseña
        nueva_contraseña = generar_contraseña()
        with open("contraseñanueva.txt", "w") as file:
            file.write(nueva_contraseña)
        log.append(f"Nueva contraseña generada: {nueva_contraseña}")

        prompts = ["Re-enter password:", "Are you sure? [Y/N]:", "Please enter old password:"]
        channel.send("aaa\n")
        channel.send("local-user admin password irreversible-cipher {nueva_contraseña}\n")
        esperar_y_enviar(channel, prompts, ssh_password) #parece q solo pide old password

        # Finalizar configuración
        channel.send("quit\n")
        time.sleep(1)
        channel.close()
        ssh.close()
        return True, nueva_contraseña

    except Exception as e:
        log.append(f"Error en conexión SSH: {e}")
        return False, None

def conectar_telnet():
    try:
        log.append("Intentando conectar por Telnet...")
        tn = telnetlib.Telnet(telnet_host, telnet_port, timeout=10)
        tn.read_until(b"Username:")
        tn.write(telnet_username.encode("ascii") + b"\n")
        tn.read_until(b"Password:")
        tn.write(telnet_password.encode("ascii") + b"\n")
        time.sleep(2)
        log.append("Conexión Telnet establecida.")

        # Configurar SSH
        tn.write(b"system-view\n")
        time.sleep(1)
        tn.write(b"stelnet server enable\n")
        time.sleep(1)
        tn.write(b"quit\n")
        time.sleep(1)
        log.append("SSH habilitado desde Telnet.")
        tn.close()
        return True

    except Exception as e:
        log.append(f"Error en conexión Telnet: {e}")
        return False

# Flujo principal
exito_ssh, contraseña_generada = conectar_ssh()
if not exito_ssh:
    if conectar_telnet():
        exito_ssh, contraseña_generada = conectar_ssh()

log.append(f"Contraseña generada: {contraseña_generada}" if contraseña_generada else "No se pudo generar una contraseña.")

with open("log_conexiones.txt", "w") as f:
    f.write("\n".join(log))

print("Script finalizado. Detalles guardados en 'log_conexiones.txt'.")
