import struct
import dataclasses
import typing

from sahara.mapping import get_structure
from structures.definitions import SaharaHeader
from typing import get_origin

def build_packet(command_id, **kwargs):
    """Builds a packet with default values for missing fields."""
    packet_class = get_structure(command_id)
    if not packet_class:
        raise ValueError(f"Unknown command ID: {command_id}")


    # Ensure all fields have default values
    field_defaults = {
        field.name: (
            field.default if field.default != dataclasses.MISSING else
            (field.default_factory() if callable(field.default_factory) else 0)
        )
        for field in dataclasses.fields(packet_class) if field.name not in ["header", "_format"]  # Ignore _format
    }

    field_defaults.update(kwargs)  # Override defaults with user-provided values

    # Create packet with correct length
    header = SaharaHeader(command=command_id, length=0)
    packet = packet_class(header=header, **field_defaults)
    packet.header.length = get_packet_length(packet)

    return packet


def parse_packet(command_id, data):
    """Parses a byte stream into the corresponding packet structure, handling padding."""
    packet_class = get_structure(command_id)
    if not packet_class:
        raise ValueError(f"Unknown command ID: {command_id}")

    expected_length = align_to_4(get_packet_length(packet_class()))
    if len(data) != expected_length:
        raise ValueError(f"Expected {expected_length} bytes, but got {len(data)}")

    header = SaharaHeader.deserialize(data[:8])  # First 8 bytes are header
    body_data = data[8:]

    field_names = list(packet_class.__dataclass_fields__.keys())[1:]  # Skip header



    if hasattr(packet_class, "_format"):
        field_values = struct.unpack(packet_class._format, body_data)
        # print(f"Parsing {packet_class.__name__} with format: {packet_class._format}")
        # print(f"Raw field values: {field_values}")

    else:
        raise ValueError(f"Packet class {packet_class.__name__} is missing _format definition")


    parsed_data = {}
    offset = 0  # Track position in field_values

    for field_name, field_info in packet_class.__dataclass_fields__.items():
        if field_name == "header" or field_name == "_format":
            continue  # Header is already handled

        field_type = field_info.type  # Extract type annotation

        # print(f"Processing field: {field_name}, Expected type: {field_type}, Value: {field_values[offset]}")

        # Properly check if the field is a list[int]
        if get_origin(field_type) is list:
            list_length = len(field_values) - offset  # Remaining values belong to the list
            parsed_data[field_name] = list(field_values[offset:offset + list_length])
            # print(f"Detected list field: {field_name}, Assigning: {parsed_data[field_name]}")
            offset += list_length  # Move offset forward
        else:
            parsed_data[field_name] = field_values[offset]
            offset += 1  # Move offset forward by 1 for single-value fields
    return packet_class(header=header, **parsed_data)


def get_packet_length(packet):
    """Calculates the actual byte length of a packet, including padding."""
    if hasattr(packet, "_format"):  # If the packet defines _format, use it
        struct_size = struct.calcsize(packet._format)
        return align_to_4(8 + struct_size)  # 8 for header + formatted size

    total_size = struct.calcsize("<II")  # SaharaHeader is always 8 bytes
    for field_name, field_info in packet.__dataclass_fields__.items():
        field_value = getattr(packet, field_name)

        if isinstance(field_value, int):
            total_size += 4
        elif isinstance(field_value, bytes):
            total_size += len(field_value)
        elif dataclasses.is_dataclass(field_value):
            total_size += get_packet_length(field_value)

    return align_to_4(total_size)  # Ensure final size is 4-byte aligned


def align_to_4(value):
    """Ensures the value is aligned to 4 bytes."""
    return (value + 3) & ~3


test_packet = build_packet(1)  # CommandHello
print("Calculated Length:", get_packet_length(test_packet))
print("Serialized Length:", len(test_packet.serialize()))
