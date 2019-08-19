import time
import sys
import usb.core

from common import *

arg = sys.argv[1].split(':')
device = usb.core.find(idVendor=int(arg[0],16), idProduct=int(arg[1],16))

logfile = sys.argv[2]

fp = open(logfile, 'r')
lines = fp.readlines()
fp.close()

for line in lines:
    if not line.startswith('IN') and not line.startswith('OUT'):
        continue
#    if 'err' in line:
#        continue
    line = line.replace('\t', ' ').replace('  ', ' ')
    params = line.split(' ')
    if params[0] == 'IN':
        bRequestType = 0x80 | int(params[1],16)
    else:
        bRequestType = 0x80 & int(params[1],16)
    try:
        res = device.ctrl_transfer(bRequestType, int(params[2], 16), int(params[3],16), int(params[4],16), int(params[6].replace('len(','').replace(')', '').replace(':', '')), timeout=250)
        print(line, res)
    except usb.core.USBError as e:
        print(e.backend_error_code)

    if not is_alive(device):
        device.reset()
        time.sleep(1)
