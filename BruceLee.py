import binascii
import configparser
import datetime
import re
import sys
import time
# from PyQt5.QtCore import QRegularExpression
# from PyQt5.QtGui import QRegularExpressionValidator

from crc import calc_crc
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from sendRes import *
from longgeforeverUI import *
from system import Child_ui
import serial.tools.list_ports
import public
import log

class MainUi(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        self.setupUi(self)
        self.uiInit()
        self.child_window = Child_ui()
        self.bindButton()
        self.showbandTitle = ' '
        self.ID=' '
        self.direction_clicks = 0
    def uiInit(self):
        # 初始化界面
        self.switchTag(0)
        self.defulti()
    def bindButton(self):
        # 绑定按钮
        self.pushButton_8.clicked.connect(self.workStart)
        self.pushButton_9.clicked.connect(self.workStop)
        self.pushButton_7.clicked.connect(self.showSystem)


       # 新增十进制可视数据和对应的按钮
        self.pushButton_90.clicked.connect(self.write_ID)
        self.pushButton_91.clicked.connect(self.write_mA)
        self.pushButton_92.clicked.connect(self.write_PPR)
        self.pushButton_93.clicked.connect(self.write_DIR)

        self.pushButton_scp.clicked.connect(self.write_scp)
        self.pushButton_peak_current.clicked.connect(self.write_peak_current) # 新增AR28 设置峰值电流
        self.pushButton_enable.clicked.connect(self.write_ena)
        self.pushButton_disable.clicked.connect(self.write_disab)
        self.pushButton_save.clicked.connect(self.write_save)
        self.pushButton_restore.clicked.connect(self.write_restore)

        self.pushButton_set0.clicked.connect(self.write_set0)
        self.pushButton_incr.clicked.connect(self.write_incr)
        self.pushButton_abso.clicked.connect(self.write_abso)

        self.pushButton_94.clicked.connect(self.write_SPD)

        self.pushButton_94_q.clicked.connect(self.write_spdq)       # 速度查询
        self.pushButton_acc.clicked.connect(self.write_acc)
        self.pushButton_acc_q.clicked.connect(self.write_accq)  #加速度查询
        self.pushButton_dec.clicked.connect(self.write_dec)
        self.pushButton_dec_q.clicked.connect(self.write_decq)  #减速度查询

        self.pushButton_94B.clicked.connect(self.write_SB)
        self.pushButton_94S.clicked.connect(self.write_S)
        self.pushButton_94F.clicked.connect(self.write_SF)

        self.pushButton_95.clicked.connect(self.write_DIS)
        self.pushButton_dis_q.clicked.connect(self.write_disq)    # 位移查询

        # self.pushButton_homez.clicked.connect(self.write_homez)
        # self.pushButton_homef.clicked.connect(self.write_homef)
        self.pushButton_95B.clicked.connect(self.write_DB)
        self.pushButton_95S.clicked.connect(self.write_S)
        self.pushButton_95F.clicked.connect(self.write_DF)


        self.pushButton_3.clicked.connect(self.Simple_Write_Serial)  #原来是 lambda: self.atwill(False)
        self.pushButton_4.clicked.connect(lambda: self.atwill(True))
        self.pushButton_10.clicked.connect(lambda: self.clearShow(''))
        self.pushButton_16.clicked.connect(lambda: self.clearShow('_2'))

    def link_clicked(self, MainWindow):
        webbrowser.open("https://www.stepping-motor.cn")
    def defulti(self):
        # 读取本机串口写入配置文件
        serialArr = list(serial.tools.list_ports.comports())
        if len(serialArr) <=0:
            # print('not find portlist')
            self.showBox('Serial Port is Not Found ')
            public.checkOpen = 0
        else:
            public.checkOpen = 1
        serial_list = []
        for i in list(serialArr):
            serial_list.append(i[0])
        # print(serial_list,'port')
        read = configparser.ConfigParser()
        read.read('system.ini')
        read.set('serial','port', ",".join(str(i) for i in serial_list))
        portSystem = readIni.readSerial()
        baud = portSystem.get('baud').split(',')
        port_num = portSystem.get('porttag')
        if len(serial_list)-1 < int(port_num):
            self.showBox('The configuration of serial port has been changed,\n '
                         'Please confirm it in the setting')
            read.set('serial','porttag','0')
        read.write(open('system.ini', "w"))


    def showSystem(self):
        # 子窗口实例
        self.child_window.setWindowModality(Qt.ApplicationModal)
        self.child_window.show()

    def sersRes(self,datas):
        # self.sendShow(datas, '')
        datas = binascii.a2b_hex(datas)
        self.startWork.ser.write(datas)
        time.sleep(0.1)
        if self.startWork.ser.inWaiting():
            res = self.startWork.ser.read(self.startWork.ser.inWaiting())
            self.startWork.ser.flushInput()
            return res


    def Simple_Write_Serial(self):
        # 自定义命令
        if not public.openSer:
            self.showBox('Please open the serial port first')
            return

        datas = self.lineEdit_14.text()
        datas = datas.replace(' ', '')

        if not datas:
            self.showBox('Cannot be empty')
            return

        if datas.endswith(';'):  # 字符串命令
            datas=datas.encode('gbk').hex()
            self.sendShow(datas.encode('gbk').hex(), '')
            r=self.sersRes(datas)
            if not r:
                return
            self.sendShow(r.hex(), '_2')
            return


        self.sendShow(datas, '')
        r = self.sersRes(datas)

        if not r:
            return
        self.sendShow(r.hex(), '_2')


    def atwill(self,crc):
        # 自定义命令
        if not public.openSer:
            self.showBox('Please open the serial port first')
            return
        datas = self.lineEdit_14.text()
        datas = datas.replace(' ','')
        if not datas:
            self.showBox('Cannot be empty')
            return
        if len(datas)%2 !=0:
            self.showBox('Command error')
            return
        if crc:
            datas = datas + calc_crc(datas)
            # self.sendShow(datas,'')
            # return
        self.sendShow(datas, '')
        # print(datas)
        r = self.sersRes(datas)
        # r = self.sersRes(datas).hex() if self.sersRes(datas) else 'The return value is null !!'
        # print(r)
        if not r:
            return
        self.sendShow(r.hex(), '_2')



# 新增的可视按钮操作，十进制数据处理的按钮
    # 设置和获取 ID
    def write_ID(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            # self.# '^lineEdit_[a-zA-Z0-9_]+$'   , 不连接不要输入??
            return

        num = self.lineEdit_90.text()
        if not num:
            self.showBox("can't empty")
            return

        try:
            self.ID=hex(int(num))[2:].zfill(2).upper()
        except ValueError:
            self.showBox('Input must be a valid integer number!')
            return
        self.ID
        self.textBrowser_2.append("Motor ID:" + num +" ("+self.ID +")")
    # 设置电流 闭环是改为读取电流了
    def write_mA(self): # AR28驱动器使用的03读取, 其他是06设置
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()
        num = self.lineEdit_91.text()

        order = self.ID + '0300000001'
        order = order + calc_crc(order)
        self.send_order(order)
        qr=self.sersRes(order)
        qr=qr.hex()
        value=int(qr.replace(' ','')[-8:-4], 16)
        self.lineEdit_91.setText(str(value))
    # 设置细分
    def write_PPR(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()
        num = self.lineEdit_92.text()
        if not num:
            self.showBox('Incorrect parameters')
            return

        order = self.ID + '060001' + hex(int(num))[2:].zfill(4)
        order = order + calc_crc(order)
        self.send_order(order)

     # 转向按钮的变化
    def direction(self):
        self.direction_clicks += 1
        if self.direction_clicks % 2 != 0:
            self.label_93.setStyleSheet("font-size: 13px; font-weight: bold; color: #00C1AB;")
            self.label_93.setText("    CW")
            return '0'

        elif self.direction_clicks % 2 == 0:
            self.label_93.setStyleSheet("font-size: 13px; font-weight: bold; color: #00C1AB;")
            self.label_93.setText("    CCW")
            return '1'

    def write_DIR(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()
        order = self.ID + '060033'+'000' + self.direction()
        order = order + calc_crc(order)
        self.send_order(order)

    def _validate_percentage_input(self, input_str, field_name):
        """
        通用的百分比数值校验函数（0~100）
        :param input_str: 文本框输入的字符串
        :param field_name: 字段名称（用于错误提示）
        :return: 校验通过返回数值(int)，失败返回None
        """
        # 1. 检查是否为空
        if not input_str:
            self.showBox(f'{field_name} cannot be empty')
            return None

        # 2. 检查是否为有效数字
        try:
            num = int(input_str)
        except ValueError:
            self.showBox(f'{field_name} must be an integer (0~100)')
            return None

        # 3. 检查数值范围
        if not (0 <= num <= 100):
            self.showBox(f'{field_name} must be between 0 and 100')
            return None

        return num

    def write_scp(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()
        # 调用通用校验函数
        num = self._validate_percentage_input(self.lineEdit_scp.text(), 'SCP value')
        if num is None:
            return

        order = self.ID + '060003' + hex(num)[2:].zfill(4)
        order = order + calc_crc(order)
        self.send_order(order)

    # 新增AR28驱动器设置峰值电流百分比
    def write_peak_current(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()
        # 调用通用校验函数
        num = self._validate_percentage_input(self.lineEdit_peakc.text(), 'Peak current value')
        if num is None:
            return

        order = self.ID + '06001A' + hex(num)[2:].zfill(4)
        order = order + calc_crc(order)
        self.send_order(order)

# 设置使能，电机锁州
    def write_ena(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()

        order = self.ID + '0600070001'
        order = order + calc_crc(order)
        self.sendShow(order, '')

        order = self.ID + '0600060001'
        order = order + calc_crc(order)
        self.send_order(order)

        # 设置不使能
    def write_disab(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()

        order = self.ID + '0600060000'
        order = order + calc_crc(order)
        self.sendShow(order, '')

        order = self.ID + '0600070000'
        order = order + calc_crc(order)
        self.sendShow(order, '')

        order = self.ID + '0600060000'
        order = order + calc_crc(order)
        self.send_order(order)
    # 保存参数
    def write_save(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()

        order = self.ID + '06005A0001'
        order = order + calc_crc(order)
        self.send_order(order)

    # 恢复出厂设置
    def write_restore(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()

        order = self.ID + '06005B0001'
        order = order + calc_crc(order)
        self.send_order(order)

    # 清零脉冲数的 命令按钮,  x28 写入0001，查询X27 28的值 搁置 待验证 ??
    def write_set0(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()

        order = self.ID + '0600280001'
        order = order + calc_crc(order)
        self.send_order(order)
    # 位移增量模式
    def write_incr(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()

        order = self.ID + '0600480000'
        order = order + calc_crc(order)
        self.send_order(order)

    # 位移绝对值模式
    def write_abso(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()

        order = self.ID + '0600480001'
        order = order + calc_crc(order)
        self.send_order(order)

    # 设置速度
    def write_SPD(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()
        num = self.lineEdit_94.text()
        if not num:
            self.showBox('Incorrect parameters')
            return

        num = int(num)
        if num < 0:
            num = abs(num)

        if int(num) <= 65535:
            self.high_spd_clear()
            hex_num = hex(int(num))[2:].zfill(4).upper()
            order = self.ID + '060040' + hex_num

        else:
            remainder = int(num) % 65536
            quotient = int(num) // 65536
            hex_num = (hex(remainder)[2:].zfill(4) + hex(quotient)[2:].zfill(4))
            order = self.ID + '100040000204' + hex_num

        order = order + calc_crc(order)
        self.send_order(order)

    # 设置的速度值不超过65535时, 要清除掉之前SPD的高位数据
    def high_spd_clear(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        order = self.ID + '060041' + '0000'
        order = order + calc_crc(order)
        self.send_order(order)

    # 设置加速度
    def write_acc(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()
        num = self.lineEdit_acc.text()
        if not num:
            self.showBox('Incorrect parameters')
            return

        try:
            num = int(num)
            if num < 0:  # 负数不起作用，
                self.showBox("Negative numbers are not supported")
                return

            if num > 2147483648:  # 超出范围
                self.showBox('Number exceeds 2147483648')
                return

            if int(num) <= 65535:
                self.high_acc_clear()
                hex_num = hex(int(num))[2:].zfill(4).upper()
                order = self.ID + '060042' + hex_num

            else:
                remainder = int(num) % 65536
                quotient = int(num) // 65536
                hex_num = (hex(remainder)[2:].zfill(4) + hex(quotient)[2:].zfill(4))
                order = self.ID + '100042000204' + hex_num

            order = order + calc_crc(order)
            self.send_order(order)

        except Exception as e:
            print(e)
            self.textBrowser_2.setText(str(e))

    # 设置的加速度值不超过65535时, 要清除掉之前的高位数据
    def high_acc_clear(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        order = self.ID + '060043' + '0000'
        order = order + calc_crc(order)
        self.send_order(order)

    # 设置减速度
    def write_dec(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()
        num = self.lineEdit_dec.text()
        if not num:
            self.showBox('Incorrect parameters')
            return

        try:
            num = int(num)
            if num < 0:  # 负数不起作用，
                self.showBox("Negative numbers are not supported")
                return

            if num > 2147483648:  # 超出范围
                self.showBox('Number exceeds 2147483648')
                return

            if int(num) <= 65535:
                self.high_dec_clear()
                hex_num = hex(int(num))[2:].zfill(4).upper()
                order = self.ID + '06003E' + hex_num

            else:
                remainder = int(num) % 65536
                quotient = int(num) // 65536
                hex_num = (hex(remainder)[2:].zfill(4) + hex(quotient)[2:].zfill(4))
                order = self.ID + '10003E000204' + hex_num

            order = order + calc_crc(order)
            self.send_order(order)

        except Exception as e:
            print(e)
            self.textBrowser_2.setText(str(e))

    # 设置的加速度值不超过65535时, 要清除掉之前的高位数据
    def high_dec_clear(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        order = self.ID + '06003F' + '0000'
        order = order + calc_crc(order)
        self.send_order(order)

    # 设置位移 pulses,
    def write_DIS(self):
        # self.write_SPD()
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        num = self.lineEdit_95.text()
        if not num:
            self.showBox('Incorrect parameters')
            return

        try:
            num = int(num)

            if num < -2147483648:  # 负数超出范围
                self.showBox('Negative number exceeds -2147483648')
                return

            if num > 2147483648:  # 正数超出范围
                self.showBox('Number exceeds 2147483648')
                return

            if num < 0:  # 处理负数
                # 负数转为补码表示
                num = (1 << 32) + num

            if num <= 65535:
                self.high_dis_clear()
                hex_num = hex(num)[2:].zfill(4).upper()
                order = '060044' + hex_num
            elif 65536 <= num <= (1 << 32) - 1:  # 包括负数补码范围
                remainder = num % 65536
                quotient = num // 65536
                hex_num = (hex(remainder)[2:].zfill(4) + hex(quotient)[2:].zfill(4)).upper()
                order = '100044000204' + hex_num
            else:
                self.showBox('Number out of supported range')
                return

            order = self.ID + order
            order = order + calc_crc(order)
            self.send_order(order)

        except Exception as e:
            print(e)
            self.textBrowser_2.setText(str(e))

    # 设置的位移不超过65535，高位数据不会被覆盖,需要把高位的数据清零
    def high_dis_clear(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        # order = self.ID + '060045' + '0000'
        order = ''.join([self.ID, '060045', '0000'])
        order = order + calc_crc(order)
        self.send_order(order)
        # self.sendShow(order, '')
        # r = self.sersRes(order)
        # if not r:
        #     self.textBrowser_2.setText('The return value is null')
        #
        #     return
        # r = r.hex()
        # self.textBrowser_2.setText('Sent successfully')
        # self.sendShow(r, '_2')

    # 简化代码，既然重复调用 有26个  null successfuly,
    def send_order(self, order):
        self.sendShow(order, '')
        r = self.sersRes(order)
        if not r:
            # 将setText改为append，确保不覆盖之前的内容
            self.textBrowser_2.append('The return value is null')
            return
        r = r.hex()
        # 将setText改为append，确保不覆盖之前的内容
        self.textBrowser_2.append('Sent successfully')
        self.sendShow(r, '_2')

    # 速度查询  需要测试
    def write_spdq(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()

        order1=''.join([self.ID, '030040', '0001'])
        order1 = order1 + calc_crc(order1)
        self.sendShow(order1, '')
        r1 = self.sersRes(order1)

        r1=r1.hex()
        self.sendShow(r1, '_2')
        value1=int(r1.replace(' ','')[-8:-4], 16)


        order2 = ''.join([self.ID, '030041', '0001'])
        order2 = order2 + calc_crc(order2)
        self.sendShow(order2, '')

        r2 = self.sersRes(order2)
        r2 = r2.hex()
        self.sendShow(r2, '_2')
        value2 = int(r2.replace(' ', '')[-8:-4], 16)*65536

        value = str(value1 + value2)

        self.lineEdit_94_q.setText(value)
        # 添加查询结果显示到textBrowser_2
        self.textBrowser_2.append(f"Speed: {value}")

    # 加速度查询  需要测试
    def write_accq(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()

        # order1 = self.ID + '030042' + '0001'
        order1 = ''.join([self.ID, '030042', '0001'])
        order1 = order1 + calc_crc(order1)

        self.sendShow(order1, '')
        r1 = self.sersRes(order1)
        r1 = r1.hex()
        self.sendShow(r1, '_2')
        value1 = int(r1.replace(' ', '')[-8:-4], 16)


        # order2 = self.ID + '030043' + '0001'
        order2 = ''.join([self.ID, '030043', '0001'])
        order2 = order2 + calc_crc(order2)

        self.sendShow(order2, '')
        r2 = self.sersRes(order2)
        r2 = r2.hex()
        self.sendShow(r2, '_2')
        value2 = int(int(r2.replace(' ', '')[-8:-4], 16)*65536)

        value = str(value1 + value2)
        self.lineEdit_acc_q.setText(value)
        # 添加查询结果显示到textBrowser_2
        self.textBrowser_2.append(f"Acceleration: {value}")

 # 减速度查询  需要测试
    def write_decq(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        self.write_ID()

        # order1 = self.ID + '03003E' + '0001'
        order1 = ''.join([self.ID, '03003E', '0001'])
        order1 = order1 + calc_crc(order1)

        self.sendShow(order1, '')
        r1 = self.sersRes(order1)
        r1 = r1.hex()
        self.sendShow(r1, '_2')
        value1 = int(r1.replace(' ', '')[-8:-4], 16)

        # order2 = self.ID + '03003F' + '0001'
        order2 = ''.join([self.ID, '03003F', '0001'])
        order2 = order2 + calc_crc(order2)

        self.sendShow(order2, '')
        r2 = self.sersRes(order2)
        r2 = r2.hex()
        self.sendShow(r2, '_2')
        value2 = int(int(r2.replace(' ', '')[-8:-4], 16)*65536)

        value = str(value1 + value2)
        self.lineEdit_dec_q.setText(value)
        # 添加查询结果显示到textBrowser_2
        self.textBrowser_2.append(f"Deceleration: {value}")

    # 位移查询  需要测试
    def write_disq(self):
        def hex_to_signed_int(hex_str):
            """将8位十六进制字符串转换为32位有符号整数"""
            # 确保输入是8位十六进制字符串
            if len(hex_str) != 8:
                raise ValueError("Hex string must be 8 characters long")

            # 将十六进制字符串转换为整数
            num = int(hex_str, 16)

            # 检查最高有效位（符号位）
            if num >= 0x80000000:
                # 如果符号位是1，则表示负数，需要转换为补码
                num -= 0x100000000

            return num

        try:
            if not public.openSer:
                self.showBox('Open the serial port')
                return

            self.write_ID()

            # 读取低位寄存器
            order1 = ''.join([self.ID, '030027', '0001'])
            order1 = order1 + calc_crc(order1)
            self.sendShow(order1, '')
            r1 = self.sersRes(order1)
            r1_hex = r1.hex()
            self.sendShow(r1_hex, '_2')
            if len(r1_hex) < 8:
                self.showBox('Error: response from r1 is too short')
                return
            value1 = r1_hex.replace(' ', '')[-8:-4]

            # 读取高位寄存器
            order2 = ''.join([self.ID, '030028', '0001'])
            order2 = order2 + calc_crc(order2)
            self.sendShow(order2, '')
            r2 = self.sersRes(order2)
            r2_hex = r2.hex()
            self.sendShow(r2_hex, '_2')
            if len(r2_hex) < 8:
                self.showBox('Error: response from r2 is too short')
                return
            value2 = r2_hex.replace(' ', '')[-8:-4]

            # 组合高位和低位值
            str_value = value2 + value1
            value = hex_to_signed_int(str_value)

            self.lineEdit_dis_q.setText(str(value))
            # 添加查询结果显示到textBrowser_2
            self.textBrowser_2.append(f"Displacement: {value}")

        except Exception as e:
            print(f"An error occurred: {e}")
            self.showBox(f"An error occurred: {e}")
    # 设置暂停按钮
    def write_S(self):
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        order = self.ID + '0600460000'
        order = order + calc_crc(order)
        self.send_order(order)
    def write_SB(self):

        # self.write_SPD()
        self.write_S()

        order = self.ID + '0600460004'
        order = order + calc_crc(order)
        self.send_order(order)
    # 正向连续
    def write_SF(self):
        # self.write_SPD()
        self.write_S()

        order = self.ID + '0600460003'
        order = order + calc_crc(order)
        self.send_order(order)

# # 正向限位信号为零点回零
#     def write_homez(self):
#         if not public.openSer:
#             self.showBox('Open the serial port')
#             return
#
#         self.write_ID()
#
#         order = self.ID + '0600470001'
#         order = order + calc_crc(order)
#         self.send_order(order)
#
#     # 正向限位信号为零点回零
#     def write_homef(self):
#         if not public.openSer:
#             self.showBox('Open the serial port')
#             return
#
#         self.write_ID()
#
#         order = self.ID + '0600470002'
#         order = order + calc_crc(order)
#         self.send_order(order)

#  设置反向一段位移
    def write_DB(self):
        self.write_S()
        # self.write_SPD()
        # self.write_DIS()
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        order = self.ID + '0600460002'
        order = order + calc_crc(order)
        self.send_order(order)

    # 设置正向一段位移
    def write_DF(self):
        self.write_S()
        # self.write_SPD()
        # self.write_DIS()
        if not public.openSer:
            self.showBox('Open the serial port')
            return

        order = self.ID + '0600460001'
        order = order + calc_crc(order)
        self.send_order(order)

    def switchTag(self,tag):

        if tag:
            self.pushButton_8.setEnabled(False)
            self.pushButton_9.setEnabled(True)
            self.pushButton_7.setEnabled(False)
            self.label_17.setText('Work')
            self.label_17.setStyleSheet("color: #a0ffd0; font-size: 16px;")
            self.status_led.setStyleSheet("background-color: #36ff00; border-radius: 15px; border: 1px solid #f8d568;")
        else:
            self.pushButton_8.setEnabled(True)
            self.pushButton_7.setEnabled(True)
            self.pushButton_9.setEnabled(False)
            self.label_17.setText('Standby')
            self.status_led.setStyleSheet("background-color: #d32f2f; border-radius: 15px; border: 1px solid #f8d568;")

    def serialThread(self):
        # 串口线程
        self.startWork = SendRes()
        self.startWork._signal.connect(self.serialRes, type=QtCore.Qt.DirectConnection)
        self.startWork.start()

    def serialRes(self,data):
        # 串口返回值
        self.startWork.quit()
        self.workStop()
        try:
            self.showBox('Failed to open serial port, please try again!')
        except Exception as e:
            print(e)

    def workStart(self):
        self.switchTag(1)
        public.openSer = 1
        if not public.checkOpen:
            self.showBox('The serial port is empty, please check!')
            self.workStop()
            return
        self.serialThread()
        time.sleep(0.3)
        self.groupBox.setTitle(public.current)

    def workStop(self):
        self.switchTag(0)
        public.openSer = 0
        self.groupBox.setTitle('Serial port settings')

    def sendShow(self,keys,name):
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        showArr = '[' + str(now_time) + '] ' + re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", keys.upper())
        eval('self.textBrowser%s.append(showArr)' %name)
    def clearShow(self,keys):
        eval('self.textBrowser%s.clear()' %keys)
    def showBox(self,datas):
        QMessageBox.critical(self,'Error',datas)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    # 添加字体设置 (关键修复)
    font = QFont("Microsoft YaHei UI", 9)
    app.setFont(font)

    a = MainUi()
    a.show()
    sys.exit(app.exec_())

