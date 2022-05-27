import re
from setup import *
import time
from MX100QP import *



## Nanotec controller


def initValve():
    # Go trough state machine to active controller
    switchOffValve()
    switchOnValve()


def switchOnValve():
    # Connect to controller
    setup.initConnection()

    # Create string parameters to send to controller
    post = b"POST /od/" + str.encode(setup.indexControlword) + b"/" \
           + str.encode(setup.subindexControlword) + b" HTTP/1.0\r\nContent-Type: " \
                                                     b"application/x-www-form-urlencoded\r" \
                                                     b"\nContent-Length: " \
           + str.encode(setup.bitLengthControlword) + b"\r\n\r\n\"" \
           + str.encode(setup.valueControlwordOn) + b"\""

    # Send parameters to controller
    setup.initConnection().send(post)
    setup.initConnection().close()


def switchOffValve():
    # Connect to controller
    setup.initConnection()

    # Create string parameters to send to controller
    post = b"POST /od/" + str.encode(setup.indexControlword) + b"/" \
           + str.encode(setup.subindexControlword) + b" HTTP/1.0\r\nContent-Type: " \
                                                     b"application/x-www-form-urlencoded\r" \
                                                     b"\nContent-Length: " \
           + str.encode(setup.bitLengthControlword) + b"\r\n\r\n\"" \
           + str.encode(setup.valueControlwordOff) + b"\""

    # Send parameters to controller
    setup.initConnection().send(post)
    setup.initConnection().close()


def moveValve():
    # Connect to controller
    setup.initConnection()

    # Create string parameters to send to controller
    post = b"POST /od/" + str.encode(setup.indexControlword) + b"/" \
           + str.encode(setup.subindexControlword) + b" HTTP/1.0\r\nContent-Type: " \
                                                     b"application/x-www-form-urlencoded\r" \
                                                     b"\nContent-Length: " \
           + str.encode(setup.bitLengthControlword) + b"\r\n\r\n\"" \
           + str.encode(setup.valueControlwordMove) + b"\""

    # Send parameters to controller
    setup.initConnection().send(post)
    setup.initConnection().close()

    # Wait for valve to reach position
    time.sleep(20)

    # Shut down valve to bring current to idle
    switchOffValve()


def setValvePos(position):
    # Set controller in desired mode to set position
    initValve()

    # Connect to controller
    setup.initConnection()

    # convert decimal value to hex value
    posHex = f"{position:08x}"
    valueControlwordSetPos = "{}".format(posHex)

    # check if position doesn't exceed limits (480)
    if position > 260:
        print("Position cannot exceed 260")

    else:
        # Create string parameters to send to controller
        post = b"POST /od/" + str.encode(setup.indexTargetPos) + b"/" \
               + str.encode(setup.subindexTargetPos) + b" HTTP/1.0\r\nContent-Type: " \
                                                       b"application/x-www-form-urlencoded\r" \
                                                       b"\nContent-Length: " \
               + str.encode(setup.bitLengtTargetPos) + b"\r\n\r\n\"" \
               + str.encode(valueControlwordSetPos)  + b"\""

        # Send parameters to controller
        setup.initConnection().send(post)
        setup.initConnection().close()

    moveValve()

def target_reached():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((nanotec, nanotec_port))

    getTarget = b"GET /od/" + str.encode(setup.indexTargetReached) + b"/" \
             + str.encode(setup.subindexTargetPos) + b" HTTP/1.0\r\nHost: " \
                                                    b"10.58.32.239\r\nConnection: " \
                                                    b"Keep-Alive\r\n\r\n "

    sock.send(getTarget)
    result_get = sock.recv(10000)


    string = str(result_get, 'utf-8')
    match = re.search("application/json\r\n\r\n(.+)", string)
    if match:
        hex = (match.group(1))
        result = re.sub('[\W_]+', '', hex)
        data = int(result, 16)

        if data & (1 << 10):
            return True

    return False


def getValvePos():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((nanotec, nanotec_port))

    getPos = b"GET /od/" + str.encode(setup.indexPosValve) + b"/" \
             + str.encode(setup.subindexPosValve) + b" HTTP/1.0\r\nHost: " \
                                                    b"10.58.32.239\r\nConnection: " \
                                                    b"Keep-Alive\r\n\r\n "

    sock.send(getPos)
    result_get = sock.recv(10000)

    string = str(result_get, 'utf-8')
    match = re.search("json\r\n\r\n\"(.+)", string)
    if match:
        hex = (match.group(1))
        result = re.sub('[\W_]+', '', hex)
        result = int(result, 16)
        if result != 0:
            currentPos = abs(result - 2**32)
        else:
            currentPos = 0


    sock.close

    return currentPos


# ttiPsu.setTargetVolts(3, 12)
# ttiPsu.setOutputEnable(3, True)
#
print("before",getValvePos())
setValvePos(250)

print("after",getValvePos())

setValvePos(0)

print("after",getValvePos())