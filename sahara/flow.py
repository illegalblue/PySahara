import struct
import logging
from structures.sahara_definitions import SaharaHeader
from structures.sahara_enums import SaharaCommand, SaharaMode
from serial import SaharaSerial

logging.basicConfig(level=logging.INFO, format="%(message)s")

class SaharaHandshake:
    def __init__(self, serial: SaharaSerial):
        self.serial = serial

    def send_hello(self):
        """Send a Hello request to the device."""
        header = SaharaHeader(command=SaharaCommand.HELLO, length=8)
        hello_packet = header.to_bytes()

        logging.info("[+] Sending Hello request...")
        self.serial.write_data(hello_packet)

    def receive_hello_response(self):
        """Receive and decode the Hello response."""
        logging.info("[+] Waiting for Hello response...")
        data = self.serial.read_data(48)  # Expecting a 48-byte Hello response

        if not data:
            logging.error("[-] No response received for Hello request.")
            return None

        if len(data) < 48:
            logging.warning("[-] Incomplete Hello response received!")

        # Unpacking structure: <IIIIIIIIIIII>
        fields = struct.unpack("<IIIIIIIIIIII", data)

        hello_response = {
            "command": fields[0],
            "length": fields[1],
            "version": fields[2],
            "min_version": fields[3],
            "max_packet_size": fields[4],
            "mode": fields[5],
            "reserved": fields[6:12]  # Reserved fields
        }

        logging.info("\n--- Device Hello Response ---")
        for key, value in hello_response.items():
            logging.info(f"{key.ljust(20)}: {value}")

        return hello_response

    def send_hello_ack(self, hello_response):
        """Send Hello Acknowledgment based on the received Hello response."""
        header = SaharaHeader(command=SaharaCommand.HELLO_ACK, length=48)

        ack_packet = struct.pack(
            "<IIIIIIIIIIII",
            header.command,          # 0x02 (HELLO_ACK command)
            header.length,           # 48 bytes
            hello_response['version'],
            hello_response['min_version'],
            0,                       # Status (0 = success)
            SaharaMode.COMMAND_MODE, # Mode (set to Command mode)
            1, 2, 3, 4, 5, 6         # Reserved fields
        )

        logging.info("[+] Sending Hello Acknowledgment...")
        self.serial.write_data(ack_packet)

    def receive_command_ready(self):
        """Wait for Command Ready confirmation from the device."""
        logging.info("[+] Waiting for Command Ready response...")
        data = self.serial.read_data(12)  # Expecting a 12-byte response

        if not data:
            logging.error("[-] No response received after Hello Ack.")
            return None

        if len(data) < 12:
            logging.warning("[-] Incomplete Command Ready response received!")

        # Unpacking structure: <II>
        command_id, length, status = struct.unpack("<III", data + b"\x00\x00\x00\x00")  # Padding if needed

        if command_id == SaharaCommand.COMMAND_READY:
            logging.info(f"[✔] Device is in Command Ready Mode ✅ (Status: {status})")
            return True
        else:
            logging.error("[-] Unexpected response after Hello Ack.")
            return False

    def perform_handshake(self):
        """Full handshake sequence."""
        self.send_hello()
        hello_response = self.receive_hello_response()
        if not hello_response:
            return False

        self.send_hello_ack(hello_response)
        return self.receive_command_ready()
