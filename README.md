# RS485 Stepper Motor Driver

[![Python CI](https://github.com/Simon2022s/RS485-Stepper-Motor-Driver/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Simon2022s/RS485-Stepper-Motor-Driver/actions/workflows/python-ci.yml)

基于 PyQt5 的 RS485 步进电机驱动控制软件，支持 Modbus RTU 协议通信。

![AR28 Driver](bruce_bg.jpg)

## 🚀 功能特性

- **串口通信**: 支持 RS485 串口通信，自动检测可用串口
- **电机控制**: 速度、加速度、减速度、位移控制
- **参数设置**: 电流、PPR（每转脉冲数）、方向设置
- **实时监控**: 速度、位置、电流实时查询
- **运动模式**: 连续运动、增量位移、绝对位移
- **数据记录**: 支持命令发送和接收日志记录
- **美观界面**: 李小龙主题 UI 设计

## 📋 系统要求

- Python 3.8+
- Windows / Linux / macOS
- RS485 转 USB 适配器

## 🔧 安装

### 1. 克隆仓库

```bash
git clone https://github.com/Simon2022s/RS485-Stepper-Motor-Driver.git
cd RS485-Stepper-Motor-Driver
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 🎮 使用方法

### 运行程序

```bash
python BruceLee.py
```

### 基本操作

1. **连接串口**: 点击 "Serial Setup" 配置串口参数，然后点击 "Open"
2. **设置电机 ID**: 在 Motor ID 输入框输入电机地址（默认 1）
3. **设置参数**: 
   - 速度 (Speed): 设置目标速度（脉冲/秒）
   - 加速度 (Acceleration): 设置加速度
   - 减速度 (Deceleration): 设置减速度
4. **控制电机**:
   - Enable: 使能电机
   - ▶▶: 正向连续运动
   - ◀◀: 反向连续运动
   - ||: 暂停
   - Disable: 禁用电机

### 高级功能

- **自定义命令**: 在 Hex Command 区域输入 Modbus 命令直接发送
- **查询功能**: 使用 🔍 按钮查询当前参数值
- **参数保存**: 点击 Save 将参数保存到电机 EEPROM

## 📁 项目结构

```
RS485-Stepper-Motor-Driver/
├── BruceLee.py              # 主程序入口
├── longgeforeverUI.py       # 主界面 UI
├── rsNew.py                 # 串口设置对话框 UI
├── system.py                # 系统设置模块
├── sendRes.py               # 串口通信线程
├── crc.py                   # CRC16 校验
├── readIni.py               # 配置文件读取
├── public.py                # 全局变量
├── log.py                   # 日志模块
├── system.ini               # 配置文件
├── bruce_bg.jpg             # 背景图片
├── logo.ico                 # 程序图标
├── wu.ico                   # 窗口图标
├── requirements.txt         # 依赖列表
├── CODE_REVIEW.md           # 代码审核报告
└── optimized_example.py     # 优化示例代码
```

## 🔌 通信协议

本软件使用 **Modbus RTU** 协议与电机驱动器通信。

### 常用寄存器

| 寄存器地址 | 功能 | 说明 |
|-----------|------|------|
| 0x0000 | 电流 | 读取/设置电流 |
| 0x0001 | PPR | 每转脉冲数 |
| 0x0003 | 待机电流 | 待机电流百分比 |
| 0x001A | 峰值电流 | 峰值电流百分比 |
| 0x0040 | 速度低位 | 速度值低 16 位 |
| 0x0041 | 速度高位 | 速度值高 16 位 |
| 0x0042 | 加速度低位 | 加速度低 16 位 |
| 0x0043 | 加速度高位 | 加速度高 16 位 |
| 0x0044 | 位移低位 | 位移值低 16 位 |
| 0x0045 | 位移高位 | 位移值高 16 位 |
| 0x0046 | 控制模式 | 启动/停止/方向控制 |
| 0x0048 | 位置模式 | 增量/绝对模式 |

### CRC 校验

使用 Modbus RTU 标准的 CRC16 校验算法。

## 🛠️ 开发

### 代码规范

- 遵循 PEP 8 代码风格
- 使用类型注解
- 编写文档字符串

### 运行测试

```bash
pytest
```

### 代码检查

```bash
# 代码风格检查
flake8 .

# 类型检查
mypy .

# 安全检查
bandit -r .
```

## 📦 打包

使用 PyInstaller 打包为可执行文件：

```bash
pyinstaller --onefile --windowed --icon=logo.ico BruceLee.py
```

## 📝 更新日志

### v1.0.0 (2026-03-09)
- ✨ 初始版本发布
- 🎨 李小龙主题 UI
- 🔧 支持 AR28 驱动器
- 📊 实时参数查询

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- PyQt5 - GUI 框架
- pySerial - 串口通信库
- 步进电机驱动器制造商

---

**注意**: 本软件仅供学习和测试使用，工业环境使用前请充分测试。
