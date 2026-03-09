from cx_Freeze import setup, Executable
import sys
import os

base = "Win32GUI" if sys.platform == "win32" else None
current_dir = os.path.dirname(os.path.abspath(__file__))

# 包含所有需要的资源文件
include_files = [
    (os.path.join(current_dir, "logo.ico"), "logo.ico"),
    (os.path.join(current_dir, "wu.ico"), "wu.ico"),
    (os.path.join(current_dir, "bruce_bg.jpg"), "bruce_bg.jpg"),
    (os.path.join(current_dir, "system.ini"), "system.ini"),
    # 如有其他资源，按此格式添加
]

# 包含必要的 Python 模块
includes = ["PyQt5", "sys", "os", "webbrowser"]
excludes = ["tkinter"]  # 排除不需要的模块以减小体积

options = {
    "build_exe": {
        "build_exe": "dist_temp",  # 临时目录，用于后续压缩
        "include_files": include_files,
        "includes": includes,
        "excludes": excludes,
        "include_msvcr": True,     # 包含VC运行库
        "optimize": 2,             # 代码优化
        "packages": ["PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets"],
    }
}

executables = [
    Executable(
        script="longyouhuaen.py",
        base=base,
        target_name="longyouhuaen.exe",
        icon="logo.ico"
    )
]

setup(
    name="longyouhuaen",
    version="1.0",
    description="MODBUS RTU Debugging Software",
    options=options,
    executables=executables
)