import struct
from dataclasses import dataclass, field, fields
from typing import List, ClassVar, Type, TypeVar

T = TypeVar('T', bound='SaharaAbstractPacket')

@dataclass
class SaharaHeader:
    command: int = 0
    length: int = 0

    def serialize(self) -> bytes:
        return struct.pack("<II", self.command, self.length)

    @classmethod
    def deserialize(cls, data: bytes) -> 'SaharaHeader':
        command, length = struct.unpack("<II", data[:8])
        return cls(command=command, length=length)

@dataclass
class SaharaAbstractPacket:
    header: SaharaHeader = field(default_factory=SaharaHeader)
    _format: ClassVar[str] = "<II"  # Default header format

    import struct
    from dataclasses import fields

    def serialize(self) -> bytes:
        """Dynamically serialize packet based on class format."""

        # 1️⃣ Extract header bytes first
        header_bytes = self.header.serialize()

        body_fields = []

        for f in fields(self):  # Iterates over dataclass fields
            if f.name == "header":
                continue  # Skip header, already serialized

            value = getattr(self, f.name)

            if isinstance(value, list):
                body_fields.extend(value)  # Flatten list (e.g., reserved fields)
            else:
                body_fields.append(value)

        # 2️⃣ Dynamically calculate payload size & update header length
        payload_size = struct.calcsize(self._format)
        self.header.length = 8 + payload_size  # Header (8 bytes) + Payload

        # 3️⃣ Serialize the header again (after updating length)
        header_bytes = struct.pack("II", self.header.command, self.header.length)

        # 4️⃣ Serialize the body
        body_bytes = struct.pack(self._format, *body_fields)

        return header_bytes + body_bytes

    @classmethod
    def deserialize(cls: Type[T], data: bytes) -> T:
        """Dynamically deserialize a byte stream."""

        if len(data) < 8:
            raise ValueError(f"Invalid data length ({len(data)}), expected at least 8 bytes.")

        # 1️⃣ Extract the header (first 8 bytes)
        header = SaharaHeader.deserialize(data[:8])

        # 2️⃣ Extract the body size based on struct format
        body_size = struct.calcsize(cls._format)

        if len(data) != header.length:
            raise ValueError(f"Header length mismatch: Expected {header.length} bytes, got {len(data)}.")

        if len(data) < 8 + body_size:
            raise ValueError(f"Data too short for expected format. Expected {8 + body_size}, got {len(data)}")

        values = struct.unpack(cls._format, data[8:8 + body_size])

        field_values = {}
        index = 0

        # 3️⃣ Iterate over fields and unpack dynamically
        for f in fields(cls):
            if f.name == "header":
                field_values[f.name] = header
                continue

            field_type = f.type  # Get field type from dataclass definition

            if isinstance(getattr(cls, f.name, None), list):  # Handling lists
                list_length = len(getattr(cls, f.name))  # Get list size from class
                field_values[f.name] = list(values[index:index + list_length])
                index += list_length
            else:
                field_values[f.name] = values[index]
                index += 1

        return cls(**field_values)


# 0x01
@dataclass
class SaharaHelloRequest(SaharaAbstractPacket):
    _format: ClassVar[str] = "<IIII6I"
    version: int = 0
    min_version: int = 0
    max_command_packet_size: int = 0
    mode: int = 0
    reserved: List[int] = field(default_factory=lambda: [0] * 6)


# 0x02
@dataclass
class SaharaHelloResponse(SaharaAbstractPacket):
    _format: ClassVar[str] = "<IIII6I"
    version: int = 0
    min_version: int = 0
    status: int = 0
    mode: int = 0
    reserved: List[int] = field(default_factory=lambda: [0] * 6)

# 0x03
@dataclass
class SaharaReadDataRequest(SaharaAbstractPacket):
    _format: ClassVar[str] = "<III"
    image_id: int = 0
    offset: int = 0
    size: int = 0

@dataclass
class SaharaEndImageTransferResponse(SaharaAbstractPacket):
    _format: ClassVar[str] = "<II"
    file: int = 0
    status: int = 0

# 0x05
@dataclass
class SaharaDoneRequest(SaharaAbstractPacket):
    _format: ClassVar[str] = ""

# 0x06
@dataclass
class SaharaDoneResponse(SaharaAbstractPacket):
    _format: ClassVar[str] = "<I"
    image_tx_status: int = 0  # 0 pending, 1 complete

# 0x07
@dataclass
class SaharaResetRequest(SaharaAbstractPacket):
    _format: ClassVar[str] = ""

# 0x08
@dataclass
class SaharaResetResponse(SaharaAbstractPacket):
    _format: ClassVar[str] = ""

# 0x09
@dataclass
class SaharaMemoryDebugRequest(SaharaAbstractPacket):
    _format: ClassVar[str] = "<II"
    memory_table_address: int = 0
    memory_table_length: int = 0

# 0x0a
@dataclass
class SaharaMemoryReadRequest(SaharaAbstractPacket):
    _format: ClassVar[str] = "<II"
    address: int = 0
    size: int = 0

# 0x0b
@dataclass
class SaharaCommandReadyResponse(SaharaAbstractPacket):
    _format: ClassVar[str] = "<I"
    image_tx_status: int = 0  # 0 pending, 1 complete

# 0x0c
@dataclass
class SaharaSwitchModeRequest(SaharaAbstractPacket):
    _format: ClassVar[str] = "<I"
    mode: int = 0

# 0x0d
@dataclass
class SaharaClientCommandRequest(SaharaAbstractPacket):
    _format: ClassVar[str] = "<I"
    command: int = 0

# 0x0e
@dataclass
class SaharaClientCommandResponse(SaharaAbstractPacket):
    _format: ClassVar[str] = "<II"
    command: int = 0
    size: int = 0

# 0x0f
@dataclass
class SaharaClientCommandExecuteDataRequest(SaharaAbstractPacket):
    _format: ClassVar[str] = "<I"
    command: int = 0

# 0x10
@dataclass
class SaharaMemoryDebug64Request(SaharaAbstractPacket):
    _format: ClassVar[str] = "<II"
    memory_table_address: int = 0
    memory_table_length: int = 0

# 0x11
@dataclass
class SaharaMemoryRead64Request(SaharaAbstractPacket):
    _format: ClassVar[str] = "<II"
    address: int = 0
    size: int = 0

# MSM HW ID Response
@dataclass
class SaharaMsmHwIdResponse:
    _format: ClassVar[str] = "<III"
    unknown1: int = 0
    unknown2: int = 0
    msm_id: int = 0

# Serial Number Response
@dataclass
class SaharaSerialNumberResponse:
    _format: ClassVar[str] = "<I"
    serial: int = 0

# SBL Version Response
@dataclass
class SaharaSblVersionResponse:
    _format: ClassVar[str] = "<I"
    version: int = 0

# OEM PK Hash Response
@dataclass
class SaharaOemPkHashResponse:
    hash: bytes = field(default_factory=lambda: bytes(32))  # 32 bytes

# Debug Log Entry
@dataclass
class SaharaDebugLogEntry:
    message: bytes = field(default_factory=lambda: bytes(64))  # Should be of length SAHARA_LOG_LENGTH

# Memory Table Entry (Packed Struct Equivalent)
@dataclass
class SaharaMemoryTableEntry:
    _format: ClassVar[str] = "<II20s20s"
    unknown1: int = 0
    address: int = 0
    size: int = 0
    name: bytes = field(default_factory=lambda: bytes(20))    # 20 bytes
    filename: bytes = field(default_factory=lambda: bytes(20))  # 20 bytes
