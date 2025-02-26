import platform
import usb.util
import serial.tools.list_ports

if platform.system() == "Windows":
    from sahara.connection_win import SerialEDLDevice as EDLInterface
else:
    from sahara.connection_linux import USBDevice as EDLInterface


class edlDevice:
    def __init__(self, vid, pid):
        self.vid = vid
        self.pid = pid
        self.myedldevice = None

    def print_device(self):
        if platform.system() == "Windows":
            ports = serial.tools.list_ports.comports()
            for port in ports:
                if port.device == self.myedldevice:
                    print(f"[+] EDL Device Detected: {self.myedldevice}")
                    print("[+] Device Info:")
                    print(f"    - Port         : {port.device or 'Unknown'}")
                    print(f"    - Description  : {port.description or 'Unknown'}")
                    print(f"    - Hardware ID  : {port.hwid} or 'Unknown'")
                    print(f"    - Manufacturer : {port.manufacturer or 'Unknown'}")
                    print(f"    - Product      : {port.product or 'Unknown'}")
                    print(f"    - Serial No.   : {port.serial_number or 'Unknown'}")
                    print(f"    - Vendor ID    : {hex(self.vid) or 'Unknown'}")
                    print(f"    - Product ID   : {hex(self.pid) or 'Unknown'}")
        else:
            print("[+] Device Info:")
            print(f"    - Manufacturer : {usb.util.get_string(self.myedldevice, self.myedldevice.iManufacturer) or 'Unknown'}")
            print(f"    - Product      : {usb.util.get_string(self.myedldevice, self.myedldevice.iProduct) or 'Unknown'}")
            print(f"    - Serial No.   : {usb.util.get_string(self.myedldevice, self.myedldevice.iSerialNumber) or 'Unknown'}")
            print(f"    - Vendor ID    : {hex(self.myedldevice.idVendor)}")
            print(f"    - Product ID   : {hex(self.myedldevice.idProduct)}")

    def getelddevice(self):
        print(platform.system())
        if platform.system() == "Windows":
            edl = EDLInterface()
            if edl.wait_for_device():
                if edl.open_connection():
                    self.myedldevice = edl.com_port
                    self.print_device()
                    return self.myedldevice
        else:
            usb_device = EDLInterface(vid=self.vid, pid=self.pid)
            if usb_device.wait_for_device():
                device = usb_device.find_device()
                self.myedldevice = usb_device.get_device()
                if self.myedldevice:
                    self.print_device()
                    return self.myedldevice

        return None
