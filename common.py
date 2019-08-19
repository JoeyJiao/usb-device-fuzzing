import usb.core

def is_alive(device):

    res = ""
    try:
        res = device.ctrl_transfer(0x80, 0, 0, 0, 2)
    except usb.core.USBError as e:

        if e.backend_error_code == -4: # LIBUSB_ERROR_NO_DEVICE
            print("\nDevice not found!")
            sys.exit()

        if e.backend_error_code == -3: # LIBUSB_ERROR_ACCESS
            print("\nAccess denied to device!")
            sys.exit()

        print("\nGET_STATUS returned error %i" % e.backend_error_code)
        return False

    if len(res) != 2:
        print("\nGET_STATUS returned %u bytes: %s" % (len(res), binascii.hexlify(res)))
        return False

    return True
