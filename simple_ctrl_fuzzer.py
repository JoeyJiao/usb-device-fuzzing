#!/usr/bin/env python

import sys
import time
import usb.core
import binascii

from common import *

RETRY_COUNT = 10

def TestCtrlTransfer(device, rt, r, v, i):

    for size in (0, 10, 100, 4000):
        sys.stdout.write('\nTRY %0.2x %0.2x %0.4x %0.4x len(%0.4u)\n' % (rt, r, v, i, size))

        try:
            res = device.ctrl_transfer(rt&0x80, r, v, i, bytearray().fromhex('ff'*size), timeout=250)
            print('OUT %0.2x %0.2x %0.4x %0.4x res(%u) len(%u)' % (rt&0x80, r, v, i, res, size))
        except usb.core.USBError as e:
            if (e.backend_error_code != -9 and e.backend_error_code != -1): # ignore LIBUSB_ERROR_PIPE and LIBUSB_ERROR_IO
                print('OUT %0.2x %0.2x %0.4x %0.4x err(%i) len(%u)' % (rt&0x80, r, v, i, e.backend_error_code, size))
        except Exception as eo:
            if not device:
                raise eo

        try:
            res = device.ctrl_transfer(rt|0x80, r, v, i, size, timeout=250)
            print('IN  %0.2x %0.2x %0.4x %0.4x data(%u) len(%u):\t%s' % (rt|0x80, r, v, i, len(res), size, binascii.hexlify(res)))
        except usb.core.USBError as e:
            if (e.backend_error_code != -9 and e.backend_error_code != -1): # ignore LIBUSB_ERROR_PIPE and LIBUSB_ERROR_IO
                print('IN  %0.2x %0.2x %0.4x %0.4x err(%i) len(%u)' % (rt|0x80, r, v, i, e.backend_error_code, size))
        except Exception as eo:
            if not device:
                raise eo

        count = 0
        while True:
            if count == RETRY_COUNT:
                print("TIMEOUT")
                sys.exit(-7)
            (A, E) = is_alive(device)
            if not A and E == -7:
                count += 1
            else:
                break


arg = sys.argv[1].split(':')
device = usb.core.find(idVendor=int(arg[0],16), idProduct=int(arg[1],16))

initq = initv = initvv = 0
if len(sys.argv) > 2:
    initq = int(sys.argv[2], 16)
if len(sys.argv) > 3:
    initv = int(sys.argv[3], 16)
if len(sys.argv) > 4:
    initvv = int(sys.argv[4], 16)

for q in range(initq, 0x100): # bRequest
    for v in range(initv, 0x10): # wValue.High
        for vv in range(initvv, 0x10): # wValue.Low
            for i in range(0, 0x10): # wIndex.High
                if q==3 and vv==2 and i==0: # avoid SET_FEATURE TEST_MODE
                    continue
                for ii in range(0, 0x10): # wIndex.Low
                    for t in range(0, 0x04): # bmRequestType.Type
                        for r in range(0, 0x04): # bmRequestType.Recipient
                            TestCtrlTransfer(device, (t<<5)|r, q, (v<<8)|vv, (i<<8)|ii)

