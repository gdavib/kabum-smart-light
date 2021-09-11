from os import path, read
import socket
from sys import argv, exit
from os import path
from threading import Thread
from infi.systray import SysTrayIcon
import threading

def desligar(socket):
    print("[-]Desligando...")
    b1 = b"\x28\x6d\xcd\x42\x07\x55\x08\x00\x27\x8d\x68\x4f\x08\x00\x45\x00" \
    b"\x00\x6f\x95\xef\x40\x00\x81\x06\xe2\x34\xc0\xa8\x00\x12\xc0\xa8" \
    b"\x00\x02\xea\x5e\x1a\x0c\x97\xf9\x02\xe2\x00\x00\x23\xeb\x50\x18" \
    b"\x72\x10\xe6\x97\x00\x00\x00\x00\x55\xaa\x00\x00\x00\x04\x00\x00" \
    b"\x00\x0d\x00\x00\x00\x37\x33\x2e\x33\x00\x00\x00\x00\x00\x00\x00" \
    b"\x96\x00\x05\x78\xec\xe6\x64\x6e\x43\xd9\xdd\x48\x5f\xb3\x22\xd2" \
    b"\x1b\xa5\xf1\x18\x47\x52\xe4\x3f\xc4\xff\xb2\x2e\x8f\xeb\x2d\xd8" \
    b"\x7e\x91\xcc\xa3\xb8\x44\x4c\x49\xb3\x00\x00\xaa\x55"
    socket.send(b1)
    socket.close()

def ligar(socket:socket.socket):
    print("[+]Ligando...")
    b1 = b"\x28\x6d\xcd\x42\x07\x55\x08\x00\x27\x8d\x68\x4f\x08\x00\x45\x00" \
    b"\x00\x6f\x96\xec\x40\x00\x81\x06\xe1\x37\xc0\xa8\x00\x12\xc0\xa8" \
    b"\x00\x02\xea\x5e\x1a\x0c\x97\xf9\x0f\x3e\x00\x00\x33\x42\x50\x18" \
    b"\x72\x10\xc9\xb0\x00\x00\x00\x00\x55\xaa\x00\x00\x00\x08\x00\x00" \
    b"\x00\x0d\x00\x00\x00\x37\x33\x2e\x33\x00\x00\x00\x00\x00\x00\x00" \
    b"\x9a\x00\x05\x78\xec\x4f\x97\x2f\x50\xdf\x0f\x23\x64\xed\xfb\xad" \
    b"\xf7\x27\x30\x4d\x19\x20\x51\x73\xf1\x05\x52\x0d\x28\x40\xc0\x79" \
    b"\x86\xfb\xdc\xba\xab\x9c\xe9\xec\x67\x00\x00\xaa\x55"
    socket.send(b1)
    socket.close()

def capturarIp(ip):
    global stop, sip
    r = ""
    ios = ".".join(ip.split(".")[:3])
    for e in range(2, 255):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        t = ios + "." + str(e)
        c = s.connect_ex((t, port))
        if c == 0:
            print("Endereço do Dispositivo: " + t + ":" + str(port))
            comando(s)
            stop = True
            configFile("save", t)
            sip = t
            break
        elif stop == True:
            break

def comando(s:socket.socket, sysAction=None):
    x = None
    try:
        x = argv[1]
    except:
        pass
    finally:
        if sysAction == "on" or x == "on": ligar(s)
        elif sysAction == "off" or x == "off": desligar(s)
        elif not any(j == x for j in ['on', 'off']): print("Use: ./kabum.py " + "[on|off]")

def ipSalvo(ip, sysAction=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    c = s.connect_ex((ip, port))
    if c == 0:
        comando(s, sysAction)
        return True
    else: return False

def configFile(action=None, ip=None):
    if action == "save" and ip != None:
        with open("kbmip.txt", "w") as f:
            f.write(ip)
            f.close()
    else:
        try:
            kabumFile = open('kbmip.txt', 'r').read()
            return kabumFile

        except:
            if FileNotFoundError: open('kbmip.txt', '+w').close()
            return None

def strayOn(systray):
    ipSalvo(sip, "on")

def strayOff(systray):
    ipSalvo(sip, "off")

port = 6668
stop = False
sip = configFile()
ipSalvoResposta = False
if sip != None and len(sip) >= 7:
    ipSalvoResposta = ipSalvo(sip)

if ipSalvoResposta == False:
    interfaces = socket.gethostbyname_ex(socket.gethostname())[-1]  
    for i in interfaces:
        t = threading.Thread(target=capturarIp, args=(i,))
        t.start()

if len(argv) <= 1:
    menu = (("Ligar", None, strayOn), ("Desligar", None, strayOff))
    systray = SysTrayIcon("icon.ico", "Smart Lâmpada", menu)
    systray.start()

