import time
import usb.core
import usb.util
import logging
from structures.sahara_definitions import SaharaHeader
from structures.sahara_enums import SaharaCommand

logging.basicConfig(level=logging.INFO, format="%(message)s")

class SaharaSerialError(Exception):
    """Custom exception for SaharaSerial errors."""
    def __init__(self, message, code=0):
        super().__init__(message)
        self.code = code

class SaharaSerialInvalidArgument(SaharaSerialError):
    """Exception for invalid arguments."""
    pass

class SaharaSerial:
    def __init__(self, vendor_id, product_id, timeout=1000):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
        self.timeout = timeout

    def wait_for_device(self):
        """Waits for the Qualcomm device in EDL mode."""
        dots = ""
        while True:
            self.device = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)
            if self.device:
                logging.info("\n[✔] Device detected!")
                self.show_device_details()
                return True
            dots = "." if len(dots) > 5 else dots + "."
            print(f"[+] Waiting for device{dots}", end="\r", flush=True)
            time.sleep(1)
        return False

    def show_device_details(self):
        """Displays device details if detected."""
        logging.info(f"Vendor ID      : {hex(self.device.idVendor)}")
        logging.info(f"Product ID     : {hex(self.device.idProduct)}")
        logging.info(f"Manufacturer   : {usb.util.get_string(self.device, self.device.iManufacturer)}")
        logging.info(f"Product        : {usb.util.get_string(self.device, self.device.iProduct)}")
        logging.info(f"Serial Number  : {usb.util.get_string(self.device, self.device.iSerialNumber)}")

    def read_data(self, size=512):
        """Reads raw data from the device."""
        try:
            data = self.device.read(0x81, size, self.timeout)  # Endpoint 0x81 (assumed)
            logging.info(f"[←] Received: {bytes(data).hex()}")
            return bytes(data)
        except usb.core.USBError as e:
            logging.error(f"USB Read Error: {e}")
            return None

    def write_data(self, data):
        """Writes raw data to the device."""
        if not isinstance(data, bytes):
            raise SaharaSerialInvalidArgument("Data must be of type bytes")

        try:
            self.device.write(1, data, self.timeout)  # Endpoint 0x01 (assumed)
            logging.info(f"[→] Sent: {data.hex()}")
        except usb.core.USBError as e:
            logging.error(f"USB Write Error: {e}")

    def reset_device(self):
        """Sends a reset command to the device if needed."""
        logging.warning("Resetting device...")
        reset_header = SaharaHeader(command=SaharaCommand.RESET, length=8)
        reset_packet = reset_header.to_bytes()
        self.write_data(reset_packet)

        response = self.read_data()
        if response and response[:4] == bytes([SaharaCommand.RESET, 0, 0, 0]):
            logging.info("[✔] Device successfully reset.")
        else:
            logging.error("Reset failed or no response.")

