import configparser
import os

######### 读配置文件 ############

class readIni():
    init_path = os.getcwd()

    def readSerial():
        read_ini = configparser.ConfigParser()
        read_ini.read('system.ini')
        resDict = {
            'port' : read_ini.get('serial', 'port'),
            'baud' : read_ini.get('serial', 'baud'),
            'parity' : read_ini.get('serial', 'parity'),
            'porttag' : read_ini.get('serial', 'porttag'),
            'baudtag': read_ini.get('serial', 'baudtag'),
            'paritytag': read_ini.get('serial', 'paritytag'),
            'stopbits': read_ini.get('serial', 'stopbits'),
            'stoptag': read_ini.get('serial', 'stoptag'),
            'bytesize': read_ini.get('serial', 'bytesize'),
            'bytetag': read_ini.get('serial', 'bytetag'),

        }
        read_ini.clear()
        return (resDict)
