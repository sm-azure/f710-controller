import evdev
import sys, time
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
                socket.send_json({'msg': BTNS[event.code], 'val': event.value, 'prio': 0})
                 

        if event.type == evdev.ecodes.EV_ABS:
            if event.code in ABS.keys():
                # For lateral control range is from 0 (full left) -255 (full right)
                # For step speed control values are +1 or -1 (ignore 0 as it is button return)
                #print(event.code, event.value, ABS[event.code])
                if((event.code == 17 and event.value !=0)):
                    print(event.code, event.value, ABS[event.code])
                    socket.send_json({'msg': ABS[event.code], 'val': -event.value, 'prio': 0})
                # Handle for lateral control. -1 for full left and + 1 for full right
                if(event.code == 02):
                    val = float("{:.2f}".format((event.value - 128.0)/128.0))
                    print(event.code, val, ABS[event.code])
                    socket.send_json({'msg': ABS[event.code], 'val': val, 'prio': 0})


def init_zmq(port):
    print ('Init socket', port);
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:%s" % port)
    return socket

if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT =  sys.argv[1]
        assert int(PORT)
    socket = init_zmq(PORT)
    logitech_controller_connect(socket)
    #while True:
    #    print ('Sending msg')
    #    socket.send_json({'msg': "STARTUP", 'val': -15, 'prio': 0})
    #    time.sleep(1)
    #logitech_controller_connect(socket)

    
    
