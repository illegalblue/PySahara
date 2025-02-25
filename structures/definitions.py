from dataclasses import dataclass, field
from typing import List

@dataclass
class SaharaHeader:
    command: int
    length: int

@dataclass
class SaharaAbstractPacket:
    header: SaharaHeader
    parameters: List[int] = field(default_factory=lambda: [0, 0])

# 0x01
@dataclass
class SaharaHelloRequest: 
    header: SaharaHeader
    version: int
    min_version: int
    max_command_packet_size: int
    mode: int
    reserved: List[int] = field(default_factory=lambda: [0] * 6)


# 0x02
@dataclass
class SaharaHelloResponse:
    header: SaharaHeader
    version: int
    min_version: int
    status: int
    mode: int
    reserved: List[int] = field(default_factory=lambda: [0] * 6)

# 0x03
@dataclass
class SaharaReadDataRequest:
    header: SaharaHeader
    image_id: int
    offset: int
    size: int


@dataclass
class SaharaEndImageTransferResponse:
    header: SaharaHeader
    file: int
    status: int

# 0x05
@dataclass
class SaharaDoneRequest:
    header: SaharaHeader

# 0x06
@dataclass
class SaharaDoneResponse:
    header: SaharaHeader
    image_tx_status: int  # 0 pending, 1 complete

# 0x07
@dataclass
class SaharaResetRequest:
    header: SaharaHeader

# 0x08
@dataclass
class SaharaResetResponse:
    header: SaharaHeader

# 0x09
@dataclass
class SaharaMemoryDebugRequest:
    header: SaharaHeader
    memory_table_address: int
    memory_table_length: int

# 0x0a
@dataclass
class SaharaMemoryReadRequest:
    header: SaharaHeader
    address: int
    size: int

# 0x0b
@dataclass
class SaharaCommandReadyResponse:
    header: SaharaHeader
    image_tx_status: int  # 0 pending, 1 complete

# 0x0c
@dataclass
class SaharaSwitchModeRequest:
    header: SaharaHeader
    mode: int

# 0x0d
@dataclass
class SaharaClientCommandRequest:
    header: SaharaHeader
    command: int

# 0x0e
@dataclass
class SaharaClientCommandResponse:
    header: SaharaHeader
    command: int
    size: int

# 0x0f
@dataclass
class SaharaClientCommandExecuteDataRequest:
    header: SaharaHeader
    command: int

# 0x10
@dataclass
class SaharaMemoryDebug64Request:
    header: SaharaHeader
    memory_table_address: int
    memory_table_length: int

# 0x11
@dataclass
class SaharaMemoryRead64Request:
    header: SaharaHeader
    address: int
    size: int

# MSM HW ID Response
@dataclass
class SaharaMsmHwIdResponse:
    unknown1: int  
    unknown2: int  
    msm_id: int    

# Serial Number Response
@dataclass
class SaharaSerialNumberResponse:
    serial: int   

# SBL Version Response
@dataclass
class SaharaSblVersionResponse:
    version: int   

# OEM PK Hash Response
@dataclass
class SaharaOemPkHashResponse:
    hash: bytes  # 32 bytes

# Debug Log Entry
@dataclass
class SaharaDebugLogEntry:
    message: bytes  # Should be of length SAHARA_LOG_LENGTH

# Memory Table Entry (Packed Struct Equivalent)
@dataclass
class SaharaMemoryTableEntry:
    unknown1: int  
    address: int   
    size: int      
    name: bytes    # 20 bytes
    filename: bytes  # 20 bytes


