from dataclasses import dataclass, field
from typing import List
from structures.definitions import SAHARA_PACKET_FORMATS  # Import packet formats
from structures.enums import SaharaCommands  # Import command IDs

@dataclass
class SaharaHeader:
    command: int
    length: int

@dataclass
class SaharaAbstractPacket:
    header: SaharaHeader
    parameters: List[int] = field(default_factory=lambda: [0, 0])

def create_packet_class(command):
    """Dynamically generate a packet dataclass based on command definition."""
    if command not in SAHARA_PACKET_FORMATS:
        raise ValueError(f"Unknown Command ID: {command}")

    definition = SAHARA_PACKET_FORMATS[command]
    fields = definition["fields"]

    # Create field mappings dynamically
    field_definitions = {"header": SaharaHeader}
    for field_name in fields[2:]:  # Skip first 2 (command & length)
        if "reserved" in field_name:
            field_definitions[field_name] = field(default_factory=lambda: [0] * 6)
        elif field_name == "hash":
            field_definitions[field_name] = bytes(32)
        elif field_name == "message":
            field_definitions[field_name] = bytes(64)  # Assuming SAHARA_LOG_LENGTH = 64
        elif field_name in ["name", "filename"]:
            field_definitions[field_name] = bytes(20)
        else:
            field_definitions[field_name] = int

    # Create and return the dataclass
    return dataclass(type(f"Sahara{command.name}", (object,), field_definitions))

# Define classes dynamically based on known commands
SaharaHelloRequest = create_packet_class(SaharaCommands.HELLO)
SaharaHelloResponse = create_packet_class(SaharaCommands.HELLO_RESPONSE)
SaharaReadDataRequest = create_packet_class(SaharaCommands.READ_DATA)
SaharaEndImageTransferResponse = create_packet_class(SaharaCommands.END_TRANSFER)
SaharaDoneRequest = create_packet_class(SaharaCommands.DONE)
SaharaDoneResponse = create_packet_class(SaharaCommands.DONE_RESPONSE)
SaharaResetRequest = create_packet_class(SaharaCommands.RESET)
SaharaResetResponse = create_packet_class(SaharaCommands.RESET_RESPONSE)
SaharaMemoryDebugRequest = create_packet_class(SaharaCommands.MEMORY_DEBUG)
SaharaMemoryReadRequest = create_packet_class(SaharaCommands.MEMORY_READ)
SaharaCommandReadyResponse = create_packet_class(SaharaCommands.COMMAND_READY)
SaharaSwitchModeRequest = create_packet_class(SaharaCommands.SWITCH_MODE)
SaharaClientCommandRequest = create_packet_class(SaharaCommands.CLIENT_COMMAND)
SaharaClientCommandResponse = create_packet_class(SaharaCommands.CLIENT_COMMAND_RESPONSE)
SaharaClientCommandExecuteDataRequest = create_packet_class(SaharaCommands.CLIENT_COMMAND_EXECUTE)
SaharaMemoryDebug64Request = create_packet_class(SaharaCommands.MEMORY_DEBUG_64)
SaharaMemoryRead64Request = create_packet_class(SaharaCommands.MEMORY_READ_64)
SaharaMsmHwIdResponse = create_packet_class(SaharaCommands.MSM_HW_ID)
SaharaSerialNumberResponse = create_packet_class(SaharaCommands.SERIAL_NUMBER)
SaharaSblVersionResponse = create_packet_class(SaharaCommands.SBL_VERSION)
SaharaOemPkHashResponse = create_packet_class(SaharaCommands.OEM_PK_HASH)
SaharaDebugLogEntry = create_packet_class(SaharaCommands.DEBUG_LOG)
SaharaMemoryTableEntry = create_packet_class(SaharaCommands.MEMORY_TABLE)
