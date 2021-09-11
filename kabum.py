from os import path, read
import socket
import sys
import json
from os import path


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

def ligar(socket):
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
    
def errmsg():
    print("Por favor, use: " + __file__.split("\\")[-1] + " [on|off]")
    
def getIp(ipTail):
    ipTail = str(ipTail)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    iplocal = ""
    if len(ipTail) > 3:
        iplocal = ipTail
    else:
        iplocal = socket.gethostbyname_ex(hostname)[2][1]
        iplocal = ".".join(iplocal.split(".")[0:3]) + "." + str(ipTail)
    s.settimeout(0.5)
    print(iplocal)
    r = s.connect_ex((iplocal, port))
    if r == 0:
        try:
            if sys.argv[1] == 'on': ligar(s)
            elif sys.argv[1] == 'off': desligar(s)
            else : errmsg()
        except:
                errmsg()
                pass

        return iplocal
    else:
        return False
    
port = 6668
o, i, n = (None,)*3
try:
    o = open('kbmip.txt', 'r')
    i = o.read()
    n = i if getIp(i) else False
except:
    pass

if not n:
    for x in range(2,255):
        n = getIp(x)
        if n != False:
            print("Endereço da Lâmpada: " + n + ":" + str(port))
            with open('kbmip.txt', 'w+') as f:
                f.write(n)
                
            break
