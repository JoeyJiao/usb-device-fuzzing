import sys
import usb.core

arg = sys.argv[1].split(':')
device = usb.core.find(idVendor=int(arg[0],16), idProduct=int(arg[1],16))

try:
    res = device.ctrl_transfer(int(sys.argv[2],16), int(sys.argv[3],16), int(sys.argv[4],16), int(sys.argv[5],16), int(sys.argv[6]))
    print(res)
except usb.core.USBError as e:
    print(e.backend_error_code)
