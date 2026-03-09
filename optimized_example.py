"""
RS485 Stepper Motor Driver - 优化示例代码
展示如何改进代码质量和架构
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, Dict, Callable
import re
import datetime


# ============================================================================
# 1. 常量定义 - 替代魔法数字
# ============================================================================

class ModbusFunction(IntEnum):
    """Modbus 功能码"""
    READ_HOLDING_REGISTERS = 0x03
    WRITE_SINGLE_REGISTER = 0x06
    WRITE_MULTIPLE_REGISTERS = 0x10


class ModbusRegister(IntEnum):
    """Modbus 寄存器地址"""
    # 电流相关
    CURRENT = 0x0000
    STANDBY_CURRENT = 0x0003
    PEAK_CURRENT = 0x001A
    
    # 速度和加速度
    SPEED_LOW = 0x0040
    SPEED_HIGH = 0x0041
    ACCEL_LOW = 0x0042
    ACCEL_HIGH = 0x0043
    DECEL_LOW = 0x003E
    DECEL_HIGH = 0x003F
    
    # 位移
    DISPLACEMENT_LOW = 0x0044
    DISPLACEMENT_HIGH = 0x0045
    PULSE_COUNTER_LOW = 0x0027
    PULSE_COUNTER_HIGH = 0x0028
    
    # 控制
    ENABLE = 0x0006
    CLEAR_ENABLE = 0x0007
    CONTROL_MODE = 0x0046
    POSITION_MODE = 0x0048
    
    # 系统
    SAVE_PARAMS = 0x005A
    RESTORE_FACTORY = 0x005B
    DIRECTION = 0x0033
    PPR = 0x0001


class MotorCommand(IntEnum):
    """电机控制命令"""
    STOP = 0x0000
    FORWARD = 0x0001
    BACKWARD = 0x0002
    PAUSE = 0x0004


# ============================================================================
# 2. 数据类 - 类型安全
# ============================================================================

@dataclass
class MotorConfig:
    """电机配置"""
    device_id: int = 1
    max_speed: int = 65535
    max_acceleration: int = 2147483648
    
    def validate(self) -> bool:
        """验证配置有效性"""
        return 0 <= self.device_id <= 255


@dataclass  
class SerialConfig:
    """串口配置"""
    port: str
    baudrate: int = 9600
    parity: str = 'N'
    stopbits: int = 1
    bytesize: int = 8
    timeout: float = 0.1


# ============================================================================
# 3. Modbus 协议封装
# ============================================================================

class ModbusRTU:
    """Modbus RTU 协议实现"""
    
    @staticmethod
    def calc_crc(data: bytes) -> bytes:
        """计算 CRC16 校验码"""
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        # 交换高低字节
        return bytes([crc & 0xFF, (crc >> 8) & 0xFF])
    
    @staticmethod
    def build_frame(device_id: int, function: int, data: bytes) -> bytes:
        """
        构建 Modbus RTU 帧
        
        Args:
            device_id: 设备地址 (0-255)
            function: 功能码
            data: 数据部分
            
        Returns:
            完整的 Modbus RTU 帧
        """
        frame = bytes([device_id, function]) + data
        crc = ModbusRTU.calc_crc(frame)
        return frame + crc
    
    @staticmethod
    def parse_response(frame: bytes) -> Optional[Dict]:
        """
        解析 Modbus 响应帧
        
        Args:
            frame: 响应帧数据
            
        Returns:
            解析结果字典，或 None（如果校验失败）
        """
        if len(frame) < 4:
            return None
        
        # 验证 CRC
        data_part = frame[:-2]
        received_crc = frame[-2:]
        calculated_crc = ModbusRTU.calc_crc(data_part)
        
        if received_crc != calculated_crc:
            return None
        
        return {
            'device_id': frame[0],
            'function': frame[1],
            'data': frame[2:-2]
        }


# ============================================================================
# 4. 输入验证工具
# ============================================================================

class InputValidator:
    """输入验证工具类"""
    
    @staticmethod
    def validate_integer(
        text: str, 
        field_name: str,
        min_val: Optional[int] = None,
        max_val: Optional[int] = None
    ) -> Optional[int]:
        """
        验证整数输入
        
        Args:
            text: 输入文本
            field_name: 字段名称（用于错误提示）
            min_val: 最小值（可选）
            max_val: 最大值（可选）
            
        Returns:
            验证通过的整数值，或 None（验证失败）
        """
        if not text or not text.strip():
            raise ValueError(f"{field_name} cannot be empty")
        
        try:
            num = int(text.strip())
        except ValueError:
            raise ValueError(f"{field_name} must be a valid integer")
        
        if min_val is not None and num < min_val:
            raise ValueError(f"{field_name} must be >= {min_val}")
        
        if max_val is not None and num > max_val:
            raise ValueError(f"{field_name} must be <= {max_val}")
        
        return num
    
    @staticmethod
    def validate_hex_string(text: str, field_name: str = "Value") -> str:
        """验证十六进制字符串"""
        text = text.strip().replace(' ', '')
        
        if not text:
            raise ValueError(f"{field_name} cannot be empty")
        
        if len(text) % 2 != 0:
            raise ValueError(f"{field_name} must have even number of characters")
        
        try:
            int(text, 16)
        except ValueError:
            raise ValueError(f"{field_name} must be valid hexadecimal")
        
        return text.upper()


# ============================================================================
# 5. 电机控制器 - 核心业务逻辑
# ============================================================================

class MotorController:
    """步进电机控制器"""
    
    def __init__(self, config: MotorConfig):
        self.config = config
        self._device_id_hex = f"{config.device_id:02X}"
    
    def _build_read_command(self, register: int, count: int = 1) -> str:
        """构建读取寄存器命令"""
        data = f"{register:04X}{count:04X}"
        frame = ModbusRTU.build_frame(
            self.config.device_id,
            ModbusFunction.READ_HOLDING_REGISTERS,
            bytes.fromhex(data)
        )
        return frame.hex().upper()
    
    def _build_write_command(self, register: int, value: int) -> str:
        """构建写入单个寄存器命令"""
        data = f"{register:04X}{value:04X}"
        frame = ModbusRTU.build_frame(
            self.config.device_id,
            ModbusFunction.WRITE_SINGLE_REGISTER,
            bytes.fromhex(data)
        )
        return frame.hex().upper()
    
    def _build_write_32bit_command(self, register_low: int, value: int) -> str:
        """构建写入 32 位值命令（使用两个寄存器）"""
        if value <= 65535:
            # 16 位值
            return self._build_write_command(register_low, value)
        
        # 32 位值 - 使用功能码 0x10
        low = value & 0xFFFF
        high = (value >> 16) & 0xFFFF
        
        # 10 功能码: 设备ID 功能码 起始地址 寄存器数量 字节数 数据...
        data = bytes.fromhex(
            f"{register_low:04X}000204"  # 起始地址, 寄存器数量, 字节数
            f"{low:04X}{high:04X}"        # 数据（低字节在前）
        )
        frame = ModbusRTU.build_frame(
            self.config.device_id,
            ModbusFunction.WRITE_MULTIPLE_REGISTERS,
            data
        )
        return frame.hex().upper()
    
    # ========== 电机参数设置 ==========
    
    def set_speed(self, speed: int) -> str:
        """设置速度"""
        speed = InputValidator.validate_integer(
            str(speed), "Speed", 0, self.config.max_speed
        )
        return self._build_write_32bit_command(
            ModbusRegister.SPEED_LOW, speed
        )
    
    def set_acceleration(self, accel: int) -> str:
        """设置加速度"""
        accel = InputValidator.validate_integer(
            str(accel), "Acceleration", 0, self.config.max_acceleration
        )
        return self._build_write_32bit_command(
            ModbusRegister.ACCEL_LOW, accel
        )
    
    def set_deceleration(self, decel: int) -> str:
        """设置减速度"""
        decel = InputValidator.validate_integer(
            str(decel), "Deceleration", 0, self.config.max_acceleration
        )
        return self._build_write_32bit_command(
            ModbusRegister.DECEL_LOW, decel
        )
    
    def set_displacement(self, displacement: int) -> str:
        """设置位移"""
        # 支持负数
        if displacement < 0:
            displacement = (1 << 32) + displacement
        
        return self._build_write_32bit_command(
            ModbusRegister.DISPLACEMENT_LOW, displacement
        )
    
    def set_current(self, percentage: int) -> str:
        """设置待机电流百分比"""
        percentage = InputValidator.validate_integer(
            str(percentage), "Current percentage", 0, 100
        )
        return self._build_write_command(
            ModbusRegister.STANDBY_CURRENT, percentage
        )
    
    def set_peak_current(self, percentage: int) -> str:
        """设置峰值电流百分比"""
        percentage = InputValidator.validate_integer(
            str(percentage), "Peak current percentage", 0, 100
        )
        return self._build_write_command(
            ModbusRegister.PEAK_CURRENT, percentage
        )
    
    def set_ppr(self, ppr: int) -> str:
        """设置每转脉冲数"""
        ppr = InputValidator.validate_integer(str(ppr), "PPR", 1)
        return self._build_write_command(ModbusRegister.PPR, ppr)
    
    def set_direction(self, direction: int) -> str:
        """设置方向 (0=CW, 1=CCW)"""
        direction = InputValidator.validate_integer(
            str(direction), "Direction", 0, 1
        )
        return self._build_write_command(
            ModbusRegister.DIRECTION, direction
        )
    
    # ========== 电机控制命令 ==========
    
    def enable(self) -> str:
        """使能电机"""
        return self._build_write_command(ModbusRegister.ENABLE, 1)
    
    def disable(self) -> str:
        """禁用电机"""
        return self._build_write_command(ModbusRegister.ENABLE, 0)
    
    def stop(self) -> str:
        """停止电机"""
        return self._build_write_command(
            ModbusRegister.CONTROL_MODE, MotorCommand.STOP
        )
    
    def move_forward(self) -> str:
        """正向连续运动"""
        return self._build_write_command(
            ModbusRegister.CONTROL_MODE, MotorCommand.FORWARD
        )
    
    def move_backward(self) -> str:
        """反向连续运动"""
        return self._build_write_command(
            ModbusRegister.CONTROL_MODE, MotorCommand.BACKWARD
        )
    
    def move_forward_displacement(self) -> str:
        """正向位移运动"""
        return self._build_write_command(
            ModbusRegister.CONTROL_MODE, MotorCommand.FORWARD
        )
    
    def move_backward_displacement(self) -> str:
        """反向位移运动"""
        return self._build_write_command(
            ModbusRegister.CONTROL_MODE, MotorCommand.BACKWARD
        )
    
    def set_position_mode(self, mode: int) -> str:
        """
        设置位置模式
        
        Args:
            mode: 0=增量模式, 1=绝对模式
        """
        mode = InputValidator.validate_integer(str(mode), "Position mode", 0, 1)
        return self._build_write_command(ModbusRegister.POSITION_MODE, mode)
    
    def set_zero_position(self) -> str:
        """设置当前位置为零点"""
        return self._build_write_command(ModbusRegister.PULSE_COUNTER_HIGH, 1)
    
    def save_parameters(self) -> str:
        """保存参数到 EEPROM"""
        return self._build_write_command(ModbusRegister.SAVE_PARAMS, 1)
    
    def restore_factory_settings(self) -> str:
        """恢复出厂设置"""
        return self._build_write_command(ModbusRegister.RESTORE_FACTORY, 1)
    
    # ========== 查询命令 ==========
    
    def query_speed(self) -> tuple[str, str]:
        """查询速度（返回高低位两个命令）"""
        low = self._build_read_command(ModbusRegister.SPEED_LOW)
        high = self._build_read_command(ModbusRegister.SPEED_HIGH)
        return low, high
    
    def query_acceleration(self) -> tuple[str, str]:
        """查询加速度"""
        low = self._build_read_command(ModbusRegister.ACCEL_LOW)
        high = self._build_read_command(ModbusRegister.ACCEL_HIGH)
        return low, high
    
    def query_deceleration(self) -> tuple[str, str]:
        """查询减速度"""
        low = self._build_read_command(ModbusRegister.DECEL_LOW)
        high = self._build_read_command(ModbusRegister.DECEL_HIGH)
        return low, high
    
    def query_displacement(self) -> tuple[str, str]:
        """查询位移"""
        low = self._build_read_command(ModbusRegister.PULSE_COUNTER_LOW)
        high = self._build_read_command(ModbusRegister.PULSE_COUNTER_HIGH)
        return low, high
    
    def query_current(self) -> str:
        """查询电流"""
        return self._build_read_command(ModbusRegister.CURRENT)


# ============================================================================
# 6. 工具函数
# ============================================================================

def format_hex_display(hex_string: str) -> str:
    """
    格式化十六进制字符串显示
    例如: "01060040" -> "01 06 00 40"
    """
    hex_string = hex_string.replace(' ', '')
    return ' '.join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))


def hex_to_signed_int(hex_str: str) -> int:
    """
    将 32 位十六进制字符串转换为有符号整数
    
    Args:
        hex_str: 8 位十六进制字符串
        
    Returns:
        有符号整数
    """
    if len(hex_str) != 8:
        raise ValueError("Hex string must be 8 characters long")
    
    num = int(hex_str, 16)
    
    # 检查符号位
    if num >= 0x80000000:
        num -= 0x100000000
    
    return num


def parse_32bit_value(low_response: str, high_response: str) -> int:
    """
    解析 32 位值（由两个 16 位寄存器组成）
    
    Args:
        low_response: 低位寄存器响应（十六进制字符串）
        high_response: 高位寄存器响应（十六进制字符串）
        
    Returns:
        32 位整数值
    """
    # 提取数据部分（假设响应格式为: 设备ID 功能码 字节数 数据... CRC CRC）
    low_val = int(low_response[-8:-4], 16)
    high_val = int(high_response[-8:-4], 16)
    
    return low_val + (high_val << 16)


# ============================================================================
# 7. 使用示例
# ============================================================================

if __name__ == "__main__":
    # 创建电机配置
    config = MotorConfig(device_id=1)
    
    # 创建控制器
    controller = MotorController(config)
    
    # 示例 1: 设置速度
    cmd = controller.set_speed(6000)
    print(f"设置速度命令: {format_hex_display(cmd)}")
    
    # 示例 2: 设置加速度
    cmd = controller.set_acceleration(10000)
    print(f"设置加速度命令: {format_hex_display(cmd)}")
    
    # 示例 3: 设置位移（支持负数）
    cmd = controller.set_displacement(-50000)
    print(f"设置位移命令: {format_hex_display(cmd)}")
    
    # 示例 4: 查询速度
    low_cmd, high_cmd = controller.query_speed()
    print(f"查询速度低位: {format_hex_display(low_cmd)}")
    print(f"查询速度高位: {format_hex_display(high_cmd)}")
    
    # 示例 5: 使能电机
    cmd = controller.enable()
    print(f"使能电机命令: {format_hex_display(cmd)}")
    
    # 示例 6: 正向运动
    cmd = controller.move_forward()
    print(f"正向运动命令: {format_hex_display(cmd)}")
    
    # 验证 CRC
    test_data = bytes.fromhex("010600010032")
    crc = ModbusRTU.calc_crc(test_data)
    print(f"CRC 校验: {crc.hex().upper()}")  # 应输出 59C6
