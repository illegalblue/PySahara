from device_setup import edlDevice

vid = 0x05C6
pid = 0x9008

edldevice = edlDevice(vid=vid, pid=pid).getelddevice()
print(edldevice)
