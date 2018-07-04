import evdev
import sys
import zmq

PORT = "7772"

def logitech_controller_connect(socket):

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
    #print (control_f710.capabilities(verbose=True))

    # Define keys of interest
    BTNS = {305: "STARTUP", 306: "SHUTDOWN", 308: "ZERO_SPEED"}
    ABS = {02: "LATERAL", 17: "SPEED_STEP"}

    for event in control_f710.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            if event.code in BTNS.keys() and event.value!= 0L:
                print (event.code, event.value, BTNS[event.code])

        if event.type == evdev.ecodes.EV_ABS:
            if event.code in ABS.keys():
                # For lateral control range is from 0 (full left) -255 (full right)
                # For step speed control values are +1 or -1 (ignore 0 as it is button return)
                #print(event.code, event.value, ABS[event.code])
                if((event.code == 17 and event.value !=0) or event.code == 02):
                    #print ('---')
                    print(event.code, event.value, ABS[event.code])


def init_zmq(port):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    return socket

if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT =  sys.argv[1]
        assert int(PORT)
    socket = init_zmq(PORT)
    socket.send_json({'msg': "STARTUP", 'val': -15, 'prio': 0})
    #logitech_controller_connect(socket)

    
    
