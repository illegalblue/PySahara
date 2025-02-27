import logging
from sahara.packet_util import build_packet, parse_packet
from structures.enums import SaharaCommands

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def test_packet_conversion():
    """Test building, serializing, and parsing packets dynamically."""
    for command in SaharaCommands:
        command_id = command.value
        logging.info(f"\nTesting Command: {command.name} (ID: {command_id})")

        try:
            # Build packet with default zeroed values
            packet = build_packet(command_id)
            logging.debug(f"Built Packet: {packet}")

            # Serialize to bytes
            packet_bytes = packet.serialize()
            logging.debug(f"Serialized Packet: {packet_bytes.hex()}")

            # Parse back to struct
            parsed_packet = parse_packet(command_id, packet_bytes)
            logging.debug(f"Parsed Packet: {parsed_packet}")

            # Log parsed field details
            for field, value in parsed_packet.__dict__.items():
                logging.debug(f"{field}: {value} (Type: {type(value).__name__})")

        except Exception as e:
            logging.error(f"Error processing {command.name}: {e}")


if __name__ == "__main__":
    test_packet_conversion()