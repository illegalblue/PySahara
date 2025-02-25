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

class SaharaCommand(Enum): 
	kSaharaCommandHello             = 0x01 # Initialize connection and protocol
	kSaharaCommandHelloResponse     = 0x02 # Acknowledge connection/protocol mode of operation
	kSaharaCommandReadData          = 0x03 # Read specified number of bytes from host
	kSaharaCommandEndImageTransfer  = 0x04 # image transfer end / target transfer failure
	kSaharaCommandDone              = 0x05 # Acknowledgement: image transfer is complete
	kSaharaCommandDoneResponse      = 0x06 # Target is exiting protocol
	kSaharaCommandReset             = 0x07 # Instruct target to perform a reset
	kSaharaCommandResetResponse     = 0x08 # Indicate to host that target is about to reset
	kSaharaCommandMemoryDebug       = 0x09 # Indicate to host: target debug mode & ready to transfer memory content
	kSaharaCommandMemoryRead        = 0x0A # Read number of bytes starting from a specified address
	kSaharaCommandReady             = 0x0B # Indicate to host: target ready to receive client commands
	kSaharaCommandSwitchMode        = 0x0C # Switch to a mode defined in enum SAHARA_MODE
	kSaharaCommandExecute           = 0x0D # Indicate to host: to execute a given client command
	kSaharaCommandExecuteResponse	= 0x0E # Indicate to host: target command execution status
	kSaharaCommandExecuteData		= 0x0F # Indicate to target that host is ready to receive (more) data
	kSaharaCommandMemoryDebug64     = 0x10
	kSaharaCommandMemoryRead64      = 0x11


class SaharaMode(Enum): 
	kSaharaModeImageTxPending  = 0x00
	kSaharaModeImageTxComplete = 0x01  
	kSaharaModeMemoryDebug     = 0x02
	kSaharaModeCommand         = 0x03

class SaharaClientCmd(Enum): 
	  kSaharaClientCmdNop                    = 0x00
	  kSaharaClientCmdSerialNumRead          = 0x01
	  kSaharaClientCmdMsmHWIDRead            = 0x02
	  kSaharaClientOemPkHashRead			 = 0x03
	  kSaharaClientCmdSwitchDMSS			 = 0x04 # haven't found a device/mode this works on
	  kSaharaClientCmdSwitchToStreamingDload = 0x05 # haven't found a device/mode this works on
	  kSaharaClientCmdReadDebugData          = 0x06
	  kSaharaClientCmdGetSblVersion			 = 0x07

class SaharaStatusCode(Enum):
	kSaharaStatusSuccess                      = 0x00
	kSaharaStatusInvalidCmd                   = 0x01
	kSaharaStatusProtocolMismatch             = 0x02
	kSaharaStatusInvalidTargetProtocol        = 0x03
	kSaharaStatusInvalidHostProtocol          = 0x04
	kSaharaStatusInvalidPacketSize            = 0x05
	kSaharaStatusUnexpectedImageId            = 0x06
	kSaharaStatusInvalidHeaderSize            = 0x07
	kSaharaStatusInvalidDataSize              = 0x08
	kSaharaStatusInvalidImageType             = 0x09
	kSaharaStatusInvalidTxLength              = 0x0A
	kSaharaStatusInvalidRxLength              = 0x0B
	kSaharaStatusTxRxError					  = 0x0C
	kSaharaStatusReadDataError                = 0x0D
	kSaharaStatusUnsupportedNumPhdrs          = 0x0E
	kSaharaStatusInvalidPhdrSize              = 0x0F
	kSaharaStatusMultipleSharedSeg            = 0x10
	kSaharaStatusUninitPhdrLoc                = 0x11
	kSaharaStatusInvalidDestAddress           = 0x12
	kSaharaStatusInvalidImageHeaderSize       = 0x13
	kSaharaStatusInvalidElfHeader             = 0x14
	kSaharaStatusUnknownError				  = 0x15
	kSaharaStatusTimeoutRx                    = 0x16
	kSaharaStatusTimeoutTx                    = 0x17
	kSaharaStatusInvalidMode				  = 0x18
	kSaharaStatusInvalidMemoryRead            = 0x19
	kSaharaStatusInvalidDataSizeRequest       = 0x1A
	kSaharaStatusMemoryDebugNotSupported      = 0x1B
	kSaharaStatusInvalidModeSwitch            = 0x1C
	kSaharaStatusExecFailure				  = 0x1D
	kSaharaStatusExecCmdInvalidParam          = 0x1E
	kSaharaStatusExecCmdUnsupported           = 0x1F
	kSaharaStatusExecDataInvalid			  = 0x20
	kSaharaStatusHashTableAuthFailure         = 0x21
	kSaharaStatusHashVerificationFailure      = 0x22
	kSaharaStatusHashTableNotFound            = 0x23
	kSaharaStatusTargetInitFailure            = 0x24
	kSaharaStatusImageAuthFailure             = 0x25
	kSaharaStatusInvalidImgHashTableSize	  = 0x26
	kSaharaStatusMax                          = 0x30
