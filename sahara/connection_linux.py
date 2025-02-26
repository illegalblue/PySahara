import usb.core
import usb.util
import time


class USBDevice:
    def __init__(self, vid, pid):
        self.vid = vid
        self.pid = pid
        self.device = None
        self.endpoint_out = None
        self.endpoint_in = None

    def wait_for_device(self, timeout=10):
        """Wait for the device to appear, with a timeout."""
        print("[*] Waiting for EDL device...")
        elapsed = 0
        while elapsed < timeout:
            self.device = usb.core.find(idVendor=self.vid, idProduct=self.pid)
            if self.device:
                print("[+] Device detected!")
                return True
            time.sleep(1)
            elapsed += 1
            print(f"[-] Still waiting... ({elapsed}s)")
        print("[!] Device not found within timeout.")
        return False

    def find_device(self):
        """Find and configure the USB device."""
        if not self.device:
            return False

        try:
            if self.device.is_kernel_driver_active(0):
                self.device.detach_kernel_driver(0)
        except (NotImplementedError, usb.core.USBError):
            pass

        self.device.set_configuration()
        cfg = self.device.get_active_configuration()
        intf = cfg[(0, 0)]

        self.endpoint_out = usb.util.find_descriptor(intf,
                                                     custom_match=lambda e: usb.util.endpoint_direction(
                                                         e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        self.endpoint_in = usb.util.find_descriptor(intf,
                                                    custom_match=lambda e: usb.util.endpoint_direction(
                                                        e.bEndpointAddress) == usb.util.ENDPOINT_IN)

        return self.device if self.endpoint_out and self.endpoint_in else None

    def get_device(self):
        """Return the configured USB device."""
        return self.device
