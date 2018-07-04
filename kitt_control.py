import evdev
import sys

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    if(device.name == 'Logitech Logitech Cordless RumblePad 2'):
        print(device.path, device.name, device.phys)
        control_f710 = device

# Check if controller exisits
if 'control_f710' not in locals():
    print ("Is the controller connected or on?")
    sys.exit(-1)
else:
    print ("Found controller on {}..",control_f710.path)


# Print device capabilities
print (control_f710.capabilities(verbose=True))

for event in control_f710.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        print (event.code, event.value)
    if event.type == evdev.ecodes.EV_ABS:
       print (event)
    
    
