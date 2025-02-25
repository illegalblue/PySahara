import logging
from core.serial import SaharaSerial
from core.handshake import SaharaHandshake
from core.flow import SaharaFlow
from structures.sahara_enums import SaharaMode

logging.basicConfig(level=logging.INFO, format="%(message)s")

class SaharaCore:
    def __init__(self, vendor_id, product_id):
        self.serial = SaharaSerial(vendor_id, product_id)
        self.handshake = SaharaHandshake(self.serial)
        self.flow = SaharaFlow(self.serial)

    def start(self):
        """Main function to start the Sahara interaction."""
        logging.info("Starting Sahara process...")

        # Wait for the device to be in the correct mode
        if not self.serial.wait_for_device():
            logging.error("Device not detected. Exiting.")
            return

        # Perform the handshake
        hello_response = self.handshake.perform_handshake()

        if hello_response:
            logging.info("Handshake successful. Proceeding with next steps.")

            # Handle post-handshake flow
            if hello_response["mode"] == SaharaMode.COMMAND:
                self.flow.handle_command_mode()
            else:
                logging.warning(f"Unexpected mode: {hello_response['mode']}")

        else:
            logging.error("Handshake failed. Exiting.")

if __name__ == "__main__":
    VENDOR_ID = 0x05C6
    PRODUCT_ID = 0x9008

    sahara = SaharaCore(VENDOR_ID, PRODUCT_ID)
    sahara.start()
