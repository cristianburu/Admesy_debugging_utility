

import ctypes

libusbtmc = ctypes.CDLL ("./x64/libusbtmc_x64.dll")

py_usbtmc_init = libusbtmc.usbtmc_init

py_usbtmc_get_version = libusbtmc.usbtmc_get_version
py_usbtmc_get_version.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
py_usbtmc_get_version.restype = None

py_usbtmc_find_devices = libusbtmc.usbtmc_find_devices
py_usbtmc_find_devices.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
py_usbtmc_find_devices.restype = ctypes.c_int32

py_usbtmc_open = libusbtmc.usbtmc_open
py_usbtmc_open.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32)]
py_usbtmc_open.restype = ctypes.c_int32

py_usbtmc_write = libusbtmc.usbtmc_write
py_usbtmc_write.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32]
py_usbtmc_write.restype = ctypes.c_int32

py_usbtmc_read = libusbtmc.usbtmc_read
py_usbtmc_read.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32]
py_usbtmc_read.restype = ctypes.c_int32

py_usbtmc_close = libusbtmc.usbtmc_close
py_usbtmc_close.argtypes = [ctypes.POINTER(ctypes.c_uint32)]
py_usbtmc_close.restype = ctypes.c_int32

# Initialization
py_usbtmc_init()

# Get libusbtmc version
version = ctypes.create_string_buffer (10)
py_usbtmc_get_version(version, 10)
print ("Libusbtmc version is " + version.value.decode("utf-8"))

# Get devices list
buffer_size = 256 * 127
usbtmcdevices = ctypes.create_string_buffer (buffer_size)
error_find_devices = py_usbtmc_find_devices (usbtmcdevices, buffer_size)
print (f"Find devices function returned error = {error_find_devices}")
first_device_found = usbtmcdevices.value.decode("utf-8").split("\n")[0]
print (f"First device found is {first_device_found}")

# Open device
handle = ctypes.c_uint32 (77) # Whatever value to initialize
#print (handle)
#print (handle.value)
ptr_handle = ctypes.pointer (handle)
error_open = py_usbtmc_open (usbtmcdevices, ptr_handle)
print (f"Open device function returned error = {error_open}")
handle_py = int (ptr_handle.contents.value)
print (f"Handle of device is {handle_py}")

# Write to device an average
command_py = ":SENSe:SP:AVERAGE 99\n"
buffer_length = len (command_py)
timeout_ms = 5000
error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
print (f"Write function returned error = {error_write} bytes written")

# Read from device an int time from Internal Memory
command_py = ":SENSe:INT?\n"
buffer_length = len (command_py)
timeout_ms = 5000
error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
bytecount = 4096
read_data = ctypes.create_string_buffer (bytecount)
error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
int_time_read_internal_mem = int (read_data.value.decode("utf-8")[:error_read])
print (f"Int. time read from Internal Memory is {int_time_read_internal_mem} μSeconds")

# Read from device an Average from EEPROM
command_py = ":EEPROM:CONFigure:SPAVG?\n"
buffer_length = len (command_py)
timeout_ms = 5000
error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
bytecount = 4096
read_data = ctypes.create_string_buffer (bytecount)
error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
avg_read_EEPROM = int (read_data.value.decode("utf-8")[:error_read])
print (f"Average read from EEPROM is {avg_read_EEPROM}")




# Close device
error_close = py_usbtmc_close (ptr_handle)
print (f"Close function error returned = {error_close}")

print ("Done!")