from device_setup import edlDevice
from device_io import  DeviceIO

vid = 0x05C6
pid = 0x9008

edldevice = edlDevice(vid=vid, pid=pid).getelddevice()
print(edldevice)
io = DeviceIO(edldevice=edldevice)
print(io.is_connected())

print(io.read(512))
