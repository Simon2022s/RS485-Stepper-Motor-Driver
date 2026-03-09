import configparser

from PyQt5.QtWidgets import QWidget
from rsNew import Ui_Form
from readIni import readIni

class Child_ui(QWidget,Ui_Form):
    def __init__(self):
        super(Child_ui,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.saveButton)
        self.readSys()

    def saveButton(self):
        self.close()
        print(self.comboBox_2.currentIndex())
        read = configparser.ConfigParser()
        read.read('system.ini')
        read.set('serial', 'porttag', str(self.comboBox.currentIndex()))
        read.set('serial', 'baudtag', str(self.comboBox_2.currentIndex()))
        read.set('serial', 'paritytag', str(self.comboBox_3.currentIndex()))
        read.set('serial', 'stoptag', str(self.comboBox_5.currentIndex()))
        read.set('serial', 'bytetag', str(self.comboBox_4.currentIndex()))
        read.write(open('system.ini', "w"))

    def readSys(self):
        res = readIni.readSerial()
        serialBaud = res.get('baud').split(',')
        self.comboBox_2.addItems(serialBaud)
        self.comboBox_2.setCurrentIndex(int(res.get('baudtag')))
        serialport = res.get('port').split(',')
        self.comboBox.addItems(serialport)
        self.comboBox.setCurrentIndex(int(res.get('porttag')))
        parity = res.get('parity').split(',')
        self.comboBox_3.addItems(parity)
        self.comboBox_3.setCurrentIndex(int(res.get('paritytag')))
        parity = res.get('stopbits').split(',')
        self.comboBox_5.addItems(parity)
        self.comboBox_5.setCurrentIndex(int(res.get('stoptag')))
        parity = res.get('bytesize').split(',')
        self.comboBox_4.addItems(parity)
        self.comboBox_4.setCurrentIndex(int(res.get('bytetag')))
