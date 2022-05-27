import pyvisa
import socket
import setup

sample_interval_secs = 2.5

max_volt_setting = 30.0
max_milliamp_setting = 3000

rm = pyvisa.ResourceManager()


class ttiPsu(object):

    def __init__(self):
        self.ip = setup.MX100QP
        self.port = 9221  # default port for socket control
        # channel=1 for single PSU and right hand of Dual PSU
        # self.channel = channel
        self.ident_string = ''
        self.sock_timeout_secs = 10
        self.packet_end = bytes('\r\n', 'ascii')

    def send(self, cmd):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.sock_timeout_secs)
            s.connect((self.ip, self.port))
            s.sendall(bytes(cmd, 'ascii'))

    def recv_end(self, the_socket):
        total_data = []
        data = ''
        while True:
            data = the_socket.recv(1024)
            if self.packet_end in data:
                total_data.append(data[:data.find(self.packet_end)])
                break
            total_data.append(data)
            if len(total_data) > 1:
                # check if end_of_data was split
                last_pair = total_data[-2] + total_data[-1]
                if self.packet_end in last_pair:
                    total_data[-2] = last_pair[:last_pair.find(self.packet_end)]
                    total_data.pop()
                    break
        return b''.join(total_data)

    # def send_receive_string(self, cmd):
    #     # print('Cmd', repr(cmd))
    #     self.mysocket.sendall(bytes(cmd, 'ascii'))
    #     data = self.recv_end(self.mysocket)
    #     # print('Received', repr(data))
    #     return data.decode('ascii')

    def send_receive_string(self, cmd):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.sock_timeout_secs)
            s.connect((self.ip, self.port))
            s.sendall(bytes(cmd, 'ascii'))
            data = s.recv(1024)
        # print('Received', repr(data))
        return data.decode('ascii')

    def send_receive_float(self, cmd):
        r = self.send_receive_string(cmd)
        # Eg. '-0.007V\r\n'  '31.500\r\n'  'V2 3.140\r\n'
        r = r.rstrip('\r\nVA')  # Strip these trailing chars
        l = r.rsplit()  # Split to array of strings
        if len(l) > 0:
            return float(l[-1])  # Convert number in last string to float
        return 0.0

    def send_receive_integer(self, cmd):
        r = self.send_receive_string(cmd)
        return int(r)

    def send_receive_boolean(self, cmd):
        if self.send_receive_integer(cmd) > 0:
            return True
        return False

    def getIdent(self):
        self.ident_string = self.send_receive_string('*IDN?')
        return self.ident_string.strip()

    def getConfig(self):
        cmd = 'CONFIG?'
        v = self.send_receive_integer(cmd)
        return v

    def getAmpRange(self):
        # Supported on PL series
        # Not supported on MX series
        r = 0
        try:
            cmd = 'IRANGE{}?'.format(self.channel)
            r = self.send_receive_integer(cmd)
        except:
            pass
        # The response is 1 for Low (500/800mA) range,
        # 2 for High range (3A or 6A parallel)
        # or 0 for no response / not supported
        return r

    def setAmpRangeLow(self):
        # Supported on PL series
        # Not supported on MX series
        cmd = 'IRANGE{} 1'.format(self.channel)
        self.send(cmd)

    def setAmpRangeHigh(self):
        # Supported on PL series
        # Not supported on MX series
        cmd = 'IRANGE{} 2'.format(self.channel)
        self.send(cmd)

    def getOutputIsEnabled(self):
        cmd = 'OP{}?'.format(self.channel)
        v = self.send_receive_boolean(cmd)
        return v

    def getOutputVolts(self, channel):
        cmd = 'V{}O?'.format(channel)
        v = self.send_receive_float(cmd)
        return v

    def getOutputAmps(self, channel):
        cmd = 'I{}O?'.format(channel)
        v = self.send_receive_float(cmd)
        return v

    def getTargetVolts(self):
        cmd = 'V{}?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    def getTargetAmps(self, channel):
        cmd = 'I{}?'.format(self, channel)
        v = self.send_receive_float(cmd)
        return v

    def getOverVolts(self):
        cmd = 'OVP{}?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    def getOverAmps(self):
        cmd = 'OCP{}?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    def setOutputEnable(self, channel, state):
        cmd = ''
        if state == True:
            cmd = 'OP{} 1'.format(channel)
        else:
            cmd = 'OP{} 0'.format(channel)
        self.send(cmd)

    def setTargetVolts(self, channel, volts):
        cmd = 'V{0} {1:2.3f}'.format(channel, volts)
        self.send(cmd)
        return volts

    def setTargetAmps(self, channel, amps):
        cmd = 'I{0} {1:1.3f}'.format(channel, amps)
        self.send(cmd)

    def setLocal(self):
        cmd = 'LOCAL'
        self.send(cmd)


ttiPsu = ttiPsu()
