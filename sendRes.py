from PyQt5.QtCore import QThread,pyqtSignal,Qt

import public
from readIni import readIni
import serial
import serial.tools.list_ports
# from readIni import readIni
#####    串口线程  ##########

class SendRes(QThread):
    _signal = pyqtSignal(str)
    def __init__(self):
        super(SendRes,self).__init__()
        # self.run()
    def run(self):
        self.portSystem = readIni.readSerial()
        # print(portSystem)
        port = self.getinitolist('port','porttag')
        baud = self.getinitolist('baud','baudtag')
        paritys = self.getinitolist('parity','paritytag')
        stopbits = self.getinitolist('stopbits', 'stoptag')
        bytesize = self.getinitolist('bytesize', 'bytetag')
        try:
            # current = ''
            self.ser = serial.Serial(port, int(baud), timeout=0.1, stopbits=int(stopbits), parity=paritys,bytesize=int(bytesize))
            if self.ser.isOpen():
                print("open success")
                public.current = 'Serial Port:'+str(port)+' Baud Rate is：'+ str(baud)
                while True:
                    if not public.openSer:
                        self.ser.close()
                        break
        except Exception as e:
            print(e)
            self.rev_data = 'F01'
            self._signal.emit(self.rev_data)

    def getinitolist(self,data,key):
        res = self.portSystem.get(data).split(',')
        # print(key)
        res = res[int(self.portSystem.get(key))]
        return res
