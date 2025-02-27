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
        self.myedldevice = None  # Stores the actual connection object (serial or USB)

    def print_device(self):
        """Print device details based on platform."""
        if platform.system() == "Windows":
            ports = serial.tools.list_ports.comports()
            for port in ports:
                if port.device == self.myedldevice.port:
                    print(f"[+] EDL Device Detected: {self.myedldevice.port}")
                    print("[+] Device Info:")
                    print(f"    - Port         : {port.device or 'Unknown'}")
                    print(f"    - Description  : {port.description or 'Unknown'}")
                    print(f"    - Hardware ID  : {port.hwid or 'Unknown'}")
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
        """Detect and return an active EDL device connection."""
        print(f"[*] Detecting EDL Device on {platform.system()}...")

        if platform.system() == "Windows":
            edl = EDLInterface()
            if edl.wait_for_device():
                conn = edl.open_connection()
                if conn:
                    self.myedldevice = conn  # Store the active serial connection
                    self.print_device()
                    return conn  # Return the connection instead of just the port
        else:
            usb_device = EDLInterface(vid=self.vid, pid=self.pid)
            if usb_device.wait_for_device():
                device = usb_device.find_device()
                self.myedldevice = usb_device.get_device()
                if self.myedldevice:
                    self.print_device()
                    return self.myedldevice  # Return the USB device object

        return None  # No device found
