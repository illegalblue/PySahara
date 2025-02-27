import serial
import serial.tools.list_ports
import time


class SerialEDLDevice:
    def __init__(self, baudrate=115200):
        self.baudrate = baudrate
        self.com_port = None
        self.serial_conn = None

    def wait_for_device(self, timeout=10):
        """Wait for the Qualcomm EDL COM port to appear, with a timeout."""
        print("[*] Waiting for EDL device...")
        elapsed = 0
        while elapsed < timeout:
            port = self.find_edl_port()
            if port:
                self.com_port = port
                print(f"[+] Device detected on {port}!")
                return True
            time.sleep(1)
            elapsed += 1
            print(f"[-] Still waiting... ({elapsed}s)")

        print("[!] Device not found within timeout.")
        return False

    def find_edl_port(self):
        """Find the Qualcomm EDL (9008) COM port dynamically."""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "Qualcomm" in port.description or "QDLoader" in port.description:
                return port.device  # Example: COM3
        return None

    def open_connection(self):
        """Open a serial connection to the detected COM port."""
        if not self.com_port:
            print("[!] No valid EDL COM port found.")
            return None

        try:
            self.serial_conn = serial.Serial(self.com_port, self.baudrate, timeout=1)
            print(f"[+] Connected to {self.com_port}")
            return self.serial_conn  # Return the established connection
        except serial.SerialException as e:
            print(f"[!] Serial Error: {e}")
            return None

    def close_connection(self):
        """Close the serial connection."""
        if self.serial_conn:
            self.serial_conn.close()
            print("[+] Connection closed.")


if __name__ == "__main__":
    edl = SerialEDLDevice()

    if edl.wait_for_device():
        conn = edl.open_connection()
        if conn:
            conn.close()  # Close explicitly
