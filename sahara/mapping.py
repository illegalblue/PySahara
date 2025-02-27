from structures.enums import SaharaCommands
from structures.definitions import (
    SaharaHelloRequest, SaharaHelloResponse, SaharaReadDataRequest,
    SaharaEndImageTransferResponse, SaharaDoneRequest, SaharaDoneResponse,
    SaharaResetRequest, SaharaResetResponse, SaharaMemoryDebugRequest,
    SaharaMemoryReadRequest, SaharaCommandReadyResponse, SaharaSwitchModeRequest,
    SaharaClientCommandRequest, SaharaClientCommandResponse,
    SaharaClientCommandExecuteDataRequest, SaharaMemoryDebug64Request,
    SaharaMemoryRead64Request
)

# ✅ UPDATED: MAPPING COMMAND ID -> STRUCTURE
COMMAND_STRUCT_MAP = {
    SaharaCommands.CommandHello.value: SaharaHelloRequest,
    SaharaCommands.CommandHelloResponse.value: SaharaHelloResponse,
    SaharaCommands.CommandReadData.value: SaharaReadDataRequest,
    SaharaCommands.CommandEndImageTransfer.value: SaharaEndImageTransferResponse,
    SaharaCommands.CommandDone.value: SaharaDoneRequest,
    SaharaCommands.CommandDoneResponse.value: SaharaDoneResponse,
    SaharaCommands.CommandReset.value: SaharaResetRequest,
    SaharaCommands.CommandResetResponse.value: SaharaResetResponse,
    SaharaCommands.CommandMemoryDebug.value: SaharaMemoryDebugRequest,
    SaharaCommands.CommandMemoryRead.value: SaharaMemoryReadRequest,
    SaharaCommands.CommandReady.value: SaharaCommandReadyResponse,
    SaharaCommands.CommandSwitchMode.value: SaharaSwitchModeRequest,
    SaharaCommands.CommandExecute.value: SaharaClientCommandRequest,
    SaharaCommands.CommandExecuteResponse.value: SaharaClientCommandResponse,
    SaharaCommands.CommandExecuteData.value: SaharaClientCommandExecuteDataRequest,
    SaharaCommands.CommandMemoryDebug64.value: SaharaMemoryDebug64Request,
    SaharaCommands.CommandMemoryRead64.value: SaharaMemoryRead64Request,
}


def get_structure(command_id):
    """Retrieve the corresponding dataclass for a given command ID."""
    struct = COMMAND_STRUCT_MAP.get(command_id)

    if struct is None:
        print(f"⚠️ Warning: Unknown command ID {command_id} (ignoring packet)")

    return struct
