import serial
import time

BAUDRATE = 115200
PORT = 'COM3'


def zerocrossed_up(prev, curr):
    return (prev < 100) and (curr > 200)


def zerocrossed_down(prev, curr):
    return (prev > 200) and (curr < 100)


def zero_crossed(prev, curr):
    return zerocrossed_up(prev, curr) or zerocrossed_down(prev, curr)


def port_open():
    fd = serial.Serial(PORT, baudrate=BAUDRATE)
    return fd


def start_ap(fd):
    cmd = '\xff\x07\x03'
    fd.write(cmd)
    print 'Access point start command given: response follows'
    for i in range(3):
        print hex(ord(fd.read()))


def stop_ap(fd):
    cmd = '\xff\x07\x03\xff\x09\x03'
    fd.write(cmd)
    print 'Access point stop command given: response follows'
    for i in range(3):
        print hex(ord(fd.read()))


def get_acc_data(fd):
    cmd = '\xff\x08\x07\x00\x00\x00\x00'
    r = fd.write(cmd)
    r = fd.read(7)
    if (ord(r[3]) == 1): return [ord(x) for x in r[4:7]]
    return []


def main():
    fd = port_open()
    start_ap(fd)
    while True:
        r = get_acc_data(fd)
        if r: print r


if __name__ == '__main__':
    main()

