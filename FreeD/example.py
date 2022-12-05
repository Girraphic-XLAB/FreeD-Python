from freed import FreeD, FreeDWrapper
import socket
import msvcrt

UDP_IP = "127.0.0.1"
UDP_PORT = 40000


KEYMAPS = """ 
              W
            A S D       Manipulate the pos_x and pos_y directions

            Q   E       Manipulate Roll left and right

           Tab Shift    Manipulate pos_z (up/down) 

           Z    C       Manipulate Yaw (in/out)

           F    G       Manipulate Pitch (up/down)

           +    -       Increase unit scalar multiplier.

           Press Ctrl-C to exit.
"""
KEYS = {b'\x77': 'w', b'\x61': 'a', b'\x73': "s", b'\x64': "d", b'\x71': "q", b'\x65': "e", b"\x09": "TAB", b'\x16': "SHIFT", 
        b'\x7a': "z", b'\x63':"c", b'\x76':"v", 'b\x62': "b", b'\x66': "f", b'\x67':"g", b'\x3d': '+', b'\x2d': '-'}



if __name__ == "__main__":
    print("FreeD Simulator; Girraphic 2022")
    print(KEYMAPS)
    struct = FreeDWrapper(0,0,0,0,0,0,0,0)
    bits: 'bytes' = struct.createFreeD().encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    unit = 1000
    print("Key", "    ", "Scale:", unit, "Packet", bits.hex(':'), end="\r")
    while (True):
        ch = msvcrt.getch()
        if (ch == b'\x03'):
            exit()
        if (ch in KEYS.keys()):

            match KEYS[ch]:
                case 'w':
                    struct.pos_y += 1 * unit
                    bits = struct.createFreeD().encode()
                case 's':
                    struct.pos_y -= 1 * unit
                    bits = struct.createFreeD().encode()
                case 'a':
                    struct.pos_z -= 1 * unit
                    bits = struct.createFreeD().encode()
                case 'd':
                    struct.pos_z += 1 * unit
                    bits = struct.createFreeD().encode()

                case 'q':
                    struct.roll -= 10 * unit 
                    bits = struct.createFreeD().encode()

                case 'e':
                    struct.roll += 10 * unit
                    bits = struct.createFreeD().encode()

                case 'TAB':
                    struct.pos_x += 1*unit
                    bits = struct.createFreeD().encode()

                case 'SHIFT':
                    struct.pos_x -= 1*unit
                    bits = struct.createFreeD().encode()
                case 'f':
                    struct.pitch += 10*unit
                    bits = struct.createFreeD().encode()

                case 'g':
                    struct.pitch -= 10*unit
                    bits = struct.createFreeD().encode()

                case 'z':
                    struct.yaw -= 10*unit
                    bits = struct.createFreeD().encode()

                case 'c':
                    struct.yaw += 10*unit
                    bits = struct.createFreeD().encode()
                case '+':
                    unit += 10
                case '-':
                    unit -= 10

                
            
            print("Key 0x" + str(ch.hex()), "Scale:", unit, "Packet", bits.hex(':'), end="\r")
            sock.sendto(bits, (UDP_IP, UDP_PORT))


    