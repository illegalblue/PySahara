# * Guest - You
# * Host - Phone
# * A general session works like this:
# *  Guest -> Connect
# *  Host -> Guest | Command: Hello - Specifying which mode it is in and its supported versions/buffer size 
# *  Guest -> Host | Command: Hello - Respond with the same mode or a new mode and tell your versions/buffer size
# *  Host -> ACK or NCK | Branch depending on mode:
# *				SaharaMemoryDebugRequest - Memory Debug
# *				SaharaCommandReadyResponse - Send Command
# *				SaharaReadDataRequest - Send Image
# *				SaharaEndImageTransferResponse - Error
# */
from enum import Enum

class SaharaCommands(Enum):
	CommandHello             = 0x01 # Initialize connection and protocol
	CommandHelloResponse     = 0x02 # Acknowledge connection/protocol mode of operation
	CommandReadData          = 0x03 # Read specified number of bytes from host
	CommandEndImageTransfer  = 0x04 # image transfer end / target transfer failure
	CommandDone              = 0x05 # Acknowledgement: image transfer is complete
	CommandDoneResponse      = 0x06 # Target is exiting protocol
	CommandReset             = 0x07 # Instruct target to perform a reset
	CommandResetResponse     = 0x08 # Indicate to host that target is about to reset
	CommandMemoryDebug       = 0x09 # Indicate to host: target debug mode & ready to transfer memory content
	CommandMemoryRead        = 0x0A # Read number of bytes starting from a specified address
	CommandReady             = 0x0B # Indicate to host: target ready to receive client commands
	CommandSwitchMode        = 0x0C # Switch to a mode defined in enum SAHARA_MODE
	CommandExecute           = 0x0D # Indicate to host: to execute a given client command
	CommandExecuteResponse	= 0x0E # Indicate to host: target command execution status
	CommandExecuteData		= 0x0F # Indicate to target that host is ready to receive (more) data
	CommandMemoryDebug64     = 0x10
	CommandMemoryRead64      = 0x11


class SaharaMode(Enum): 
	ModeImageTxPending  = 0x00
	ModeImageTxComplete = 0x01  
	ModeMemoryDebug     = 0x02
	ModeCommand         = 0x03

class SaharaClientCmd(Enum): 
	  ClientCmdNop                    = 0x00
	  ClientCmdSerialNumRead          = 0x01
	  ClientCmdMsmHWIDRead            = 0x02
	  ClientOemPkHashRead			 = 0x03
	  ClientCmdSwitchDMSS			 = 0x04 # haven't found a device/mode this works on
	  ClientCmdSwitchToStreamingDload = 0x05 # haven't found a device/mode this works on
	  ClientCmdReadDebugData          = 0x06
	  ClientCmdGetSblVersion			 = 0x07

class SaharaStatusCode(Enum):
	StatusSuccess                      = 0x00
	StatusInvalidCmd                   = 0x01
	StatusProtocolMismatch             = 0x02
	StatusInvalidTargetProtocol        = 0x03
	StatusInvalidHostProtocol          = 0x04
	StatusInvalidPacketSize            = 0x05
	StatusUnexpectedImageId            = 0x06
	StatusInvalidHeaderSize            = 0x07
	StatusInvalidDataSize              = 0x08
	StatusInvalidImageType             = 0x09
	StatusInvalidTxLength              = 0x0A
	StatusInvalidRxLength              = 0x0B
	StatusTxRxError					  = 0x0C
	StatusReadDataError                = 0x0D
	StatusUnsupportedNumPhdrs          = 0x0E
	StatusInvalidPhdrSize              = 0x0F
	StatusMultipleSharedSeg            = 0x10
	StatusUninitPhdrLoc                = 0x11
	StatusInvalidDestAddress           = 0x12
	StatusInvalidImageHeaderSize       = 0x13
	StatusInvalidElfHeader             = 0x14
	StatusUnknownError				  = 0x15
	StatusTimeoutRx                    = 0x16
	StatusTimeoutTx                    = 0x17
	StatusInvalidMode				  = 0x18
	StatusInvalidMemoryRead            = 0x19
	StatusInvalidDataSizeRequest       = 0x1A
	StatusMemoryDebugNotSupported      = 0x1B
	StatusInvalidModeSwitch            = 0x1C
	StatusExecFailure				  = 0x1D
	StatusExecCmdInvalidParam          = 0x1E
	StatusExecCmdUnsupported           = 0x1F
	StatusExecDataInvalid			  = 0x20
	StatusHashTableAuthFailure         = 0x21
	StatusHashVerificationFailure      = 0x22
	StatusHashTableNotFound            = 0x23
	StatusTargetInitFailure            = 0x24
	StatusImageAuthFailure             = 0x25
	StatusInvalidImgHashTableSize	  = 0x26
	StatusMax                          = 0x30
