import serial

class DeviceIO:
    def __init__(self, edldevice, baudrate=115200):
        """Initialize the device IO for reading and writing."""
        self.edldevice = edldevice
        self.baudrate = baudrate
        self.conn = None

        # Determine if it's a serial connection
        if isinstance(edldevice, serial.Serial):  # Proper serial detection
            self.conn = edldevice
            print(f"[+] Using Serial Port: {self.conn.port}")
        else:
            # Assuming it's a USB device (Linux)
            self.conn = edldevice
            print("[+] Using USB Device")

    def is_connected(self):
        """Check if the connection is valid and open."""
        if self.conn is None:
            return False
        if isinstance(self.conn, serial.Serial):
            return self.conn.is_open  # Serial-specific check
        return True  # For USB, assume it's valid if assigned

    def write(self, data):
        """Write data to the connected device."""
        if not self.is_connected():
            print("[!] No active connection. Cannot write.")
            return False

        try:
            self.conn.write(data)
            return True
        except Exception as e:
            print(f"[!] Write Error: {e}")
            return False

    def read(self, length=512):
        """Read data from the connected device."""
        if not self.is_connected():
            print("[!] No active connection. Cannot read.")
            return None

        try:
            return self.conn.read(length)
        except Exception as e:
            print(f"[!] Read Error: {e}")
            return None

    def close(self):
        """Close the connection if it's a serial port."""
        if isinstance(self.conn, serial.Serial) and self.conn.is_open:
            self.conn.close()
            print("[+] Serial connection closed.")
